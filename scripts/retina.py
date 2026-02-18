"""
Módulo de Geração de Retina 3D Simulada.

Este módulo fornece ferramentas para gerar uma representação 3D simulada
da retina com células fotorreceptoras e outras estruturas, incluindo
propriedades de saúde e localização.
"""

import numpy as np
from typing import Tuple, List, Dict, Optional
from dataclasses import dataclass
from scripts.config import (
    RETINA_WIDTH,
    RETINA_HEIGHT,
    RETINA_DEPTH,
    TOTAL_CELLS,
    CELL_TYPES,
)


@dataclass
class Cell:
    """
    Representa uma célula individual na retina.
    
    Attributes:
        cell_id (int): Identificador único da célula.
        cell_type (str): Tipo de célula (photoreceptor, bipolar, ganglion, glial).
        x (float): Coordenada X (0 a RETINA_WIDTH).
        y (float): Coordenada Y (0 a RETINA_HEIGHT).
        z (float): Coordenada Z (profundidade, 0 a RETINA_DEPTH).
        health (float): Saúde da célula (0.0 a 1.0, onde 1.0 é saudável).
        is_alive (bool): Indica se a célula está viva.
    """

    cell_id: int
    cell_type: str
    x: float
    y: float
    z: float
    health: float = 1.0
    is_alive: bool = True

    def __str__(self) -> str:
        """Representação em string da célula."""
        return f"Cell(id={self.cell_id}, type={self.cell_type}, pos=({self.x:.1f}, {self.y:.1f}, {self.z:.1f}), health={self.health:.2f})"


