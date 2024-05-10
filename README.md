
### Objetivo

O projeto tem como objetivo avaliar diferentes políticas de escalonamento de requisições de I/O, por meio de simulações. As métricas utilizadas são: quantidade de seeks e tempo de execução. Ao executar o script, são apresentados gráficos de comparação entre as políticas C-SCAN e SSTF.

## Como Executar

1. **Criação de um ambiente virtual (opcional)**

   ```
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Instalação de Requisitos:**

   ```
   pip install -r requirements.txt
   ```

3. **Execução do Programa:**

   ```
   python main.py
   ```

   
## Opções Disponíveis

- **Iniciar**

    Ao selecionar esta opção, você pode escolher um caso de estudo para executar:
    
    - Primeiro Caso:
      - Descrição: Lista pequena ordenada e aleatória.
      
    - Segundo Caso:
      - Descrição: Lista de 10 mil elementos, tanto ordenada quanto aleatória.
      
    - Terceiro Caso:
      - Descrição: Comparação entre resultados de várias listas aleatórias e várias listas ordenadas.

- **Cancelar** 

    - Advertência: Nossos casos de estudo podem demorar a rodar devido ao número de requisições, especialmente o caso 3.
