"""
Módulo de Modelo de IA para Predição de Glaucoma.

Este módulo implementa um modelo de rede neural para prever a progressão
do glaucoma e o prognóstico baseado em dados da simulação.
"""

import numpy as np
from typing import Tuple, List, Optional, Dict
from dataclasses import dataclass

try:
    from tensorflow import keras
    from tensorflow.keras import layers
    TENSORFLOW_AVAILABLE = True
except ImportError:
    TENSORFLOW_AVAILABLE = False
    print("Aviso: TensorFlow não está instalado. Algumas funcionalidades estarão limitadas.")

from scripts.config import (
    MODEL_INPUT_SIZE,
    MODEL_HIDDEN_LAYERS,
    MODEL_OUTPUT_SIZE,
    BATCH_SIZE,
    LEARNING_RATE,
    EPOCHS,
    TRAIN_TEST_SPLIT,
)


@dataclass
class ModelConfig:
    """Configuração do modelo de IA."""

    input_size: int = MODEL_INPUT_SIZE
    hidden_layers: List[int] = None
    output_size: int = MODEL_OUTPUT_SIZE
    batch_size: int = BATCH_SIZE
    learning_rate: float = LEARNING_RATE
    epochs: int = EPOCHS

    def __post_init__(self):
        """Inicializa valores padrão se não fornecidos."""
        if self.hidden_layers is None:
            self.hidden_layers = MODEL_HIDDEN_LAYERS


class GlaucomaPredictor:
    """
    Modelo de predição de glaucoma usando rede neural.
    
    Utiliza TensorFlow/Keras para criar e treinar um modelo que prediz
    a progressão do glaucoma baseado em características da simulação.
    """

    def __init__(self, config: Optional[ModelConfig] = None):
        """
        Inicializa o preditor de glaucoma.
        
        Args:
            config (Optional[ModelConfig]): Configuração do modelo.
                Se None, usa valores padrão.
        """
        self.config = config or ModelConfig()
        self.model = None
        self.history = None
        self.input_scaler = None
        self.output_scaler = None

        if TENSORFLOW_AVAILABLE:
            self._build_model()

    def _build_model(self) -> None:
        """
        Constrói a arquitetura da rede neural.
        
        Arquitetura:
        - Camada de entrada: input_size
        - Camadas ocultas: com ativação ReLU
        - Camada de saída: output_size com ativação sigmoid (probabilidades)
        - Dropout para regularização
        """
        if not TENSORFLOW_AVAILABLE:
            print("Erro: TensorFlow não está disponível para construir o modelo.")
            return

        self.model = keras.Sequential()

        # Camada de entrada
        self.model.add(keras.Input(shape=(self.config.input_size,)))

        # Camadas ocultas
        for hidden_size in self.config.hidden_layers:
            self.model.add(layers.Dense(hidden_size, activation="relu"))
            self.model.add(layers.Dropout(0.2))  # Regularização

        # Camada de saída
        self.model.add(layers.Dense(self.config.output_size, activation="sigmoid"))

        # Compilação
        optimizer = keras.optimizers.Adam(learning_rate=self.config.learning_rate)
        self.model.compile(
            optimizer=optimizer,
            loss="binary_crossentropy",
            metrics=["mse", "mae"],
        )

        print(f"Modelo construído com sucesso!")
        self.model.summary()

    def generate_synthetic_data(
        self, num_samples: int = 1000
    ) -> Tuple[np.ndarray, np.ndarray]:
        """
        Gera dados sintéticos para treinamento.
        
        Simula dados de características (IOP, mortalidade, etc.) e outputs
        (progressão, vitalidade, risco).
        
        Args:
            num_samples (int): Número de amostras a gerar.
        
        Returns:
            Tuple[np.ndarray, np.ndarray]: (dados_entrada, dados_saída)
        """
        # Características de entrada: [IOP, mortalidade, saúde média, ...]
        X = np.random.randn(num_samples, self.config.input_size)
        X[:, 0] = np.random.uniform(10, 50, num_samples)  # IOP (10-50 mmHg)
        X[:, 1] = np.random.uniform(0, 1, num_samples)  # Taxa de mortalidade

        # Saídas: [progressão_glaucoma, vitalidade, risco]
        y = np.random.uniform(0, 1, (num_samples, self.config.output_size))

        # Correlação: IOP alta → maior progressão
        y[:, 0] = np.clip(X[:, 0] / 50, 0, 1)  # Progressão correlacionada com IOP
        y[:, 1] = np.clip(1 - X[:, 1], 0, 1)  # Vitalidade inversa à mortalidade
        y[:, 2] = np.clip((X[:, 0] - 21) / 30, 0, 1)  # Risco correlacionado com IOP

        return X, y

    def train(
        self,
        X_train: Optional[np.ndarray] = None,
        y_train: Optional[np.ndarray] = None,
        X_val: Optional[np.ndarray] = None,
        y_val: Optional[np.ndarray] = None,
        use_synthetic: bool = True,
    ) -> Dict:
        """
        Treina o modelo.
        
        Args:
            X_train (Optional[np.ndarray]): Dados de treinamento (entrada).
            y_train (Optional[np.ndarray]): Dados de treinamento (saída).
            X_val (Optional[np.ndarray]): Dados de validação (entrada).
            y_val (Optional[np.ndarray]): Dados de validação (saída).
            use_synthetic (bool): Se True, gera dados sintéticos para teste.
        
        Returns:
            Dict: Histórico de treinamento.
        """
        if not TENSORFLOW_AVAILABLE:
            print("Erro: TensorFlow não está disponível para treinar.")
            return {}

        if use_synthetic or X_train is None:
            print("Gerando dados sintéticos para treinamento...")
            X, y = self.generate_synthetic_data(num_samples=1000)

            # Split em treino/validação
            split_idx = int(len(X) * TRAIN_TEST_SPLIT)
            X_train, X_val = X[:split_idx], X[split_idx:]
            y_train, y_val = y[:split_idx], y[split_idx:]

        print(f"Treinando modelo com {len(X_train)} amostras...")
        self.history = self.model.fit(
            X_train,
            y_train,
            batch_size=self.config.batch_size,
            epochs=self.config.epochs,
            validation_data=(X_val, y_val),
            verbose=1,
        )

        return self.history.history

    def predict(self, X: np.ndarray) -> np.ndarray:
        """
        Faz predições usando o modelo.
        
        Args:
            X (np.ndarray): Dados de entrada para predição.
        
        Returns:
            np.ndarray: Predições do modelo.
        """
        if self.model is None:
            print("Erro: Modelo não foi construído ou treinado.")
            return np.array([])

        return self.model.predict(X)

    def evaluate(self, X_test: np.ndarray, y_test: np.ndarray) -> Dict:
        """
        Avalia o modelo em dados de teste.
        
        Args:
            X_test (np.ndarray): Dados de teste (entrada).
            y_test (np.ndarray): Dados de teste (saída esperada).
        
        Returns:
            Dict: Métricas de avaliação.
        """
        if self.model is None:
            print("Erro: Modelo não foi construído.")
            return {}

        loss, mse, mae = self.model.evaluate(X_test, y_test, verbose=0)

        return {
            "loss": loss,
            "mse": mse,
            "mae": mae,
        }

    def save_model(self, filepath: str) -> None:
        """
        Salva o modelo treinado.
        
        Args:
            filepath (str): Caminho para salvar o modelo.
        """
        if self.model is not None and TENSORFLOW_AVAILABLE:
            self.model.save(filepath)
            print(f"Modelo salvo em: {filepath}")

    def load_model(self, filepath: str) -> None:
        """
        Carrega um modelo previamente salvo.
        
        Args:
            filepath (str): Caminho do modelo salvo.
        """
        if TENSORFLOW_AVAILABLE:
            self.model = keras.models.load_model(filepath)
            print(f"Modelo carregado de: {filepath}")

    def predict_from_iop(self, iop: float, mortality_rate: float = 0.0) -> Dict[str, float]:
        """
        Prediz progressão de glaucoma a partir de IOP (e opcionalmente mortalidade).

        Constrói o vetor de entrada esperado pelo modelo e retorna
        um dicionário com as mesmas chaves de SimplePredictor.

        Args:
            iop (float): Pressão intraocular em mmHg.
            mortality_rate (float): Taxa de mortalidade acumulada [0-1].

        Returns:
            Dict[str, float]: {glaucoma_progression, cell_vitality, risk_level}
        """
        if not TENSORFLOW_AVAILABLE or self.model is None:
            # Fallback para regas simples se o modelo não estiver disponível
            normalized_iop = np.clip((iop - 10) / 40, 0, 1)
            return {
                "glaucoma_progression": float(normalized_iop),
                "cell_vitality": float(max(0, 1 - normalized_iop)),
                "risk_level": float(np.clip(normalized_iop * 1.5, 0, 1)),
            }

        # Monta vetor de entrada na mesma ordem do treinamento sintético:
        # feature[0] = IOP, feature[1] = mortalidade, restante = 0
        X = np.zeros((1, self.config.input_size), dtype=np.float32)
        X[0, 0] = float(iop)
        X[0, 1] = float(mortality_rate)

        preds = self.model.predict(X, verbose=0)[0]  # shape (output_size,)
        return {
            "glaucoma_progression": float(np.clip(preds[0], 0, 1)),
            "cell_vitality":        float(np.clip(preds[1], 0, 1)),
            "risk_level":           float(np.clip(preds[2], 0, 1)),
        }