class RetinaSim:
    """
    Classe para simular e gerenciar uma retina 3D.
    
    Esta classe implementa a geração, armazenamento e manipulação de uma
    população de células que representam a estrutura da retina humana.
    """

    def __init__(
        self,
        width: int = RETINA_WIDTH,
        height: int = RETINA_HEIGHT,
        depth: int = RETINA_DEPTH,
        num_cells: int = TOTAL_CELLS,
        cell_distribution: Optional[Dict[str, float]] = None,
    ):
        """
        Inicializa a simulação da retina.
        
        Args:
            width (int): Largura da retina.
            height (int): Altura da retina.
            depth (int): Profundidade (espessura) da retina.
            num_cells (int): Número total de células.
            cell_distribution (Optional[Dict[str, float]]): Distribuição de tipos
                de células. Se None, usa CELL_TYPES.
        """
        self.width = width
        self.height = height
        self.depth = depth
        self.num_cells = num_cells
        self.cells: List[Cell] = []
        self.cell_distribution = cell_distribution or CELL_TYPES

        # Gera as células iniciais
        self._generate_cells()

    def _generate_cells(self) -> None:
        """
        Gera as células iniciais da retina com distribuição espacial aleatória.
        
        Distribuição:
        - Células são colocadas aleatoriamente no espaço 3D da retina.
        - A distribuição de tipos segue CELL_TYPES.
        - Todas as células iniciam com health = 1.0 e is_alive = True.
        """
        np.random.seed(42)  # Para reprodutibilidade

        cell_id = 0
        for cell_type, proportion in self.cell_distribution.items():
            num_of_type = int(self.num_cells * proportion)

            for _ in range(num_of_type):
                x = np.random.uniform(0, self.width)
                y = np.random.uniform(0, self.height)
                z = np.random.uniform(0, self.depth)

                cell = Cell(
                    cell_id=cell_id,
                    cell_type=cell_type,
                    x=x,
                    y=y,
                    z=z,
                    health=1.0,
                    is_alive=True,
                )
                self.cells.append(cell)
                cell_id += 1

    def get_cell_coordinates(self) -> np.ndarray:
        """
        Retorna matriz de coordenadas de todas as células vivas.
        
        Returns:
            np.ndarray: Matriz de forma (num_live_cells, 3) com coordenadas (x, y, z).
        """
        coords = np.array(
            [(cell.x, cell.y, cell.z) for cell in self.cells if cell.is_alive]
        )
        return coords

    def get_cell_health(self) -> np.ndarray:
        """
        Retorna vetor de saúde de todas as células vivas.
        
        Returns:
            np.ndarray: Vetor de saúde das células.
        """
        health = np.array([cell.health for cell in self.cells if cell.is_alive])
        return health

    def get_alive_cells_count(self) -> int:
        """
        Retorna o número de células vivas.
        
        Returns:
            int: Quantidade de células vivas.
        """
        return sum(1 for cell in self.cells if cell.is_alive)

    def get_dead_cells_count(self) -> int:
        """
        Retorna o número de células mortas.
        
        Returns:
            int: Quantidade de células mortas.
        """
        return sum(1 for cell in self.cells if not cell.is_alive)

    def get_average_health(self) -> float:
        """
        Retorna a saúde média de todas as células vivas.
        
        Returns:
            float: Saúde média (0.0 a 1.0).
        """
        alive_cells = [cell for cell in self.cells if cell.is_alive]
        if not alive_cells:
            return 0.0
        return sum(cell.health for cell in alive_cells) / len(alive_cells)

    def damage_cell(self, cell_id: int, damage_amount: float) -> bool:
        """
        Aplica dano a uma célula específica.
        
        Args:
            cell_id (int): ID da célula a ser danificada.
            damage_amount (float): Quantidade de dano (0.0 a 1.0).
        
        Returns:
            bool: True se a célula morreu, False caso contrário.
        """
        if 0 <= cell_id < len(self.cells):
            cell = self.cells[cell_id]
            cell.health = max(0.0, cell.health - damage_amount)

            if cell.health <= 0.0 and cell.is_alive:
                cell.is_alive = False
                return True
        return False

    def heal_cell(self, cell_id: int, heal_amount: float) -> None:
        """
        Cura uma célula, aumentando sua saúde.
        
        Args:
            cell_id (int): ID da célula a ser curada.
            heal_amount (float): Quantidade de cura (0.0 a 1.0).
        """
        if 0 <= cell_id < len(self.cells):
            cell = self.cells[cell_id]
            cell.health = min(1.0, cell.health + heal_amount)

    def get_cells_by_type(self, cell_type: str) -> List[Cell]:
        """
        Retorna todas as células de um tipo específico.
        
        Args:
            cell_type (str): Tipo de célula a filtrar.
        
        Returns:
            List[Cell]: Lista de células do tipo especificado.
        """
        return [cell for cell in self.cells if cell.cell_type == cell_type]

    def get_statistics(self) -> Dict[str, any]:
        """
        Retorna estatísticas gerais da retina.
        
        Returns:
            Dict[str, any]: Dicionário com estatísticas desagregadas.
        """
        total_cells = len(self.cells)
        alive_cells = self.get_alive_cells_count()
        dead_cells = self.get_dead_cells_count()
        avg_health = self.get_average_health()

        type_stats = {}
        for cell_type in self.cell_distribution.keys():
            cells_of_type = self.get_cells_by_type(cell_type)
            alive = sum(1 for c in cells_of_type if c.is_alive)
            type_stats[cell_type] = {
                "total": len(cells_of_type),
                "alive": alive,
                "dead": len(cells_of_type) - alive,
            }

        return {
            "total_cells": total_cells,
            "alive_cells": alive_cells,
            "dead_cells": dead_cells,
            "mortality_rate": dead_cells / total_cells if total_cells > 0 else 0,
            "average_health": avg_health,
            "by_type": type_stats,
        }

    def __repr__(self) -> str:
        """Representação em string da retina."""
        return (
            f"RetinaSim(width={self.width}, height={self.height}, depth={self.depth}, "
            f"num_cells={len(self.cells)}, alive={self.get_alive_cells_count()})"
        )


if __name__ == "__main__":
    # Teste simples da classe RetinaSim
    print("Inicializando retina simulada...")
    retina = RetinaSim()

    print(f"\n{retina}")
    print(f"Saúde média: {retina.get_average_health():.2%}")

    print("\nEstatísticas:")
    stats = retina.get_statistics()
    for key, value in stats.items():
        if key != "by_type":
            print(f"  {key}: {value}")

    print("\nPor tipo de célula:")
    for cell_type, type_stat in stats["by_type"].items():
        print(f"  {cell_type}: {type_stat}")
