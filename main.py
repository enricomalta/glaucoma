"""
Script Principal - Exemplo de uso completo do projeto.

Este script demonstra como usar os módulos do projeto para:
1. Criar uma retina simulada,
2. Executar simulação de glaucoma,
3. Treinar modelo de IA,
4. Visualizar resultados.
"""

import sys
import os

# Adiciona o diretório raiz ao path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from scripts.config import get_config
from scripts.retina import RetinaSim
from scripts.simulation import GlaucomaSimulator
from scripts.ai_model import GlaucomaPredictor, SimplePredictor, TENSORFLOW_AVAILABLE
from scripts.visualization import RetinaVisualizer
from utils import print_banner, save_simulation_results, create_directories_if_not_exist


def main():
    """Função principal do projeto."""
    
    print_banner("SIMULADOR DE RETINA 3D COM GLAUCOMA")
    
    # ========================================================================
    # 1. CARREGAR CONFIGURAÇÃO
    # ========================================================================
    print("\n1. Carregando configuração...")
    config = get_config()
    print(f"   ✓ Total de células: {config['retina']['total_cells']:,}")
    print(f"   ✓ Pressão inicial: {config['physics']['initial_iop']} mmHg")
    print(f"   ✓ Duração da simulação: {config['simulation']['duration']:.1f} unidades")

    # ========================================================================
    # 2. CRIAR RETINA SIMULADA
    # ========================================================================
    print("\n2. Criando retina simulada...")
    retina = RetinaSim(
        width=config["retina"]["width"],
        height=config["retina"]["height"],
        depth=config["retina"]["depth"],
        num_cells=config["retina"]["total_cells"],
    )
    print(f"   ✓ Retina criada: {retina}")
    
    # Estatísticas iniciais
    stats = retina.get_statistics()
    print(f"   ✓ Saúde média inicial: {stats['average_health']:.2%}")

    # ========================================================================
    # 3. EXECUTAR SIMULAÇÃO DE GLAUCOMA
    # ========================================================================
    print("\n3. Executando simulação de glaucoma...")
    simulator = GlaucomaSimulator(
        retina=retina,
        initial_iop=config["physics"]["initial_iop"],
    )

    # Simula 100 passos
    num_steps = 100
    results = simulator.run_simulation(num_steps=num_steps, log_interval=25)

    # Sumário
    summary = simulator.get_summary()
    print(f"\n   Sumário da Simulação:")
    print(f"   ✓ IOP final: {summary['final_iop']:.2f} mmHg")
    print(f"   ✓ Taxa de mortalidade final: {summary['final_mortality_rate']:.2%}")
    print(f"   ✓ Células vivas: {summary['alive_cells']}/{summary['total_cells']}")
    print(f"   ✓ Saúde média final: {summary['final_average_health']:.2%}")

    # ========================================================================
    # 4. TREINAR MODELO DE IA
    # ========================================================================
    print("\n4. Inicializando modelo de IA...")

    if TENSORFLOW_AVAILABLE:
        try:
            predictor = GlaucomaPredictor()
            print("   ✓ Modelo de rede neural criado")

            print("   Treinando modelo (epochs reduzido para demo)...")
            predictor.config.epochs = 5
            predictor.train(use_synthetic=True)
            print("   ✓ Treinamento concluído")

        except Exception as e:
            print(f"   ⚠ Erro no modelo neural: {e}")
            print("   Usando SimplePredictor como alternativa...")
            predictor = SimplePredictor()
    else:
        print("   ⚠ TensorFlow não encontrado. Usando SimplePredictor...")
        predictor = SimplePredictor()

        # Predição demonstrativa
        test_prediction = predictor.predict_from_iop(summary['final_iop'])
        print(f"   ✓ Predição para IOP {summary['final_iop']:.1f} mmHg:")
        for key, value in test_prediction.items():
            print(f"      - {key}: {value:.2%}")

    # ========================================================================
    # 5. VISUALIZAR RESULTADOS
    # ========================================================================
    print("\n5. Gerando visualizações...")
    
    try:
        visualizer = RetinaVisualizer()

        # Cria diretório de resultados
        results_dir = config["directories"]["results"]
        create_directories_if_not_exist([results_dir])

        # Gera gráficos
        print("   Gerando gráficos...")
        
        fig1 = visualizer.plot_retina_3d(retina, title="Retina 3D - Final da Simulação")
        if fig1:
            visualizer.save_figure(fig1, os.path.join(results_dir, "retina_3d.png"))
            print(f"   ✓ Salvo: retina_3d.png")

        fig2 = visualizer.plot_health_heatmap_2d(retina, title="Mapa de Saúde Celular")
        if fig2:
            visualizer.save_figure(fig2, os.path.join(results_dir, "health_heatmap.png"))
            print(f"   ✓ Salvo: health_heatmap.png")

        fig3 = visualizer.plot_timeline(simulator, show_metrics=["iop", "mortality_rate"])
        if fig3:
            visualizer.save_figure(fig3, os.path.join(results_dir, "timeline.png"))
            print(f"   ✓ Salvo: timeline.png")

        fig4 = visualizer.plot_cell_type_distribution(retina)
        if fig4:
            visualizer.save_figure(fig4, os.path.join(results_dir, "cell_distribution.png"))
            print(f"   ✓ Salvo: cell_distribution.png")

        fig5 = visualizer.plot_iop_distribution(simulator.iop_history)
        if fig5:
            visualizer.save_figure(fig5, os.path.join(results_dir, "iop_distribution.png"))
            print(f"   ✓ Salvo: iop_distribution.png")

    except ImportError:
        print("   ⚠ Matplotlib não disponível. Pulando visualizações...")

    # ========================================================================
    # 6. SALVAR RESULTADOS
    # ========================================================================
    print("\n6. Salvando resultados...")
    
    results_file = os.path.join(config["directories"]["results"], "simulation_results.json")
    save_simulation_results(summary, results_file, format="json")
    print(f"   ✓ Resultados salvos em: {results_file}")

    # ========================================================================
    # FINALIZAÇÃO
    # ========================================================================
    print_banner("SIMULAÇÃO CONCLUÍDA COM SUCESSO!")
    
    print("\nArtefatos gerados:")
    print(f"  📊 Gráficos: {config['directories']['results']}/")
    print(f"  📄 Dados: {config['directories']['data']}/")
    print(f"  🤖 Modelos: {config['directories']['models']}/")
    
    print("\nPróximos passos:")
    print("  1. Verificar os gráficos gerados em results/")
    print("  2. Analisar dados da simulação")
    print("  3. Ajustar parâmetros em scripts/config.py")
    print("  4. Treinar modelo com dados reais")


if __name__ == "__main__":
    main()