class SimplePredictor:
    """
    Preditor simples baseado em regras (sem dependências de TensorFlow).
    
    Útil como baseline quando TensorFlow não está disponível.
    """

    def __init__(self):
        """Inicializa o preditor simples."""
        pass

    def predict_from_iop(self, iop: float) -> Dict[str, float]:
        """
        Prediz progressão de glaucoma baseado em IOP.
        
        Args:
            iop (float): Pressão intraocular em mmHg.
        
        Returns:
            Dict[str, float]: Dicionário com predições.
        """
        # Normaliza IOP para 0-1
        normalized_iop = np.clip((iop - 10) / 40, 0, 1)

        return {
            "glaucoma_progression": normalized_iop,
            "cell_vitality": max(0, 1 - normalized_iop),
            "risk_level": np.clip(normalized_iop * 1.5, 0, 1),
        }


if __name__ == "__main__":
    print("Inicializando modelo de IA para predição de glaucoma...\n")

    if TENSORFLOW_AVAILABLE:
        config = ModelConfig()
        predictor = GlaucomaPredictor(config)

        print("\nTreinando modelo...")
        history = predictor.train(epochs=10)

        print("\nTeste de predição...")
        X_test = np.random.randn(5, MODEL_INPUT_SIZE)
        predictions = predictor.predict(X_test)
        print(f"Predições (5 amostras):\n{predictions}")
    else:
        print("TensorFlow não disponível. Usando SimplePredictor...\n")
        simple_pred = SimplePredictor()

        test_iop_values = [15, 20, 25, 35, 45]
        for iop in test_iop_values:
            pred = simple_pred.predict_from_iop(iop)
            print(f"IOP {iop} mmHg: {pred}")
