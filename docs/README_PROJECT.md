# Simulador de Retina 3D com Glaucoma
Inicio do Desenvolvimento Quarta Feira de Cinzas 18/02/2026 19:00h

Projeto completo de simulação e análise de progressão de glaucoma em retina 3D, utilizando inteligência artificial para predição e visualização tridimensional.


Desenvolvido por @enricomalta
## 🎯 Objetivos

- Simular a estrutura 3D da retina humana
- Modelar a progressão do glaucoma baseado em pressão intraocular (IOP)
- Predizer morte celular e deterioração da visão
- Treinar modelos de IA para análise de simulações
- Visualizar dados em 3D e gráficos analíticos

## 📁 Estrutura do Projeto

```
glaucoma/
├── data/                    # Dados brutos e datasets de simulação
├── notebooks/              # Jupyter Notebooks para análise interativa
├── scripts/                # Módulos Python principais
│   ├── __init__.py
│   ├── config.py           # Configuração global do projeto
│   ├── retina.py           # Geração e gestão de retina 3D
│   ├── simulation.py       # Simulação de glaucoma e IOP
│   ├── ai_model.py         # Modelos de IA e redes neurais
│   └── visualization.py    # Visualização de resultados
├── models/                 # Modelos treinados (.h5, .pkl)
├── simulations/            # Dados e checkpoints de simulações
├── utils/                  # Funções utilitárias e helpers
├── results/                # Gráficos, tabelas e saídas
├── main.py                 # Script principal de execução
├── requirements.txt        # Dependências do projeto
└── README.md              # Este arquivo
```

## 🚀 Início Rápido

### 1. Instalação de Dependências

```bash
# Ativar ambiente virtual (recomendado)
python -m venv venv
venv\Scripts\activate  # Windows
source venv/bin/activate  # Linux/Mac

# Instalar dependências
pip install -r requirements.txt
```

### 2. Executar Simulação Principal

```bash
python main.py
```

Isto irá:
- Criar uma retina simulada com 10.000 células
- Executar 100 passos de simulação de glaucoma
- Treinar um modelo de IA para predição
- Gerar gráficos e visualizações
- Salvar resultados em `results/`

### 3. Explorar Notebooks

```bash
jupyter notebook
# Abra notebooks/ para análises interativas
```

## 📚 Módulos Principais

### `scripts/config.py`
Centraliza todos os parâmetros da simulação:
- Dimensões da retina
- Número de células
- Parâmetros físicos (IOP, taxa de morte celular)
- Configurações de IA e visualização

**Uso:**
```python
from scripts.config import get_config, TOTAL_CELLS, INITIAL_IOP
config = get_config()
```

### `scripts/retina.py`
Define estrutura de células 3D e gerenciamento:
- Classe `Cell`: representa célula individual
- Classe `RetinaSim`: gerencia população celular

**Uso:**
```python
from scripts.retina import RetinaSim
retina = RetinaSim()
print(retina.get_statistics())
```

### `scripts/simulation.py`
Simula progressão do glaucoma:
- Variação de pressão intraocular
- Morte celular baseada em IOP
- Efeito de tratamento médico

**Uso:**
```python
from scripts.simulation import GlaucomaSimulator
simulator = GlaucomaSimulator(retina)
results = simulator.run_simulation(num_steps=100)
```

### `scripts/ai_model.py`
Modelos de predição usando IA:
- `GlaucomaPredictor`: Rede neural com TensorFlow/Keras
- `SimplePredictor`: Baseline sem dependências complexas

**Uso:**
```python
from scripts.ai_model import GlaucomaPredictor
predictor = GlaucomaPredictor()
predictor.train(use_synthetic=True)
```

### `scripts/visualization.py`
Visualizações 3D e gráficos:
- Retina 3D interativa
- Mapas de calor 2D
- Gráficos de evolução temporal
- Distribuição de tipos celulares

**Uso:**
```python
from scripts.visualization import RetinaVisualizer
visualizer = RetinaVisualizer()
fig = visualizer.plot_retina_3d(retina)
```

## 🔬 Fluxo de Trabalho Típico

### 1. Personalizar Configuração
Editar `scripts/config.py` para ajustar:
- Número de células
- Pressão inicial
- Taxa de morte celular
- Parâmetros de IA

