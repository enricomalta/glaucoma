"""
DIAGRAMA DE ARQUITETURA DO PROJETO
===================================

Visualização dos fluxos de dados e relações entre módulos
"""

ARCHITECTURE = """
┌─────────────────────────────────────────────────────────────────────────────┐
│                SIMULADOR DE RETINA 3D COM GLAUCOMA                         │
│                          ARQUITETURA DO PROJETO                             │
└─────────────────────────────────────────────────────────────────────────────┘


1. FLUXO PRINCIPAL DE EXECUÇÃO:
═════════════════════════════════════════════════════════════════════════════

    ┌──────────────────┐
    │   main.py        │ ◄─── Ponto de entrada do projeto
    │                  │
    │ 1. Load config   │
    │ 2. Create retina │
    │ 3. Run sim       │
    │ 4. Train AI      │
    │ 5. Visualize     │
    └────────┬─────────┘
             │
             ▼
    ┌────────────────────────────────────────────────────────────┐
    │                    MÓDULOS PRINCIPAIS                      │
    └────────────────────────────────────────────────────────────┘


2. FLUXO DE DADOS:
═════════════════════════════════════════════════════════════════════════════

    config.py                retina.py
    ├─ INITIAL_IOP      ──►  ├─ RetinaSim
    ├─ TOTAL_CELLS      ──►  ├─ Cell
    ├─ CELL_TYPES       ──►  └─ population
    └─ ...
         │
         │                   simulation.py
         ├─ IOP params  ──►  ├─ GlaucomaSimulator
         │                   ├─ pressure variation
         └─────────────────► └─ cell death logic
                                    │
                                    ▼
                            ┌──────────────┐
                            │  Results     │
                            ├──────────────┤
                            │ - IOP history
                            │ - Mortality  
                            │ - Cell health
                            └──────────────┘
                                    │
                    ┌───────────────┼───────────────┐
                    ▼               ▼               ▼
            ai_model.py      visualization.py    utils/
            ├─ Predictor  ──► ├─ 3D plots    ──► ├─ Save/Load
            └─ Predictions    ├─ Heatmaps        └─ Helpers
                              ├─ Timeline
                              └─ Charts


3. ESTRUTURA DE CLASSES:
═════════════════════════════════════════════════════════════════════════════

    ┌─────────────────────────────────────────────────────────┐
    │                      Cell (Dataclass)                   │
    ├─────────────────────────────────────────────────────────┤
    │ - cell_id: int          (identificador único)           │
    │ - cell_type: str        (tipo de célula)                │
    │ - x, y, z: float        (posição 3D)                    │
    │ - health: float (0-1)   (saúde da célula)              │
    │ - is_alive: bool        (viva ou morta)                 │
    └─────────────────────────────────────────────────────────┘
                              ▲
                              │ 10.000 instâncias
                              │
    ┌─────────────────────────────────────────────────────────┐
    │                    RetinaSim                            │
    ├─────────────────────────────────────────────────────────┤
    │ - width, height, depth: int                             │
    │ - cells: List[Cell]                                     │
    │                                                         │
    │ + get_cell_coordinates() → np.ndarray                   │
    │ + get_alive_cells_count() → int                         │
    │ + damage_cell(id, amount) → bool                        │
    │ + heal_cell(id, amount) → None                          │
    │ + get_statistics() → Dict                               │
    └─────────────────────────────────────────────────────────┘
                              ▲
                              │
    ┌─────────────────────────────────────────────────────────┐
    │                GlaucomaSimulator                        │
    ├─────────────────────────────────────────────────────────┤
    │ - retina: RetinaSim                                     │
    │ - current_iop: float                                    │
    │ - iop_history: List[float]                              │
    │ - treatment_active: bool                                │
    │                                                         │
    │ + simulate_iop_variation() → float                      │
    │ + apply_pressure_damage() → int                         │
    │ + apply_treatment(effectiveness) → None                │
    │ + step() → Dict                                         │
    │ + run_simulation(num_steps) → List[Dict]               │
    │ + get_summary() → Dict                                  │
    └─────────────────────────────────────────────────────────┘


4. PIPELINE DE DADOS:
═════════════════════════════════════════════════════════════════════════════

    Raw Configs          Generate           Simulate          Analyze
    ─────────────       ─────────────       ──────────        ────────
         │                   │                  │                │
         ├─ IOP           ┌─ Retina         ┌─ IOP ──┬── AI ─┬─ Predict
         ├─ Cell count    │ generations     │          │       │
         ├─ Physics       │ with Cell       │ + Death  │       │
         └─ ...           │ instances       │ + Heal   └──┬─── Viz ──┐
                          └─                └─            │          │
                                                          │      Output
                                                          │     Graphs
                                                   json data


5. FLUXO DE VISUALIZAÇÃO:
═════════════════════════════════════════════════════════════════════════════

    Retina + History Data
            │
            ├──► RetinaVisualizer.plot_retina_3d()
            │    └─► scatter plot 3D com cores de saúde
            │
            ├──► plot_health_heatmap_2d()
            │    └─► grid 2D com valores interpolados
            │
            ├──► plot_timeline()
            │    ├─► IOP vs Tempo
            │    └─► Mortalidade vs Tempo
            │
            ├──► plot_cell_type_distribution()
            │    └─► Bar chart vivas/mortas por tipo
            │
            └──► plot_iop_distribution()
                 └─► Histograma com média/mediana


6. DEPENDÊNCIAS DE MÓDULOS:
═════════════════════════════════════════════════════════════════════════════

    main.py
    ├─ scripts/config.py
    ├─ scripts/retina.py ◄─┐
    │                       ├─ scripts/config.py
    ├─ scripts/simulation.py ◄─┐
    │                         ├─ scripts/retina.py
    │                         ├─ scripts/config.py
    │
    ├─ scripts/ai_model.py ◄─── scripts/config.py (opt: tensorflow)
    │
    ├─ scripts/visualization.py
    │   ├─ scripts/config.py
    │   ├─ scripts/retina.py
    │   ├─ scripts/simulation.py
    │   └─ matplotlib
    │
    └─ utils/__init__.py


7. CICLO DE DESENVOLVIMENTO:
═════════════════════════════════════════════════════════════════════════════

    Modificar Config
         │
         ▼
    Run Simulation (main.py ou custom)
         │
         ▼
    Análise de Resultados
         │
         ├─ OK ──► Deploy/Publicar
         │
         └─ Ajustar ──► (retorna ao início)


8. TIPOS DE SAÚDA:
═════════════════════════════════════════════════════════════════════════════

    JSON Files:
        results/simulation_results.json
        └─ summary: timestamps, IOP, mortality, etc

    PNG/Image Files:
        results/retina_3d.png
        results/health_heatmap.png
        results/timeline.png
        results/cell_distribution.png
        results/iop_distribution.png

    Model Files:
        models/glaucoma_model.h5 (TensorFlow)
        models/*.pkl (Pickle/Joblib)

    Data Files:
        data/* (datasets de entrada)
        simulations/* (checkpoints)


9. INTEGRAÇÃO COM JUPYTER:
═════════════════════════════════════════════════════════════════════════════

    Jupyter Notebook
        │
        ├─ Import modules
        ├─ Execute cells
        ├─ Interactive plots
        └─ Export results


10. TESTE UNITÁRIO FLOW:
═════════════════════════════════════════════════════════════════════════════

    test_project.py
    ├─ TestRetinaSim
    │  ├─ test_retina_creation√
    │  ├─ test_coordinates√
    │  ├─ test_cell_damage√
    │  └─ test_statistics√
    │
    ├─ TestGlaucomaSimulator
    │  ├─ test_simulator_creation√
    │  ├─ test_simulation_step√
    │  ├─ test_treatment√
    │  └─ test_full_simulation√
    │
    ├─ TestAIModel
    │  └─ test_simple_predictor√
    │
    └─ TestConfig
       └─ test_config_loading√

═════════════════════════════════════════════════════════════════════════════
                        ✅ ARQUITETURA COMPLETA
═════════════════════════════════════════════════════════════════════════════
"""

print(ARCHITECTURE)

if __name__ == "__main__":
    import sys
    import os
    sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    
    print("\n✓ Arquitetura visualizada com sucesso!")
    print("\nPara entender melhor cada módulo:")
    print("  - config.py: help(get_config)")
    print("  - retina.py: help(RetinaSim)")
    print("  - simulation.py: help(GlaucomaSimulator)")
    print("  - ai_model.py: help(GlaucomaPredictor)")
    print("  - visualization.py: help(RetinaVisualizer)")
