"""
Script Principal - Demonstração Comparativa de Cenários de Glaucoma.

Executa três cenários em sequência:
  1. Paciente saudável (IOP normal)
  2. Glaucoma moderado sem tratamento
  3. Glaucoma moderado com tratamento (iniciado no meio da simulação)
"""

import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.config import (
    get_config,
    SCENARIO_NORMAL,
    SCENARIO_GLAUCOMA,
)
from scripts.retina import RetinaSim
from scripts.simulation import GlaucomaSimulator
from scripts.ai_model import GlaucomaPredictor, SimplePredictor, TENSORFLOW_AVAILABLE
from scripts.visualization import RetinaVisualizer
from utils import print_banner, save_simulation_results, create_directories_if_not_exist


# ---------------------------------------------------------------------------
# Número de passos para cada simulação (aumente para 500+ para maior detalhamento)
NUM_STEPS = 200
LOG_INTERVAL = 50
TREATMENT_STEP = 100  # Passo em que o tratamento é iniciado no cenário 3
# ---------------------------------------------------------------------------


def run_scenario(
    label: str,
    initial_iop: float,
    num_steps: int,
    treatment_at: int = 0,
    seed_offset: int = 0,
) -> tuple:
    """
    Executa um cenário completo de simulação.

    Args:
        label (str): Nome do cenário para exibição.
        initial_iop (float): IOP inicial em mmHg.
        num_steps (int): Passos de simulação.
        treatment_at (int): Passo em que o tratamento é ativado (0 = nunca).
        seed_offset (int): Offset para diferenciar seeds entre cenários.

    Returns:
        tuple: (GlaucomaSimulator, RetinaSim)
    """
    import numpy as np
    np.random.seed(42 + seed_offset)

    retina = RetinaSim()
    sim = GlaucomaSimulator(retina, initial_iop=initial_iop)

    print(f"\n  [{label}] IOP inicial: {initial_iop:.1f} mmHg")

    for step in range(num_steps):
        result = sim.step()

        if treatment_at and step == treatment_at:
            sim.apply_treatment(effectiveness=0.85)
            print(f"  [{label}] Tratamento iniciado no passo {step}  (IOP: {sim.current_iop:.1f} mmHg)")

        if (step + 1) % LOG_INTERVAL == 0:
            print(
                f"  [{label}] Step {step + 1}: "
                f"IOP={result['iop']:.1f} mmHg | "
                f"Vivas={result['total_alive_cells']:,} | "
                f"Mortalidade={result['mortality_rate']:.2%}"
            )

    return sim, retina