### 2. Criar Simulação
```python
from scripts.retina import RetinaSim
from scripts.simulation import GlaucomaSimulator

retina = RetinaSim()
simulator = GlaucomaSimulator(retina)
results = simulator.run_simulation(num_steps=500)
```

### 3. Análise de Resultados
```python
summary = simulator.get_summary()
print(f"Mortalidade final: {summary['final_mortality_rate']:.2%}")
```

### 4. Visualizar
```python
from scripts.visualization import RetinaVisualizer
visualizer = RetinaVisualizer()
fig = visualizer.plot_timeline(simulator)
visualizer.save_figure(fig, "results/timeline.png")
```

## 📊 Parâmetros Ajustáveis

### Pressão Intraocular (IOP)
- Normal: 10-21 mmHg
- Elevada: > 21 mmHg
- Severa: > 30 mmHg

### Taxa de Morte Celular
- Normal: 0.1% por passo
- IOP elevada: 5% por passo
- IOP severa: 15% por passo

### Células
- Fotorreceptores: 40%
- Células Bipolares: 30%
- Células Ganglionares: 20%
- Células Gliais: 10%

## 🤖 Modelo de IA

O projeto inclui um modelo de rede neural para predição de glaucoma:

### Arquitetura
- Entrada: 20 características (IOP, mortalidade, saúde, etc.)
- Camadas ocultas: [64, 32, 16]
- Saída: 3 valores (progressão, vitalidade, risco)

### Treinamento
```python
predictor = GlaucomaPredictor()
history = predictor.train(epochs=100, use_synthetic=True)
predictor.save_model("models/glaucoma_model.h5")
```

## 📈 Outputs Gerados

Após executar `main.py`, em `results/`:

- `retina_3d.png`: Visualização 3D da retina
- `health_heatmap.png`: Mapa de saúde celular
- `timeline.png`: Evolução temporal de IOP e mortalidade
- `cell_distribution.png`: Distribuição de tipos celulares
- `iop_distribution.png`: Histograma de pressão
- `simulation_results.json`: Dados completos da simulação

## 🔧 Boas Práticas Implementadas

✅ **Type Hints**: Todas as funções têm anotações de tipo
✅ **Docstrings**: Documentação completa em English
✅ **Modularização**: Código organizado em módulos independentes
✅ **Configuração Centralizada**: Parâmetros em `config.py`
✅ **Tratamento de Erros**: Validação de entrada e tratamento de exceções
✅ **Reprodutibilidade**: Seeds aleatórias fixadas
✅ **Performance**: Uso de NumPy para operações vetorizadas

## 📦 Dependências

- `numpy`: Computação científica
- `matplotlib`: Visualização 2D/3D
- `tensorflow / keras`: Modelos de IA (opcional)
- `jupyter`: Notebooks interativos

Ver `requirements.txt` para versões específicas.

## 🐛 Troubleshooting

### ImportError: tensorflow not found
```bash
pip install tensorflow
```

### ImportError: matplotlib not found
```bash
pip install matplotlib
```

### Uso de memória elevado
- Reduzir `TOTAL_CELLS` em `config.py`
- Usar checkpoint de simulações em `simulations/`

## 📝 Exemplos Adicionales

### Simular com Tratamento
```python
simulator.apply_treatment(effectiveness=0.8)
results = simulator.run_simulation(num_steps=100)
```

### Exportar Dados
```python
from utils import save_simulation_results
save_simulation_results(simulator.get_summary(), "results/sim.json")
```

### Comparar Cenários
```python
# Sem tratamento
sim1 = GlaucomaSimulator(retina1)
sim1.run_simulation(200)

# Com tratamento
sim2 = GlaucomaSimulator(retina2)
sim2.apply_treatment()
sim2.run_simulation(200)

# Comparar resultados
print(sim1.get_summary())
print(sim2.get_summary())
```

## 📄 Licença

Projeto de Pesquisa - Simulação de Glaucoma em Retina 3D

## 👥 Contribuições

Contribuições são bem-vindas! Abra um Issue ou Pull Request.

## 📧 Contato

Para dúvidas ou sugestões sobre o projeto, abra uma Issue no repositório.

---

**Última atualização**: 18 de Fevereiro de 2026
