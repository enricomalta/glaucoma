"""
Guide de Desenvolvimento - Estilo de Código e Práticas

Este arquivo documenta as convenções e boas práticas usadas no projeto.
"""

# ============================================================================
# ESTILO DE CÓDIGO
# ============================================================================

"""
1. Type Hints
   - Sempre usar type hints em assinaturas de funções
   - Usar para argumentos, retorno e variáveis quando apropriado
   
   ✓ Correto:
   def process_cells(cells: List[Cell]) -> Dict[str, int]:
       pass
   
   ✗ Incorreto:
   def process_cells(cells):
       pass
"""

"""
2. Docstrings
   - Usar docstrings em Google format
   - Incluir descrição, Args, Returns e Raises
   
   ✓ Correto:
   def calculate_mortality(iop: float) -> float:
       '''Calcula taxa de mortalidade baseado em IOP.
       
       Args:
           iop (float): Pressão intraocular em mmHg.
       
       Returns:
           float: Taxa de mortalidade (0.0 a 1.0).
       '''
       pass
"""

"""
3. Nomes
   - Classes: PascalCase (ex: RetinaSim)
   - Funções: snake_case (ex: calculate_mortality)
   - Constantes: UPPER_SNAKE_CASE (ex: TOTAL_CELLS)
   - Privadas: _snake_case (ex: _private_method)
"""

"""
4. Comprimento de Linhas
   - Máximo 88 caracteres (Black formatter)
   - Quebrar em múltiplas linhas se necessário
"""

# ============================================================================
# ESTRUTURA DE MÓDULOS
# ============================================================================

"""
Padrão de organização:

1. Docstring do módulo no início
2. Imports (stdlib, third-party, local)
3. Constantes
4. Classes
5. Funções
6. main() / testes
"""

# ============================================================================
# BOAS PRÁTICAS
# ============================================================================

"""
1. Tratamento de Erros
   - Usar try/except específicos, não capturar Exception genérico
   - Fornecer mensagens de erro úteis
   
   ✓ Correto:
   try:
       result = model.predict(data)
   except ValueError as e:
       print(f"Erro na predição: {e}")

2. Performance
   - Preferir NumPy para operações vetorizadas
   - Evitar loops Python para grandes datasets
   - Usar generators para dados grandes

3. Documentação
   - Comentários para "por quê", não "o quê"
   - Exemplos em docstrings quando complexo
   - README.md atualizado

4. Testes
   - Testes em test_project.py
   - Executar: python test_project.py
   - Adicionar testes para novos componentes
"""

# ============================================================================
# FLUXO DE DESENVOLVIMENTO
# ============================================================================

"""
1. Feature Branch
   git checkout -b feature/description

2. Fazer Mudanças
   - Seguir convenções
   - Não quebrar código existente
   - Testar localmente

3. Commit
   git add .
   git commit -m "Descrição clara da mudança"

4. Pull Request
   - Descrever mudanças
   - Referir issues relacionados
   - Pedir review

5. Merge
   - Após aprovação
   - Deletar branch local
"""

# ============================================================================
# COMO ADICIONAR NOVOS MÓDULOS
# ============================================================================

"""
1. Criar arquivo em local apropriado (scripts/, utils/, etc.)

2. Estrutura básica:
   '''
   \"\"\"Docstring do módulo.\"\"\"
   
   import os
   from typing import Dict, List
   from scripts.config import CONSTANT_NAME
   
   class NewClass:
       \"\"\"Documentação da classe.\"\"\"
       
       def __init__(self):
           \"\"\"Inicializar.\"\"\"
           pass
       
       def method(self) -> str:
           \"\"\"Documentação do método.\"\"\"
           return "resultado"
   
   def helper_function(x: int) -> int:
       \"\"\"Documentação da função.\"\"\"
       return x * 2
   
   if __name__ == "__main__":
       # Testes/exemplos
       pass
   '''

3. Adicionar imports em __init__.py do pacote

4. Adicionar testes em test_project.py

5. Documentar em README.md
"""

# ============================================================================
# DEBUGGING
# ============================================================================

"""
1. Print Debug
   print(f"DEBUG: variavel={variavel}, tipo={type(variavel)}")

2. Breakpoint (Python 3.7+)
   breakpoint()  # Abre PDB
   
3. Logging
   import logging
   logger = logging.getLogger(__name__)
   logger.debug("Mensagem de debug")

4. NumPy Arrays
   array.shape
   array.dtype
   array.min(), array.max(), array.mean()
"""

# ============================================================================
# PERFORMANCE
# ============================================================================

"""
1. Profiling
   import cProfile
   cProfile.run('function()')

2. Timing
   import time
   start = time.time()
   # código
   print(f"Tempo: {time.time() - start:.2f}s")

3. Memory
   import tracemalloc
   tracemalloc.start()
   # código
   print(tracemalloc.get_traced_memory())
"""

# ============================================================================
# RESOURCES
# ============================================================================

"""
Documentação externa útil:

- Python Style Guide (PEP 8): https://pep8.org/
- Type Hints: https://docs.python.org/3/library/typing.html
- NumPy: https://numpy.org/doc/
- Matplotlib: https://matplotlib.org/
- TensorFlow: https://www.tensorflow.org/
- Jupyter: https://jupyter.org/
"""
