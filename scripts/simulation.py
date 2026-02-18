"""
Módulo de Simulação de Glaucoma.

Este módulo implementa a simulação da progressão do glaucoma, incluindo
variações de pressão intraocular (IOP) e morte celular resultante.
"""

import numpy as np
from typing import List, Tuple, Dict, Optional
from scripts.config import (
    INITIAL_IOP,
    NORMAL_IOP_RANGE,
    GLAUCOMATOUS_IOP_THRESHOLD,
    PRESSURE_DAMAGE_THRESHOLD,
    CELL_DEATH_RATE_NORMAL,
    CELL_DEATH_RATE_ELEVATED_IOP,
    CELL_DEATH_RATE_SEVERE,
    CELL_MIGRATION_RATE,
    NOISE_LEVEL,
)
from scripts.retina import RetinaSim


class GlaucomaSimulator:
    """
    Simulador de progressão do glaucoma na retina.
    
    Gerencia a simulação temporal da pressão intraocular, morte celular
    e deterioração da visão ao longo do tempo.
    """

    def __init__(
        self,
        retina: RetinaSim,
        initial_iop: float = INITIAL_IOP,
        simulation_step: int = 0,
    ):
        """
        Inicializa o simulador de glaucoma.
        
        Args:
            retina (RetinaSim): Instância da retina a ser simulada.
            initial_iop (float): Pressão intraocular inicial em mmHg.
            simulation_step (int): Passo inicial de simulação.
        """
        self.retina = retina
        self.current_iop = initial_iop
        self.simulation_step = simulation_step
        self.iop_history: List[float] = [initial_iop]
        self.mortality_history: List[float] = []
        self.treatment_active = False

    def _calculate_cell_death_rate(self, iop: float) -> float:
        """
        Calcula a taxa de morte celular baseada na pressão intraocular.
        
        Args:
            iop (float): Pressão intraocular atual em mmHg.
        
        Returns:
            float: Taxa de morte celular para este passo.
        """
        if iop <= NORMAL_IOP_RANGE[1]:
            # Pressão normal
            return CELL_DEATH_RATE_NORMAL
        elif iop < PRESSURE_DAMAGE_THRESHOLD:
            # Pressão elevada
            return CELL_DEATH_RATE_ELEVATED_IOP
        else:
            # Pressão severa
            return CELL_DEATH_RATE_SEVERE

    def simulate_iop_variation(self) -> float:
        """
        Simula a variação da pressão intraocular em um passo de tempo.
        
        A pressão varia através de:
        - Componente determinística: tendência geral,
        - Componente estocástica: ruído natural.
        
        Returns:
            float: Nova pressão intraocular.
        """
        # Ruído aleatório para simular flutuações naturais
        noise = np.random.normal(0, NOISE_LEVEL)

        # Mudança determinística (possível progressão do glaucoma)
        # Aumenta levemente a cada passo se sem tratamento
        if not self.treatment_active:
            deterministic_change = 0.05
        else:
            deterministic_change = -0.1  # Reduz com tratamento

        self.current_iop = max(5.0, self.current_iop + deterministic_change + noise)
        self.iop_history.append(self.current_iop)

        return self.current_iop

    def apply_pressure_damage(self) -> int:
        """
        Aplica dano às células baseado na pressão atual.
        
        Cells are randomly selected for damage based on:
        - Death rate calculated from current IOP,
        - Random selection to simulate stochastic cell death.
        
        Returns:
            int: Número de células mortas neste passo.
        """
        death_rate = self._calculate_cell_death_rate(self.current_iop)
        alive_cells = self.retina.get_alive_cells_count()

        # Calcula quantas células podem sofrer dano
        cells_at_risk = int(alive_cells * death_rate)

        # Seleciona células aleatoriamente para dano
        alive_cell_ids = [
            i for i, cell in enumerate(self.retina.cells) if cell.is_alive
        ]

        cells_killed = 0
        for _ in range(cells_at_risk):
            if alive_cell_ids:
                cell_id = np.random.choice(alive_cell_ids)
                alive_cell_ids.remove(cell_id)

                # Aplica dano incremental
                damage = np.random.uniform(0.1, 0.5)
                if self.retina.damage_cell(cell_id, damage):
                    cells_killed += 1

        return cells_killed

    def apply_treatment(self, effectiveness: float = 0.8) -> None:
        """
        Ativa tratamento médico para o glaucoma.
        
        Args:
            effectiveness (float): Efetividade do tratamento (0.0 a 1.0).
        """
        self.treatment_active = True
        # Reduz a pressão atual proportional à efetividade
        reduction = (self.current_iop - NORMAL_IOP_RANGE[1]) * effectiveness
        self.current_iop = max(INITIAL_IOP, self.current_iop - reduction)

    def stop_treatment(self) -> None:
        """Interrompe o tratamento medico."""
        self.treatment_active = False

    def step(self) -> Dict[str, any]:
        """
        Executa um passo de simulação.
        
        Realiza:
        1. Variação da pressão intraocular,
        2. Aplicação de dano às células,
        3. Atualização de estatísticas.
        
        Returns:
            Dict[str, any]: Dicionário com dados do passo simulado.
        """
        # Simula variação de pressão
        new_iop = self.simulate_iop_variation()

        # Aplica dano
        cells_killed = self.apply_pressure_damage()

        # Registra mortalidade
        current_mortality = self.retina.get_dead_cells_count() / len(
            self.retina.cells
        )
        self.mortality_history.append(current_mortality)

        self.simulation_step += 1

        return {
            "step": self.simulation_step,
            "iop": self.current_iop,
            "cells_killed_this_step": cells_killed,
            "total_alive_cells": self.retina.get_alive_cells_count(),
            "total_dead_cells": self.retina.get_dead_cells_count(),
            "mortality_rate": current_mortality,
            "average_health": self.retina.get_average_health(),
        }

    def run_simulation(self, num_steps: int, log_interval: int = 100) -> List[Dict]:
        """
        Executa múltiplos passos de simulação.
        
        Args:
            num_steps (int): Número de passos a executar.
            log_interval (int): Intervalo para logging de resultados.
        
        Returns:
            List[Dict]: Lista de resultados para cada passo.
        """
        results = []

        for _ in range(num_steps):
            step_result = self.step()
            results.append(step_result)

            if (self.simulation_step % log_interval) == 0:
                print(
                    f"Step {self.simulation_step}: IOP={step_result['iop']:.1f} mmHg, "
                    f"Alive={step_result['total_alive_cells']}, "
                    f"Mortality={step_result['mortality_rate']:.2%}"
                )

        return results

    def get_summary(self) -> Dict[str, any]:
        """
        Retorna um sumário dos resultados da simulação.
        
        Returns:
            Dict[str, any]: Dicionário com resumo da simulação.
        """
        return {
            "total_steps": self.simulation_step,
            "final_iop": self.current_iop,
            "mean_iop": np.mean(self.iop_history),
            "max_iop": np.max(self.iop_history),
            "min_iop": np.min(self.iop_history),
            "treatment_active": self.treatment_active,
            "final_mortality_rate": (
                self.retina.get_dead_cells_count() / len(self.retina.cells)
            ),
            "final_average_health": self.retina.get_average_health(),
            "total_cells": len(self.retina.cells),
            "alive_cells": self.retina.get_alive_cells_count(),
            "dead_cells": self.retina.get_dead_cells_count(),
        }


if __name__ == "__main__":
    # Teste simples do simulador
    print("Inicializando simulação de glaucoma...")
    retina = RetinaSim()
    simulator = GlaucomaSimulator(retina)

    print("\nExecutando 50 passos de simulação...")
    results = simulator.run_simulation(num_steps=50, log_interval=10)

    print("\nResumo da Simulação:")
    summary = simulator.get_summary()
    for key, value in summary.items():
        print(f"  {key}: {value}")
