"""
Módulo de Utilitários e Helpers.

Contém funções auxiliares reutilizáveis para o projeto.
"""

import os
from typing import Dict, Any
import json


def create_directories_if_not_exist(paths: list) -> None:
    """
    Cria diretórios se não existirem.
    
    Args:
        paths (list): Lista de caminhos de diretórios a criar.
    """
    for path in paths:
        if not os.path.exists(path):
            os.makedirs(path, exist_ok=True)
            print(f"Diretório criado: {path}")


def save_simulation_results(
    results: Dict[str, Any], filepath: str, format: str = "json"
) -> None:
    """
    Salva resultados de simulação em arquivo.
    
    Args:
        results (Dict[str, Any]): Dicionário com resultados.
        filepath (str): Caminho para salvar.
        format (str): Formato do arquivo ('json' ou 'txt').
    """
    os.makedirs(os.path.dirname(filepath) or ".", exist_ok=True)

    if format == "json":
        with open(filepath, "w") as f:
            json.dump(results, f, indent=4)
    else:
        with open(filepath, "w") as f:
            for key, value in results.items():
                f.write(f"{key}: {value}\n")

    print(f"Resultados salvos em: {filepath}")


def load_simulation_results(filepath: str) -> Dict[str, Any]:
    """
    Carrega resultados de simulação de arquivo.
    
    Args:
        filepath (str): Caminho do arquivo com resultados.
    
    Returns:
        Dict[str, Any]: Dicionário com resultados carregados.
    """
    try:
        with open(filepath, "r") as f:
            return json.load(f)
    except Exception as e:
        print(f"Erro ao carregar resultados: {e}")
        return {}


def print_banner(text: str, char: str = "=") -> None:
    """
    Imprime um banner com texto.
    
    Args:
        text (str): Texto a exibir.
        char (str): Caractere para border.
    """
    width = len(text) + 4
    print(char * width)
    print(f"  {text}  ")
    print(char * width)
