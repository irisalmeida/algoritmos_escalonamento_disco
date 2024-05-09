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
    #for _ in range(1000):
        #requests = random.sample(range(0, 1000), 5)

    #requests = [16, 24, 43, 82, 140, 170, 190]
    #requests = [24, 140, 16, 190, 43, 170, 82]
    requests = [71, 161, 278, 335, 447, 659, 914]
    print(requests)


    cscan = Cscan(requests, 500)
    _, seek_count_cscan, execution_time_cscan = cscan.execute()
    seeks_cscan.append(seek_count_cscan)
    execute_time_cscan.append(execution_time_cscan)
    print(f"Tempo de execução do C-SCAN: {execution_time_cscan} ms")
    print(f"Quantidade de Seeks do C-SCAN:{seeks_cscan}")
  
    sstf = Sstf(requests, 500)
    _, seek_count_sstf, execution_time_sstf = sstf.execute()
    seeks_sstf.append(seek_count_sstf)
    execution_time_sstf_l.append(execution_time_sstf)
    print(f"Tempo de execução do SSTF: {execution_time_sstf} ms")
    print(f"Quantidade de Seeks do SSTF:{seeks_sstf}")


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
