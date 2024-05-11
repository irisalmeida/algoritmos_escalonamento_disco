
### Objetivo

Este projeto visa avaliar diferentes políticas de escalonamento de requisições de I/O por meio de simulações. As métricas utilizadas são a quantidade de seeks e o tempo de execução. Ao executar o script, são apresentados gráficos de comparação entre as políticas C-SCAN e SSTF.

## Como Executar

1. **Criação de um Ambiente Virtual (Opcional)**

   ```bash
   python -m venv .venv
   source .venv/bin/activate
   ```

2. **Instalação de Requisitos**


   ```bash
   pip install -r requirements.txt
   ```

3. **Execução do Programa**

   ```bash
   python main.py
   ```

## 🔨 Funcionalidades do projeto

- **``Iniciar``**

    Ao selecionar esta opção, você pode escolher um caso de estudo para executar:
    
    - **`Primeiro Caso:`** Lista pequena ordenada e aleatória.
      
    - **`Segundo Caso:`** Lista de 10 mil elementos, tanto ordenada quanto aleatória.
      
    - **`Terceiro Caso:`** Comparação entre resultados de várias listas aleatórias e várias listas ordenadas.

- **``Cancelar``** 

    - Advertência: Nossos casos de estudo podem demorar a rodar devido ao número de requisições, especialmente o caso 3.

## Métricas usadas:

   - **`Lista Ordenada`**: As solicitações estão organizadas em ordem crescente ou decrescente de endereço de bloco. 
   - **`Lista Aleatória`**: As solicitações de acesso ao disco chegam de forma aleatória, refletindo um cenário mais realista com padrões de acesso imprevisíveis.
   - **`Tempo de Execução por Requisição`**: Indica o tempo gasto para processar todas as solicitações de acesso ao disco. 
   - **`Total de Seeks`**: Refere-se ao número total de movimentações do cabeçote do disco entre os cilindros.

