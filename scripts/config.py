"""
Módulo de Configuração Global do Projeto.

Este módulo centraliza todos os parâmetros globais utilizados nas simulações
de retina 3D com glaucoma, incluindo dimensões, propriedades físicas e
parâmetros de simulação.
"""

import os
from typing import Dict, Any

# Suprimir warnings verbosos do TensorFlow (oneDNN)
os.environ.setdefault("TF_ENABLE_ONEDNN_OPTS", "0")
os.environ.setdefault("TF_CPP_MIN_LOG_LEVEL", "2")

# ============================================================================
# PARÂMETROS DE GEOMETRIA DA RETINA
# ============================================================================

# Dimensões da retina simulada (em unidades virtuais)
RETINA_WIDTH: int = 100  # Largura da retina
RETINA_HEIGHT: int = 100  # Altura da retina
RETINA_DEPTH: int = 50  # Profundidade (espessura) da retina

# Número total de células na simulação
TOTAL_CELLS: int = 10000  # Quantidade de células fotorreceptoras

# Tipos de células presentes na retina simulada
CELL_TYPES: Dict[str, int] = {
    "photoreceptor": 0.4,  # 40% de fotorreceptores
    "bipolar": 0.3,  # 30% de células bipolares
    "ganglion": 0.2,  # 20% de células ganglionares
    "glial": 0.1,  # 10% de células gliais
}

# ============================================================================
# PARÂMETROS FÍSICOS E FISIOLÓGICOS
# ============================================================================

# Pressão Intraocular (IOP - Intraocular Pressure)
INITIAL_IOP: float = 15.0  # Pressão inicial em mmHg (normal: 10-21)
NORMAL_IOP_RANGE: tuple = (10.0, 21.0)  # Faixa de pressão normal
GLAUCOMATOUS_IOP_THRESHOLD: float = 21.0  # Limite para pressão elevada

# Taxa de perda celular sob diferentes pressões
CELL_DEATH_RATE_NORMAL: float = 0.0002       # Taxa normal de apoptose (~4% em 200 passos)
CELL_DEATH_RATE_ELEVATED_IOP: float = 0.005  # Taxa elevada — IOP 21-30 mmHg (~39% em 100 passos)
CELL_DEATH_RATE_SEVERE: float = 0.02          # Taxa severa — IOP >30 mmHg (~86% em 100 passos)

# Limiar de pressão para dano celular acelerado
PRESSURE_DAMAGE_THRESHOLD: float = 30.0  # mmHg

# ============================================================================
# CENÁRIOS PREDEFINIDOS DE SIMULAÇÃO
# ============================================================================

# Paciente saudável (IOP normal)
SCENARIO_NORMAL: Dict[str, float] = {
    "initial_iop": 15.0,
    "label": "Paciente Saudável",
    "description": "IOP normal (15 mmHg), sem glaucoma",
}

# Paciente com glaucoma moderado
SCENARIO_GLAUCOMA: Dict[str, float] = {
    "initial_iop": 28.0,
    "label": "Glaucoma Moderado",
    "description": "IOP elevada (28 mmHg), sem tratamento",
}

# Paciente com glaucoma severo
SCENARIO_SEVERE: Dict[str, float] = {
    "initial_iop": 38.0,
    "label": "Glaucoma Severo",
    "description": "IOP muito elevada (38 mmHg), dano acelerado",
}

# ============================================================================
# PARÂMETROS DE SIMULAÇÃO
# ============================================================================

# Configurações temporais
TIME_STEPS: int = 200   # Número de passos padrão para demo
DELTA_TIME: float = 0.1  # Intervalo de tempo entre passos (em unidades virtuais)
SIMULATION_DURATION: float = TIME_STEPS * DELTA_TIME  # Duração total

# Perturbações e variabilidade
NOISE_LEVEL: float = 0.05  # Nível de ruído nas leituras de pressão
CELL_MIGRATION_RATE: float = 0.01  # Taxa de migração celular

