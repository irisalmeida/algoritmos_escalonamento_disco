import random

import inquirer
import matplotlib.pyplot as plt
import statistics

import numpy as np
from algorithms import Cscan, Sstf
import generate_seqs


def create_figure():
    plt.figure(figsize=(18, 6))


def add_graph(name, x, y, color):
    plt.subplot(1, 3, 1)
    plt.plot(x, y, "o", color=color, label=name)

    plt.xlabel('Número de Requisições')
    plt.ylabel('Seek count')
    plt.title('')
    plt.legend()
    plt.grid(True)


def get_requests(file_path):
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
            sequences = []
            for line in lines:
                # Remove whitespace and brackets, then split by commas
                nums = line.strip().strip('[]').split(',')
                # Convert strings to integers and append to sequences list
                seq = [int(num) for num in nums if num.strip()]
                sequences.append(seq)
            return sequences
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return []
    except Exception as e:
        print(f"An error occurred: {e}")
        return []



def test_algorithms():
    requests = [278, 914, 447, 71, 161, 659, 335]
    # requests = [176, 79, 34, 60, 92, 11, 41, 114]
    # requests = [16, 24, 43, 82, 140, 170, 190]

    cscan = Cscan(requests, 50)
    seek_sequence, seek_count = cscan.execute()
    print("C-SCAN:")
    print(seek_sequence)
    print(seek_count)
    print()

    sstf = Sstf(requests, 50)
    seek_sequence, seek_count = sstf.execute()
    print("SSTF:")
    print(seek_sequence)
    print(seek_count)



