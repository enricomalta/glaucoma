# 🚀 GUIA DE INÍCIO RÁPIDO

## Em 5 Minutos

### 1️⃣ Ativar Ambiente Virtual
```bash
# Windows
cd d:\Dados\Coding\glaucoma
python -m venv venv
venv\Scripts\activate

# Linux/Mac
cd glaucoma
python3 -m venv venv
source venv/bin/activate
```

### 2️⃣ Instalar Dependências
```bash
pip install numpy matplotlib scipy jupyter
# Opcional (para IA completa):
pip install tensorflow
```

### 3️⃣ Validar Instalação
```bash
python -c "from scripts.retina import RetinaSim; r = RetinaSim(); print(f'✓ Retina criada com {r.get_alive_cells_count():,} células')"
```

### 4️⃣ Executar Simulação
```bash
python main.py
```

Isto criará gráficos em `results/` em ~2-3 minutos.

### 5️⃣ Explorar Notebook Interativo
```bash
jupyter notebook notebooks/01_introducao_simulacao.ipynb
```

---

## 📊 Testes Rápidos

```bash
# Testar todos os módulos
python test_project.py

# Testar um módulo específico
python -c "from scripts.retina import RetinaSim; RetinaSim().get_statistics()"
```

---

## 💡 Exemplos de Código

### Criar Retina e Executar Simulação
```python
from scripts.retina import RetinaSim
from scripts.simulation import GlaucomaSimulator

# Criar retina
retina = RetinaSim()
print(f"Retina com {len(retina.cells)} células")

# Simular glaucoma
simulator = GlaucomaSimulator(retina)
results = simulator.run_simulation(num_steps=100)

# Ver resultados
summary = simulator.get_summary()
print(f"IOP final: {summary['final_iop']:.1f} mmHg")
print(f"Mortalidade: {summary['final_mortality_rate']:.1%}")
```

### Visualizar Resultados
```python
from scripts.visualization import RetinaVisualizer

visualizer = RetinaVisualizer()

# Plotar retina 3D
fig1 = visualizer.plot_retina_3d(retina)
visualizer.save_figure(fig1, "results/retina.png")

# Plotar timeline
fig2 = visualizer.plot_timeline(simulator)
visualizer.save_figure(fig2, "results/timeline.png")
```

### Fazer Predições
```python
from scripts.ai_model import SimplePredictor

predictor = SimplePredictor()
pred = predictor.predict_from_iop(35.0)  # IOP elevada
print(f"Risco: {pred['risk_level']:.1%}")
```

---

## 🛠️ Personalizar Simulação

Editar `scripts/config.py`:

```python
# Aumentar número de células
TOTAL_CELLS = 50000

# Aumentar pressão inicial
INITIAL_IOP = 25.0

# Alterar duração
TIME_STEPS = 500
```

---

## 📁 Arquivos Principais

| Arquivo | Descrição |
|---------|-----------|
| `main.py` | Script principal que executa tudo |
| `scripts/config.py` | Parâmetros globais |
| `scripts/retina.py` | Geração de retina 3D |
| `scripts/simulation.py` | Simulação de glaucoma |
| `scripts/ai_model.py` | Modelos de IA |
| `scripts/visualization.py` | Gráficos e visualizações |
| `test_project.py` | Testes unitários |
| `notebooks/01_introducao_simulacao.ipynb` | Tutorial interativo |

---

## ⚠️ Problemas Comuns

### "ModuleNotFoundError: No module named 'numpy'"
```bash
pip install numpy
```

### "ModuleNotFoundError: No module named 'tensorflow'"
(Opcional - código funciona sem)
```bash
pip install tensorflow  # ou pip install tensorflow-cpu
```

### "No module named 'scripts'"
Certifique-se de estar no diretório `glaucoma/`:
```bash
cd d:\Dados\Coding\glaucoma
python main.py
```

---

## 📚 Documentação Completa

- **Documentação do projeto**: `README_PROJECT.md`
- **Guia de desenvolvimento**: `DEVELOPMENT.md`
- **Estrutura do projeto**: `PROJECT_STRUCTURE.py`
- **Testes**: `test_project.py`

---

## ✅ Checklist de Setup

- [ ] Python 3.7+ instalado
- [ ] Environment virtual criado e ativado
- [ ] Base requirements instalado: `pip install -r requirements.txt`
- [ ] Teste rápido passou: `python test_project.py`
- [ ] `main.py` executou com sucesso
- [ ] Gráficos gerados em `results/`

---

## 🎯 Próximos Passos

Após familiarizar-se:

1. **Explorar dados**: Abrir `results/` para ver outputs
2. **Modificar parâmetros**: Ajustar `scripts/config.py`
3. **Rodar múltiplas simulações**: Criar scripts de batch
4. **Treinar modelo**: Usar `scripts/ai_model.py` com dados reais
5. **Criar visualizações customizadas**: Estender `scripts/visualization.py`
6. **Implementar novos features**: Adicionar módulos em `scripts/`

---

## 🆘 Suporte

Se encontrar problemas:
1. Ler `DEVELOPMENT.md` para convenções
2. Executar `test_project.py` para validar
3. Consultar docstrings das classes (`help(RetinaSim)`, etc)
4. Verificar notebooks para exemplos
