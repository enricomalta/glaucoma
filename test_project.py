"""
Testes e Validação do Projeto.

Este módulo contém testes unitários para validar a funcionalidade
dos componentes principais do projeto.
"""

import sys
import os
import numpy as np

# Adicionar raiz ao path
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from scripts.config import get_config, TOTAL_CELLS
from scripts.retina import RetinaSim, Cell
from scripts.simulation import GlaucomaSimulator
from scripts.ai_model import SimplePredictor


class TestRetinaSim:
    """Testes para a classe RetinaSim."""

    @staticmethod
    def test_retina_creation():
        """Testa criação básica da retina."""
        print("Teste 1: Criação de retina...")
        retina = RetinaSim()

        assert len(retina.cells) == TOTAL_CELLS, "Número de células incorreto"
        assert retina.get_alive_cells_count() == TOTAL_CELLS, "Todas as células devem estar vivas inicialmente"
        assert retina.get_average_health() == 1.0, "Saúde inicial deve ser 1.0"

        print("  ✓ Criação de retina OK")

    @staticmethod
    def test_retina_coordinates():
        """Testa que coordenadas estão dentro dos limites."""
        print("Teste 2: Limites de coordenadas...")
        retina = RetinaSim()

        for cell in retina.cells:
            assert 0 <= cell.x <= retina.width, f"X fora dos limites: {cell.x}"
            assert 0 <= cell.y <= retina.height, f"Y fora dos limites: {cell.y}"
            assert 0 <= cell.z <= retina.depth, f"Z fora dos limites: {cell.z}"

        print("  ✓ Coordenadas OK")

    @staticmethod
    def test_cell_damage():
        """Testa sistema de dano celular."""
        print("Teste 3: Sistema de dano celular...")
        retina = RetinaSim()

        # Danificar a primeira célula
        initial_health = retina.cells[0].health
        retina.damage_cell(0, 0.5)

        assert retina.cells[0].health == initial_health - 0.5, "Dano não aplicado corretamente"
        assert retina.cells[0].is_alive, "Célula não deveria estar morta ainda"

        # Danificar ainda mais até matar
        retina.damage_cell(0, 0.6)
        assert not retina.cells[0].is_alive, "Célula deveria estar morta"

        print("  ✓ Dano celular OK")

    @staticmethod
    def test_statistics():
        """Testa função de estatísticas."""
        print("Teste 4: Estatísticas...")
        retina = RetinaSim()

        stats = retina.get_statistics()

        assert stats["total_cells"] == TOTAL_CELLS, "Total de células incorreto"
        assert stats["alive_cells"] == TOTAL_CELLS, "Vivas incorreto"
        assert stats["dead_cells"] == 0, "Mortas deveria ser 0"
        assert stats["mortality_rate"] == 0.0, "Taxa de mortalidade deveria ser 0"
        assert 0 <= stats["average_health"] <= 1.0, "Saúde média inválida"

        print("  ✓ Estatísticas OK")