# Regeneração e recuperação
CELL_REGENERATION_RATE: float = 0.001  # Taxa de regeneração celular
RECOVERY_WITH_TREATMENT: float = 1.5  # Fator de recuperação com tratamento

# ============================================================================
# PARÂMETROS DE IA E TREINAMENTO
# ============================================================================

# Configurações de rede neural
MODEL_INPUT_SIZE: int = 20  # Dimensionalidade da entrada
MODEL_HIDDEN_LAYERS: list = [64, 32, 16]  # Camadas ocultas
MODEL_OUTPUT_SIZE: int = 3  # Saída: [progresso glaucoma, vitalidade, risco]

# Treinamento
TRAIN_TEST_SPLIT: float = 0.8  # Proporção treino/teste
BATCH_SIZE: int = 32
LEARNING_RATE: float = 0.001
EPOCHS: int = 100

# ============================================================================
# PARÂMETROS DE VISUALIZAÇÃO
# ============================================================================

FIGURE_DPI: int = 100  # Resolução de figuras
FIGURE_SIZE: tuple = (12, 8)  # Tamanho padrão de figuras

# Mapa de cores para visualização
COLORMAP_RETINA: str = "viridis"  # Colormap para retina 3D
COLORMAP_DAMAGE: str = "hot"  # Colormap para mapa de dano

# ============================================================================
# DIRETÓRIOS
# ============================================================================

PROJECT_ROOT: str = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR: str = os.path.join(PROJECT_ROOT, "data")
RESULTS_DIR: str = os.path.join(PROJECT_ROOT, "results")
MODELS_DIR: str = os.path.join(PROJECT_ROOT, "models")
NOTEBOOKS_DIR: str = os.path.join(PROJECT_ROOT, "notebooks")

# ============================================================================
# UTILITY FUNCTION
# ============================================================================


def get_config() -> Dict[str, Any]:
    """
    Retorna um dicionário com todas as configurações do projeto.
    
    Returns:
        Dict[str, Any]: Dicionário contendo todos os parâmetros de configuração.
    """
    return {
        "retina": {
            "width": RETINA_WIDTH,
            "height": RETINA_HEIGHT,
            "depth": RETINA_DEPTH,
            "total_cells": TOTAL_CELLS,
            "cell_types": CELL_TYPES,
        },
        "physics": {
            "initial_iop": INITIAL_IOP,
            "normal_iop_range": NORMAL_IOP_RANGE,
            "glaucomatous_threshold": GLAUCOMATOUS_IOP_THRESHOLD,
            "cell_death_rates": {
                "normal": CELL_DEATH_RATE_NORMAL,
                "elevated": CELL_DEATH_RATE_ELEVATED_IOP,
                "severe": CELL_DEATH_RATE_SEVERE,
            },
            "pressure_damage_threshold": PRESSURE_DAMAGE_THRESHOLD,
        },
        "simulation": {
            "time_steps": TIME_STEPS,
            "delta_time": DELTA_TIME,
            "duration": SIMULATION_DURATION,
            "noise_level": NOISE_LEVEL,
            "cell_migration_rate": CELL_MIGRATION_RATE,
            "regeneration_rate": CELL_REGENERATION_RATE,
        },
        "model": {
            "input_size": MODEL_INPUT_SIZE,
            "hidden_layers": MODEL_HIDDEN_LAYERS,
            "output_size": MODEL_OUTPUT_SIZE,
        },
        "directories": {
            "project_root": PROJECT_ROOT,
            "data": DATA_DIR,
            "results": RESULTS_DIR,
            "models": MODELS_DIR,
        },
    }


if __name__ == "__main__":
    # Teste da configuração
    config = get_config()
    print("Configuração do Projeto Carregada com Sucesso!")
    print(f"Total de células: {config['retina']['total_cells']}")
    print(f"Pressão inicial: {config['physics']['initial_iop']} mmHg")
