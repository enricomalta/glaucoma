"""
Módulo de Visualização de Retina 3D e Resultados.

Este módulo fornece funções para visualizar a retina 3D, mapas de dano celular,
evolução temporal e gráficos analíticos dos resultados da simulação.
"""

import numpy as np
from typing import Optional, Dict, List, Tuple
from scripts.config import FIGURE_DPI, FIGURE_SIZE, COLORMAP_RETINA, COLORMAP_DAMAGE
from scripts.retina import RetinaSim
from scripts.simulation import GlaucomaSimulator

try:
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.patches as mpatches

    MATPLOTLIB_AVAILABLE = True
except ImportError:
    MATPLOTLIB_AVAILABLE = False
    print("Aviso: Matplotlib não está instalado.")


class RetinaVisualizer:
    """
    Visualizador de retina 3D e análise de dados de simulação.
    
    Fornece métodos para plotar a geometria 3D da retina, mapas de saúde
    celular, progressão temporal e comparação de cenários.
    """

    def __init__(self, dpi: int = FIGURE_DPI, figsize: Tuple = FIGURE_SIZE):
        """
        Inicializa o visualizador.
        
        Args:
            dpi (int): Resolução das figuras em DPI.
            figsize (Tuple): Tamanho padrão das figuras (width, height).
        """
        self.dpi = dpi
        self.figsize = figsize
        self.matplotlib_available = MATPLOTLIB_AVAILABLE

        if not self.matplotlib_available:
            print(
                "Aviso: Matplotlib não está disponível. "
                "Visualizações não funcionarão."
            )

    def plot_retina_3d(
        self, retina: RetinaSim, show_only_alive: bool = True, title: str = "Retina 3D"
    ) -> Optional[plt.Figure]:
        """
        Plota a retina em 3D com cores baseadas em saúde celular.
        
        Args:
            retina (RetinaSim): Instância da retina a visualizar.
            show_only_alive (bool): Se True, mostra apenas células vivas.
            title (str): Título do gráfico.
        
        Returns:
            Optional[plt.Figure]: Figura matplotlib ou None se não disponível.
        """
        if not self.matplotlib_available:
            return None

        fig = plt.figure(figsize=self.figsize, dpi=self.dpi)
        ax = fig.add_subplot(111, projection="3d")

        # Filtra células
        cells_to_plot = (
            [c for c in retina.cells if c.is_alive]
            if show_only_alive
            else retina.cells
        )

        if not cells_to_plot:
            ax.text2D(0.5, 0.5, "Nenhuma célula para visualizar")
            return fig

        # Extrai coordenadas e saúde
        x = [c.x for c in cells_to_plot]
        y = [c.y for c in cells_to_plot]
        z = [c.z for c in cells_to_plot]
        health = [c.health for c in cells_to_plot]

        # Plota pontos
        scatter = ax.scatter(
            x, y, z, c=health, cmap=COLORMAP_RETINA, s=20, alpha=0.6, edgecolors="k"
        )

        ax.set_xlabel("X (Largura)")
        ax.set_ylabel("Y (Altura)")
        ax.set_zlabel("Z (Profundidade)")
        ax.set_title(title)

        # Colorbar
        cbar = plt.colorbar(scatter, ax=ax, shrink=0.5, aspect=5)
        cbar.set_label("Saúde Celular")

        return fig

    def plot_health_heatmap_2d(
        self,
        retina: RetinaSim,
        z_slice: Optional[float] = None,
        title: str = "Mapa de Saúde Celular (2D)",
    ) -> Optional[plt.Figure]:
        """
        Plota um mapa 2D de saúde celular em um corte da retina.
        
        Args:
            retina (RetinaSim): Instância da retina a visualizar.
            z_slice (Optional[float]): Profundidade do corte. Se None, usa média.
            title (str): Título do gráfico.
        
        Returns:
            Optional[plt.Figure]: Figura matplotlib ou None.
        """
        if not self.matplotlib_available:
            return None

        # Define corte
        if z_slice is None:
            z_slice = retina.depth / 2

        # Cria grid
        grid = np.zeros((retina.height, retina.width))
        counts = np.zeros((retina.height, retina.width))

        # Agrupa células por proximidade ao corte
        tolerance = retina.depth / 10
        for cell in retina.cells:
            if abs(cell.z - z_slice) < tolerance:
                x_idx = int((cell.x / retina.width) * (retina.width - 1))
                y_idx = int((cell.y / retina.height) * (retina.height - 1))

                grid[y_idx, x_idx] += cell.health
                counts[y_idx, x_idx] += 1

        # Calcula média
        valid_mask = counts > 0
        grid[valid_mask] /= counts[valid_mask]

        # Plota
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        im = ax.imshow(grid, cmap=COLORMAP_DAMAGE, origin="lower", aspect="auto")

        ax.set_xlabel("X (Largura)")
        ax.set_ylabel("Y (Altura)")
        ax.set_title(f"{title} (z={z_slice:.1f})")

        cbar = plt.colorbar(im, ax=ax)
        cbar.set_label("Saúde Média")

        return fig

    def plot_timeline(
        self,
        simulator: GlaucomaSimulator,
        show_metrics: List[str] = None,
        title: str = "Evolução Temporal da Simulação",
    ) -> Optional[plt.Figure]:
        """
        Plota a evolução temporal de métricas da simulação.
        
        Args:
            simulator (GlaucomaSimulator): Simulador com histórico.
            show_metrics (List[str]): Métricas a plotar
                (ex: ['iop', 'mortality_rate', 'average_health']).
            title (str): Título do gráfico.
        
        Returns:
            Optional[plt.Figure]: Figura matplotlib ou None.
        """
        if not self.matplotlib_available:
            return None

        if show_metrics is None:
            show_metrics = ["iop", "mortality_rate"]

        fig, axes = plt.subplots(
            len(show_metrics), 1, figsize=self.figsize, dpi=self.dpi
        )

        if len(show_metrics) == 1:
            axes = [axes]

        # iop_history começa com o valor inicial (n+1 entradas),
        # enquanto mortality_history acumula apenas durante os passos (n entradas).
        # Cada métrica usa seu próprio eixo X para evitar inconsistência de dimensão.

        for idx, metric in enumerate(show_metrics):
            ax = axes[idx]

            if metric == "iop":
                data = simulator.iop_history
                steps = range(len(data))
                ax.plot(steps, data, "b-", linewidth=2)
                ax.set_ylabel("IOP (mmHg)")
                ax.axhline(y=21, color="r", linestyle="--", label="Limite Normal")
                ax.legend()
            elif metric == "mortality_rate":
                data = simulator.mortality_history
                steps = range(len(data))
                ax.plot(steps, data, "r-", linewidth=2)
                ax.set_ylabel("Taxa de Mortalidade")
            else:
                # Tenta plotar atributo genérico
                if hasattr(simulator, metric):
                    data = getattr(simulator, metric)
                    steps = range(len(data))
                    ax.plot(steps, data, "g-", linewidth=2)
                    ax.set_ylabel(metric)

            ax.grid(True, alpha=0.3)
            ax.set_xlabel("Passo de Simulação")

            if idx == 0:
                ax.set_title(title)

        plt.tight_layout()
        return fig

    def plot_cell_type_distribution(
        self, retina: RetinaSim, title: str = "Distribuição de Tipos de Células"
    ) -> Optional[plt.Figure]:
        """
        Plota a distribuição de tipos de células.
        
        Args:
            retina (RetinaSim): Instância da retina.
            title (str): Título do gráfico.
        
        Returns:
            Optional[plt.Figure]: Figura matplotlib ou None.
        """
        if not self.matplotlib_available:
            return None

        stats = retina.get_statistics()
        type_stats = stats["by_type"]

        types = list(type_stats.keys())
        alive_counts = [type_stats[t]["alive"] for t in types]
        dead_counts = [type_stats[t]["dead"] for t in types]

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        x = np.arange(len(types))
        width = 0.35

        bars1 = ax.bar(x - width / 2, alive_counts, width, label="Vivas", color="green")
        bars2 = ax.bar(x + width / 2, dead_counts, width, label="Mortas", color="red")

        ax.set_xlabel("Tipo de Célula")
        ax.set_ylabel("Contagem")
        ax.set_title(title)
        ax.set_xticks(x)
        ax.set_xticklabels(types)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        return fig

    def plot_iop_distribution(
        self,
        iop_history: List[float],
        title: str = "Distribuição de Pressão Intraocular",
    ) -> Optional[plt.Figure]:
        """
        Plota o histograma de pressão intraocular ao longo do tempo.
        
        Args:
            iop_history (List[float]): Histórico de IOP.
            title (str): Título do gráfico.
        
        Returns:
            Optional[plt.Figure]: Figura matplotlib ou None.
        """
        if not self.matplotlib_available:
            return None

        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)

        ax.hist(iop_history, bins=30, color="skyblue", edgecolor="black", alpha=0.7)
        ax.axvline(np.mean(iop_history), color="red", linestyle="--", linewidth=2, label=f"Média: {np.mean(iop_history):.2f}")
        ax.axvline(np.median(iop_history), color="green", linestyle="--", linewidth=2, label=f"Mediana: {np.median(iop_history):.2f}")

        ax.set_xlabel("Pressão Intraocular (mmHg)")
        ax.set_ylabel("Frequência")
        ax.set_title(title)
        ax.legend()
        ax.grid(True, alpha=0.3, axis="y")

        return fig

    def save_figure(self, fig: plt.Figure, filepath: str) -> None:
        """
        Salva uma figura em arquivo.
        
        Args:
            fig (plt.Figure): Figura matplotlib a salvar.
            filepath (str): Caminho completo do arquivo.
        """
        if self.matplotlib_available and fig is not None:
            fig.savefig(filepath, dpi=self.dpi, bbox_inches="tight")
            print(f"Figura salva em: {filepath}")


if __name__ == "__main__":
    print("Teste do módulo de visualização...\n")

    if MATPLOTLIB_AVAILABLE:
        # Cria retina e simulador para teste
        retina = RetinaSim()
        simulator = GlaucomaSimulator(retina)
        simulator.run_simulation(num_steps=100, log_interval=50)

        visualizer = RetinaVisualizer()

        print("Criando visualizações...")
        fig1 = visualizer.plot_retina_3d(retina)
        fig2 = visualizer.plot_health_heatmap_2d(retina)
        fig3 = visualizer.plot_timeline(simulator)
        fig4 = visualizer.plot_cell_type_distribution(retina)
        fig5 = visualizer.plot_iop_distribution(simulator.iop_history)

        if fig1:
            plt.show()
    else:
        print("Matplotlib não está disponível. Instale-o para usar a visualização.")