def main():
    choices = ["Iniciar", "Cancelar"]
    input_option_question = inquirer.List(
        "input_option",
        message="Análise de algoritmos de disco C-SCAN e F-Scan",
        choices=choices,
    )
    answer = inquirer.prompt([input_option_question]) or {}
    if answer.get("input_option") == choices[1]:
        print("Operação cancelada pelo usuário.")
        exit()

    # test_algorithms()

    create_figure()

    seeks_cscan = []
    seeks_sstf = []
    execute_time_cscan = []
    execution_time_sstf_l = []
    requests = []
    # for _ in range(1000):
    #     requests = random.sample(range(0, 1000), 5)

    #requests = [16, 24, 43, 82, 140, 170, 190]
    #requests = [278, 914, 447, 71, 161, 659, 335]
    #requests = [71, 161, 278, 335, 447, 659, 914]
    # requests = [random.randint(0, 999) for _ in range(10000)]
    # requests.sort()
    lista_requests_aleatorias = get_requests("data/reqs_aleatorias.txt")
    lista_requests_sequenciais = get_requests("data/reqs_sequenciais.txt")

    lista_seek_count_cscan_ALEATORIA = []
    lista_execution_time_cscan_ALEATORIA = []
    lista_seek_count_sstf_ALEATORIA = []
    lista_execution_time_sstf_ALEATORIA = []

    for lista in lista_requests_aleatorias:
        cscan = Cscan(lista, 500)
        _, seek_count_cscan, execution_time_cscan = cscan.execute()
        lista_seek_count_cscan_ALEATORIA.append(seek_count_cscan)
        lista_execution_time_cscan_ALEATORIA.append(execution_time_cscan)

    for lista in lista_requests_aleatorias:
        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_ALEATORIA.append(seek_count_sstf)
        lista_execution_time_sstf_ALEATORIA.append(execution_time_sstf)

    print("ALEATÓRIAS")
    print("CSCAN")
    print(f"{statistics.mean(lista_seek_count_cscan_ALEATORIA) = }")
    print(f"{statistics.mean(lista_execution_time_cscan_ALEATORIA) = }")
    print("SSTF")
    print(f"{statistics.mean(lista_seek_count_sstf_ALEATORIA) = }")
    print(f"{statistics.mean(lista_execution_time_sstf_ALEATORIA) = }")

    lista_seek_count_cscan_SEQUENCIAL = []
    lista_execution_time_cscan_SEQUENCIAL = []
    lista_seek_count_sstf_SEQUENCIAL = []
    lista_execution_time_sstf_SEQUENCIAL = []

    for lista in lista_requests_sequenciais:
        cscan = Cscan(lista, 500)
        _, seek_count_cscan, execution_time_cscan = cscan.execute()
        lista_seek_count_cscan_SEQUENCIAL.append(seek_count_cscan)
        lista_execution_time_cscan_SEQUENCIAL.append(execution_time_cscan)

    for lista in lista_requests_sequenciais:
        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_SEQUENCIAL.append(seek_count_sstf)
        lista_execution_time_sstf_SEQUENCIAL.append(execution_time_sstf)

    print("SEQUENCIAIS")
    print("CSCAN")
    print(f"{statistics.mean(lista_seek_count_cscan_SEQUENCIAL) = }")
    print(f"{statistics.mean(lista_execution_time_cscan_SEQUENCIAL) = }")
    print("SSTF")
    print(f"{statistics.mean(lista_seek_count_sstf_SEQUENCIAL) = }")
    print(f"{statistics.mean(lista_execution_time_sstf_SEQUENCIAL) = }")

    import matplotlib.pyplot as plt

    def plot_comparison(seek_counts, execution_times, title, ylabel, order, labels):
        # Calcula a largura das barras
        bar_width = 0.35
        index = range(len(seek_counts) // 2)

        fig, ax = plt.subplots()
        # Plota as barras para CSCAN
        bars1 = ax.bar(index, seek_counts[:2], bar_width, label='CSCAN', color='purple')

        # Plota as barras para SSTF com um deslocamento
        bars2 = ax.bar([p + bar_width for p in index], seek_counts[2:], bar_width, label='SSTF', color='green')

        ax.set_xlabel('Tipo de Lista')
        ax.set_ylabel(ylabel)
        ax.set_title(title)
        ax.set_xticks([p + bar_width / 2 for p in index])
        ax.set_xticklabels(order)
        ax.legend()

        # Adiciona as etiquetas de dados nas barras
        for bars in (bars1, bars2):
            for bar in bars:
                height = bar.get_height()
                ax.annotate('{}'.format(height),
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 3),  # 3 pontos de deslocamento vertical
                            textcoords="offset points",
                            ha='center', va='bottom')

        plt.show()

    # # Asumindo que as listas *_ALEATORIA e *_SEQUENCIAL contêm os dados médios de cada algoritmo
    # plot_comparison(
    #     [statistics.mean(lista_seek_count_cscan_ALEATORIA), statistics.mean(lista_seek_count_cscan_SEQUENCIAL),
    #      statistics.mean(lista_seek_count_sstf_ALEATORIA), statistics.mean(lista_seek_count_sstf_SEQUENCIAL)],
    #     [statistics.mean(lista_execution_time_cscan_ALEATORIA), statistics.mean(lista_execution_time_cscan_SEQUENCIAL),
    #      statistics.mean(lista_execution_time_sstf_ALEATORIA), statistics.mean(lista_execution_time_sstf_SEQUENCIAL)],
    #     'Comparação de Seek Count por Algoritmo e Tipo de Lista',
    #     'Média de Seek Count',
    #     ['Aleatórias', 'Sequenciais'],
    #     ['CSCAN', 'SSTF']
    # )

    plot_comparison(
        [statistics.mean(lista_execution_time_cscan_ALEATORIA), statistics.mean(lista_execution_time_cscan_SEQUENCIAL),
         statistics.mean(lista_execution_time_sstf_ALEATORIA), statistics.mean(lista_execution_time_sstf_SEQUENCIAL)],
        [statistics.mean(lista_seek_count_cscan_ALEATORIA), statistics.mean(lista_seek_count_cscan_SEQUENCIAL),
         statistics.mean(lista_seek_count_sstf_ALEATORIA), statistics.mean(lista_seek_count_sstf_SEQUENCIAL)],
        'Comparação de Tempo de Execução por Algoritmo e Tipo de Lista',
        'Tempo de Execução (s)',
        ['Aleatórias', 'Sequenciais'],
        ['CSCAN', 'SSTF']
    )




# cscan = Cscan(requests, 500)
    # seek_sequence_cscan, seek_count_cscan, execution_time_cscan = cscan.execute()
    # seeks_cscan.append(seek_count_cscan)
    # execute_time_cscan.append(execution_time_cscan)
    # print(f"Tempo de execução do C-SCAN: {execution_time_cscan} ms")
    # print(f"Quantidade de Seeks do C-SCAN:{seeks_cscan}")
    #
    # sstf = Sstf(requests, 500)
    # seek_sequence_sstf, seek_count_sstf, execution_time_sstf = sstf.execute()
    # seeks_sstf.append(seek_count_sstf)
    # execution_time_sstf_l.append(execution_time_sstf)
    # print(f"Tempo de execução do SSTF: {execution_time_sstf} ms")
    # print(f"Quantidade de Seeks do SSTF:{seeks_sstf}")