class TestGlaucomaSimulator:
    """Testes para a classe GlaucomaSimulator."""

    @staticmethod
    def test_simulator_creation():
        """Testa criação do simulador."""
        print("Teste 5: Criação do simulador...")
        retina = RetinaSim()
        simulator = GlaucomaSimulator(retina)

        assert simulator.current_iop > 0, "IOP deve ser positivo"
        assert len(simulator.iop_history) > 0, "Histórico deve ter pelo menos um valor"

        print("  ✓ Criação do simulador OK")

    @staticmethod
    def test_simulation_step():
        """Testa um passo de simulação."""
        print("Teste 6: Passo de simulação...")
        retina = RetinaSim()
        simulator = GlaucomaSimulator(retina)

        initial_alive = retina.get_alive_cells_count()
        result = simulator.step()

        assert "step" in result, "Resultado deve conter 'step'"
        assert "iop" in result, "Resultado deve conter 'iop'"
        assert result["total_alive_cells"] <= initial_alive, "Não deveria haver mais células vivas"

        print("  ✓ Passo de simulação OK")

    @staticmethod
    def test_treatment():
        """Testa sistema de tratamento."""
        print("Teste 7: Sistema de tratamento...")
        retina = RetinaSim()
        simulator = GlaucomaSimulator(retina, initial_iop=35.0)

        iop_before = simulator.current_iop
        simulator.apply_treatment(effectiveness=0.8)

        assert simulator.treatment_active, "Tratamento deveria estar ativo"
        assert simulator.current_iop < iop_before, "IOP deveria diminuir com tratamento"

        print("  ✓ Sistema de tratamento OK")

    @staticmethod
    def test_full_simulation():
        """Testa simulação completa."""
        print("Teste 8: Simulação completa (50 passos)...")
        retina = RetinaSim()
        simulator = GlaucomaSimulator(retina)

        results = simulator.run_simulation(num_steps=50, log_interval=100)

        assert len(results) == 50, "Deveria ter 50 resultados"
        assert len(simulator.iop_history) > 50, "Histórico deveria ter mais de 50 entradas"
        assert len(simulator.mortality_history) == 50, "Histórico de mortalidade deveria ter 50 entradas"

        summary = simulator.get_summary()
        assert summary["total_steps"] == 50, "Total de passos incorreto"

        print("  ✓ Simulação completa OK")


class TestAIModel:
    """Testes para modelos de IA."""

    @staticmethod
    def test_simple_predictor():
        """Testa preditor simples."""
        print("Teste 9: Preditor simples...")
        predictor = SimplePredictor()

        # Testar com IOP normal
        pred_normal = predictor.predict_from_iop(15.0)
        assert pred_normal["glaucoma_progression"] < 0.5, "Progressão deveria ser baixa para IOP normal"

        # Testar com IOP elevada
        pred_elevated = predictor.predict_from_iop(40.0)
        assert pred_elevated["glaucoma_progression"] > 0.5, "Progressão deveria ser alta para IOP elevada"

        # Verificar que todos os valores estão em [0, 1]
        for key, value in pred_normal.items():
            assert 0 <= value <= 1, f"{key} fora do intervalo [0, 1]"

        print("  ✓ Preditor simples OK")


class TestConfig:
    """Testes para configuração."""

    @staticmethod
    def test_config_loading():
        """Testa carregamento de configuração."""
        print("Teste 10: Carregamento de configuração...")
        config = get_config()

        assert "retina" in config, "Config deveria conter 'retina'"
        assert "physics" in config, "Config deveria conter 'physics'"
        assert "simulation" in config, "Config deveria conter 'simulation'"
        assert "model" in config, "Config deveria conter 'model'"
        assert "directories" in config, "Config deveria conter 'directories'"

        # Validar valores específicos
        assert config["retina"]["total_cells"] > 0, "Total de células deve ser positivo"
        assert config["physics"]["initial_iop"] > 0, "IOP deve ser positivo"

        print("  ✓ Carregamento de configuração OK")


def run_all_tests():
    """Executa todos os testes."""
    print("\n" + "=" * 60)
    print("EXECUTANDO SUITE DE TESTES DO PROJETO GLAUCOMA")
    print("=" * 60 + "\n")

    tests = [
        TestRetinaSim,
        TestGlaucomaSimulator,
        TestAIModel,
        TestConfig,
    ]

    total_tests = 0
    passed_tests = 0

    for test_class in tests:
        methods = [method for method in dir(test_class) if method.startswith("test_")]

        for method_name in methods:
            total_tests += 1
            try:
                method = getattr(test_class, method_name)
                method()
                passed_tests += 1
            except AssertionError as e:
                print(f"  ✗ FALHOU: {e}")
            except Exception as e:
                print(f"  ✗ ERRO: {e}")

    print("\n" + "=" * 60)
    print(f"RESULTADOS: {passed_tests}/{total_tests} testes passaram")
    print("=" * 60)

    if passed_tests == total_tests:
        print("✓ TODOS OS TESTES PASSARAM!")
        return True
    else:
        print("✗ ALGUNS TESTES FALHARAM!")
        return False


if __name__ == "__main__":
    success = run_all_tests()
    sys.exit(0 if success else 1)
