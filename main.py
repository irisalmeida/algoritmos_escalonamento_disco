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
    # requests = [278, 914, 447, 71, 161, 659, 335]
    # requests = [176, 79, 34, 60, 92, 11, 41, 114]
    requests = [16, 24, 43, 82, 140, 170, 190]

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
    for _ in range(1000):
        requests = random.sample(range(0, 1000), 5)

        cscan = Cscan(requests, 500)
        _, seek_count_cscan = cscan.execute()
        #add_graph("C-SCAN", 50, seek_count_cscan, "blue")
        seeks_cscan.append(seek_count_cscan)

        sstf = Sstf(requests, 500)
        _, seek_count_sstf = sstf.execute()
        #add_graph("SSTF", 50, seek_count_sstf, "red")
        seeks_sstf.append(seek_count_sstf)

    print(f"{statistics.mean(seeks_cscan) = }")
    print(f"{statistics.mean(seeks_sstf) = }")




 

    #teste do histograma:
    algoritmos = ['C-SCAN   ', 'SSTF       ']  # Lista de nomes dos algoritmos
    medias = [statistics.mean(seeks_cscan),statistics.mean(seeks_sstf) ]  # Lista de valores médios

    plt.bar(algoritmos, medias, color=['purple', 'green'], width=0.3)  # Ajustar cores e largura das barras

    plt.xlabel('Algoritmo')
    plt.ylabel('Média de Seek')
    plt.title('Comparação de Médias de Seek')
    plt.xticks([i + 0.1 for i in range(len(algoritmos))], algoritmos)  # Ajustar posição dos rótulos dos eixos X
    plt.show()











if __name__ == "__main__":
    main()