#ESSE ABAIXO DEU BOM E FOI USADO
    # # Plotar o gráfico CSCAN
    # plt.figure(figsize=(10, 5))  # Define o tamanho da figura
    # plt.plot(seek_sequence_cscan, marker='o', color='purple')  # Plotar a sequência de movimentos
    # plt.title('Comportamento Circular do Algoritmo C-SCAN')
    # plt.xlabel('Sequência de Requisições')
    # plt.ylabel('Posição no Disco')
    # plt.xticks(range(len(seek_sequence_cscan)), labels=seek_sequence_cscan)  # Marca cada ponto com a posição correspondente
    # plt.grid(True)  # Adiciona uma grade para melhor visualização
    # plt.show()

    # Plotar o gráfico SSTF
    # plt.figure(figsize=(10, 5))  # Define o tamanho da figura
    # plt.plot(seek_sequence_sstf, marker='o', color='green')  # Plotar a sequência de movimentos
    # plt.title('Comportamento Circular do Algoritmo SSTF')
    # plt.xlabel('Sequência de Requisições')
    # plt.ylabel('Posição no Disco')
    # plt.xticks(range(len(seek_sequence_sstf)), labels=seek_sequence_sstf)  # Marca cada ponto com a posição correspondente
    # plt.grid(True)  # Adiciona uma grade para melhor visualização
    # plt.show()

    #print(f"{statistics.mean(seeks_cscan) = }")
    #print(f"{statistics.mean(seeks_sstf) = }")


"""
#QUANTIDADE TEMPOOOOO de execução  POR ALGORITMO(FIZ MANUAL PELA FALTA DE TEMPO):

    # Assume que seeks_cscan e seeks_sstf contêm o número total de seeks para cada algoritmo
    algorithms = ['C-SCAN', 'SSTF']  # Nomes dos algoritmos
    seek_counts = [0.022172927856445312, 0.07319450378417969]  # Total de seeks para cada algoritmo

    # Cria o gráfico de barras horizontais
    plt.figure(figsize=(10, 5))  # Ajusta o tamanho da figura para melhor visualização
    bars = plt.barh(algorithms, seek_counts, color=['green', 'purple'])  # Barras horizontais com cores

    # Adiciona os valores exatos no final de cada barra
    for bar, value in zip(bars, seek_counts):
        bbox = dict(boxstyle='round', facecolor='white', edgecolor='0.3')
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{value}', 
                va='center', ha='right', bbox=bbox)

    # Personaliza os rótulos e o título
    plt.xlabel('Tempo de execução (ms)')
    plt.ylabel('Algoritmo')
    plt.title('Comparação do tempo de execução entre C-SCAN e SSTF')

    # Ajusta o espaçamento e exibe o gráfico
    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.tight_layout()
    plt.show()

"""






"""
    #QUANTIDADE DE SEEKS POR ALGORITMO(FIZ MANUAL PELA FALTA DE TEMPO):

    # Assume que seeks_cscan e seeks_sstf contêm o número total de seeks para cada algoritmo
    algorithms = ['C-SCAN', 'SSTF']  # Nomes dos algoritmos
    seek_counts = [1945, 1272]  # Total de seeks para cada algoritmo

    # Cria o gráfico de barras horizontais
    plt.figure(figsize=(10, 5))  # Ajusta o tamanho da figura para melhor visualização
    bars = plt.barh(algorithms, seek_counts, color=['purple', 'green'])  # Barras horizontais com cores

    # Adiciona os valores exatos no final de cada barra
    for bar, value in zip(bars, seek_counts):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height()/2, f'{value}', 
                va='center', ha='left')

    # Personaliza os rótulos e o título
    plt.xlabel('Quantidade de Seeks')
    plt.ylabel('Algoritmo')
    plt.title('Comparação da Contagem de Seeks entre C-SCAN e SSTF')

    # Ajusta o espaçamento e exibe o gráfico
    plt.tight_layout()
    plt.show()
"""



"""
     #HISTOGRAMAAAA DE MÉDIAS 
    #teste do histograma:
    algoritmos = ['C-SCAN   ', 'SSTF       ']  # Lista de nomes dos algoritmos
    medias = [statistics.mean(seeks_cscan),statistics.mean(seeks_sstf) ]  # Lista de valores médios

    plt.bar(algoritmos, medias, color=['purple', 'green'], width=0.3)  # Ajustar cores e largura das barras

    plt.xlabel('Algoritmo')
    plt.ylabel('Média de Seek')
    plt.title('Comparação de Médias de Seek')
    plt.xticks([i + 0.1 for i in range(len(algoritmos))], algoritmos)  # Ajustar posição dos rótulos dos eixos X
    plt.show()
"""
















if __name__ == "__main__":
    main()