def main():
    """Função principal do projeto."""

    print_banner("SIMULADOR DE RETINA 3D COM GLAUCOMA")

    config = get_config()
    results_dir = config["directories"]["results"]
    create_directories_if_not_exist([results_dir])

    # ========================================================================
    # 1. CONFIGURAÇÃO
    # ========================================================================
    print("\n1. Configuração carregada")
    print(f"   Total de células por simulação: {config['retina']['total_cells']:,}")
    print(f"   Passos por simulação: {NUM_STEPS}")

    # ========================================================================
    # 2. EXECUTAR OS 3 CENÁRIOS
    # ========================================================================
    print(f"\n2. Executando simulações ({NUM_STEPS} passos cada)...")

    sim_normal, retina_normal = run_scenario(
        label=SCENARIO_NORMAL["label"],
        initial_iop=SCENARIO_NORMAL["initial_iop"],
        num_steps=NUM_STEPS,
        seed_offset=0,
    )

    sim_glaucoma, retina_glaucoma = run_scenario(
        label=SCENARIO_GLAUCOMA["label"],
        initial_iop=SCENARIO_GLAUCOMA["initial_iop"],
        num_steps=NUM_STEPS,
        seed_offset=1,
    )

    sim_treated, retina_treated = run_scenario(
        label="Glaucoma + Tratamento",
        initial_iop=SCENARIO_GLAUCOMA["initial_iop"],
        num_steps=NUM_STEPS,
        treatment_at=TREATMENT_STEP,
        seed_offset=2,
    )

    # ========================================================================
    # 3. SUMÁRIO COMPARATIVO
    # ========================================================================
    print("\n3. Sumário Comparativo")
    print(f"   {'Cenário':<30} {'IOP Final':>10} {'Mortalidade':>12} {'Saúde Média':>12}")
    print(f"   {'-'*30} {'-'*10} {'-'*12} {'-'*12}")

    for label, sim in [
        (SCENARIO_NORMAL["label"], sim_normal),
        (SCENARIO_GLAUCOMA["label"], sim_glaucoma),
        ("Glaucoma + Tratamento", sim_treated),
    ]:
        s = sim.get_summary()
        print(
            f"   {label:<30} "
            f"{s['final_iop']:>9.1f}  "
            f"{s['final_mortality_rate']:>11.2%}  "
            f"{s['final_average_health']:>11.2%}"
        )

    # ========================================================================
    # 4. MODELO DE IA
    # ========================================================================
    print("\n4. Modelo de IA...")

    if TENSORFLOW_AVAILABLE:
        try:
            predictor = GlaucomaPredictor()
            predictor.config.epochs = 10
            predictor.train(use_synthetic=True)
            model_path = os.path.join(config["directories"]["models"], "glaucoma_model.keras")
            predictor.save_model(model_path)
            print(f"   ✓ Modelo treinado e salvo em models/")
        except Exception as e:
            print(f"   ⚠ Erro no treino: {e} — usando SimplePredictor")
            predictor = SimplePredictor()
    else:
        predictor = SimplePredictor()

    print("\n   Predições para IOP final de cada cenário:")
    print(f"\n   {'Cenário':<30} {'IOP':>6} {'Progressão':>12} {'Vitalidade':>12} {'Risco':>8}")
    print(f"   {'-'*30} {'-'*6} {'-'*12} {'-'*12} {'-'*8}")
    for label, sim in [
        (SCENARIO_NORMAL["label"], sim_normal),
        (SCENARIO_GLAUCOMA["label"], sim_glaucoma),
        ("Glaucoma + Tratamento", sim_treated),
    ]:
        s = sim.get_summary()
        iop = s["final_iop"]
        mort = s["final_mortality_rate"]
        pred = predictor.predict_from_iop(iop, mort) if hasattr(predictor, "predict_from_iop") else {}
        if pred:
            print(
                f"   {label:<30} {iop:>5.1f}  "
                f"{pred['glaucoma_progression']:>11.1%}  "
                f"{pred['cell_vitality']:>11.1%}  "
                f"{pred['risk_level']:>7.1%}"
            )

    # ========================================================================
    # 5. VISUALIZAÇÕES
    # ========================================================================
    print("\n5. Gerando visualizações...")

    visualizer = RetinaVisualizer()
    saved = []

    simulators = [sim_normal, sim_glaucoma, sim_treated]
    retinas = [retina_normal, retina_glaucoma, retina_treated]
    labels = [SCENARIO_NORMAL["label"], SCENARIO_GLAUCOMA["label"], "Glaucoma + Tratamento"]

    def save(fig, name):
        if fig:
            path = os.path.join(results_dir, name)
            visualizer.save_figure(fig, path)
            saved.append(name)

    save(visualizer.plot_comparison_scenarios(simulators, labels), "comparison_iop_mortality.png")
    save(visualizer.plot_cell_survival_comparison(simulators, retinas, labels), "comparison_cell_survival.png")
    save(visualizer.plot_retina_3d(retina_glaucoma, title="Retina 3D — Glaucoma Moderado"), "retina_3d_glaucoma.png")
    save(visualizer.plot_retina_3d(retina_treated, title="Retina 3D — Com Tratamento"), "retina_3d_treated.png")
    save(visualizer.plot_timeline(sim_glaucoma, show_metrics=["iop", "mortality_rate"],
                                  title="Evolução — Glaucoma Sem Tratamento"), "timeline_glaucoma.png")
    save(visualizer.plot_timeline(sim_treated, show_metrics=["iop", "mortality_rate"],
                                  title="Evolução — Glaucoma Com Tratamento"), "timeline_treated.png")
    save(visualizer.plot_cell_type_distribution(retina_glaucoma), "cell_distribution_glaucoma.png")

    print(f"\n   {len(saved)} gráfico(s) salvos em results/")

    # ========================================================================
    # 6. SALVAR RESULTADOS JSON
    # ========================================================================
    print("\n6. Salvando resultados JSON...")
    for label, sim in zip(labels, simulators):
        filename = label.lower().replace(" ", "_").replace("+", "com") + ".json"
        save_simulation_results(sim.get_summary(), os.path.join(results_dir, filename))

    # ========================================================================
    # CONCLUSÃO
    # ========================================================================
    print_banner("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    print("\nGráficos gerados em results/:")
    for name in saved:
        print(f"  📊 {name}")

    print("\nPróximos passos:")
    print("  → Abrir notebooks/02_comparativo_tratamento.ipynb para análise interativa")
    print("  → Ajustar NUM_STEPS e TREATMENT_STEP no topo de main.py")
    print("  → Aumentar EPOCHS em ai_model.py para treino mais profundo")


if __name__ == "__main__":
    main()
