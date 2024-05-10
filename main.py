import random
import inquirer
import matplotlib.pyplot as plt
import statistics
from algorithms import Cscan, Sstf


def get_requests(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
        sequences = []
        for line in lines:
            nums = line.strip().strip('[]').split(',')
            seq = [int(num) for num in nums if num.strip()]
            sequences.append(seq)
        return sequences


def primeiro_caso(should_print_and_plot):
    requests_ord = [278, 914, 447, 71, 161, 659, 335]
    requests_aleat = [71, 161, 278, 335, 447, 659, 914]

    cscan = Cscan(requests_ord, 500)
    seek_sequence1, seek_count1, execution_time1 = cscan.execute()

    sstf = Sstf(requests_ord, 500)
    seek_sequence2, seek_count2, execution_time2 = sstf.execute()

    cscan2 = Cscan(requests_aleat, 500)
    seek_sequence3, seek_count3, execution_time3 = cscan2.execute()

    sstf2 = Sstf(requests_aleat, 500)
    seek_sequence4, seek_count4, execution_time4 = sstf2.execute()

    if should_print_and_plot:
        print("C-SCAN lista ordenada:")
        print(f"Contagem de seeks: {seek_count1}")
        print(f"Tempo de execução: {execution_time1}\n")

        print("SSTF lista ordenada:")
        print(f"Contagem de seeks: {seek_count2}")
        print(f"Tempo de execução: {execution_time2}\n")

        print("C-SCAN lista aleatória:")
        print(f"Contagem de seeks: {seek_count3}")
        print(f"Tempo de execução: {execution_time3}\n")

        print("SSTF lista aleatória:")
        print(f"Contagem de seeks: {seek_count4}")
        print(f"Tempo de execução: {execution_time4}\n")

        plt.figure(figsize=(10, 5))
        plt.plot(seek_sequence3, marker='o', color='purple')
        plt.title('Comportamento Circular do Algoritmo C-SCAN')
        plt.xlabel('Sequência de Requisições')
        plt.ylabel('Posição no Disco')
        plt.xticks(range(len(seek_sequence3)), labels=seek_sequence3)
        plt.grid(True)
        plt.show()

    return seek_count1, execution_time1, seek_count2, execution_time2


def plota_grafico_comparacao_seek_count(seek_count_cscan, seek_count_sstf, xlabel, ylabel, title):
    algorithms = ['C-SCAN', 'SSTF']
    seek_counts = [seek_count_cscan, seek_count_sstf]

    plt.figure(figsize=(10, 5))
    bars = plt.barh(algorithms, seek_counts, color=['purple', 'green'])

    for bar, value in zip(bars, seek_counts):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}',
                 va='center', ha='left')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.tight_layout()
    plt.show()


def plota_grafico_comparacao_execution_time(execution_time_cscan, execution_time_sstf, xlabel, ylabel, title):
    algorithms = ['C-SCAN', 'SSTF']
    seek_counts = [execution_time_cscan, execution_time_sstf]

    plt.figure(figsize=(10, 5))
    bars = plt.barh(algorithms, seek_counts, color=['purple', 'green'])

    for bar, value in zip(bars, seek_counts):
        bbox = dict(boxstyle='round', facecolor='white', edgecolor='0.3')
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value}',
                 va='center', ha='right', bbox=bbox)

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.tight_layout()
    plt.show()


def segundo_caso():
    requests = [random.randint(0, 999) for _ in range(10000)]
    requests.sort()

    seek_count_pq_cscan, execution_time_pq_cscan, seek_count_pq_sstf, execution_time_pq_sstf = primeiro_caso(False)

    cscan = Cscan(requests, 500)
    seek_sequence_gd_cscan, seek_count_gd_cscan, execution_time_gd_cscan = cscan.execute()
    print("C-SCAN lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_cscan}")
    print(f"Tempo de execução: {execution_time_gd_cscan}\n")

    sstf = Sstf(requests, 500)
    seek_sequence_gd_sstf, seek_count_gd_sstf, execution_time_gd_sstf = sstf.execute()
    print("SSTF lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_sstf}")
    print(f"Tempo de execução: {execution_time_gd_sstf}\n")

    plota_grafico_comparacao_seek_count(seek_count_pq_cscan, seek_count_pq_sstf, 'Quantidade de Seeks', 'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista pequena e ordenada')
    plota_grafico_comparacao_execution_time(execution_time_pq_cscan, execution_time_pq_sstf, 'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação do tempo de execução entre C-SCAN e SSTF para uma lista pequena e ordenada')

    plota_grafico_comparacao_seek_count(seek_count_gd_cscan, seek_count_gd_sstf, 'Quantidade de Seeks', 'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista com 10 mil elementos e ordenada')
    plota_grafico_comparacao_execution_time(execution_time_gd_cscan, execution_time_gd_sstf, 'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação do tempo de execução entre C-SCAN e SSTF para uma lista com 10 mil elementos e ordenada')


def histograma_medias(seek_counts, title, ylabel, order):
    bar_width = 0.35
    index = range(len(seek_counts) // 2)

    fig, ax = plt.subplots()
    bars1 = ax.bar(index, seek_counts[:2], bar_width, label='C-SCAN', color='purple')

    bars2 = ax.bar([p + bar_width for p in index], seek_counts[2:], bar_width, label='SSTF', color='green')

    ax.set_xlabel('Tipo de Lista')
    ax.set_ylabel(ylabel)
    ax.set_title(title)
    ax.set_xticks([p + bar_width / 2 for p in index])
    ax.set_xticklabels(order)
    ax.legend()

    for bars in (bars1, bars2):
        for bar in bars:
            height = bar.get_height()
            ax.annotate('{}'.format(height),
                        xy=(bar.get_x() + bar.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom')

    plt.show()


def terceiro_caso():
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

        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_ALEATORIA.append(seek_count_sstf)
        lista_execution_time_sstf_ALEATORIA.append(execution_time_sstf)

    print("LISTAS ALEATÓRIAS")
    print("C-SCAN:")
    seek_media_cscan_aleatoria = statistics.mean(lista_seek_count_cscan_ALEATORIA)
    execution_medio_cscan_aleatoria = statistics.mean(lista_execution_time_cscan_ALEATORIA)
    print(f"Quantidade de seek média: {seek_media_cscan_aleatoria}")
    print(f"Tempo de execução médio: {execution_medio_cscan_aleatoria}")

    print("SSTF:")
    seek_media_sstf_aleatoria = statistics.mean(lista_seek_count_sstf_ALEATORIA)
    execution_medio_sstf_aleatoria = statistics.mean(lista_execution_time_sstf_ALEATORIA)
    print(f"Quantidade de seek média: {seek_media_sstf_aleatoria}")
    print(f"Tempo de execução médio: {execution_medio_sstf_aleatoria}")

    lista_seek_count_cscan_SEQUENCIAL = []
    lista_execution_time_cscan_SEQUENCIAL = []
    lista_seek_count_sstf_SEQUENCIAL = []
    lista_execution_time_sstf_SEQUENCIAL = []

    for lista in lista_requests_sequenciais:
        cscan = Cscan(lista, 500)
        _, seek_count_cscan, execution_time_cscan = cscan.execute()
        lista_seek_count_cscan_SEQUENCIAL.append(seek_count_cscan)
        lista_execution_time_cscan_SEQUENCIAL.append(execution_time_cscan)

        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_SEQUENCIAL.append(seek_count_sstf)
        lista_execution_time_sstf_SEQUENCIAL.append(execution_time_sstf)

    print("LISTAS SEQUENCIAIS")
    print("CSCAN")
    seek_media_cscan_sequencial = statistics.mean(lista_seek_count_cscan_SEQUENCIAL)
    execution_medio_cscan_sequencial = statistics.mean(lista_execution_time_cscan_SEQUENCIAL)
    print(f"Quantidade de seek média: {seek_media_cscan_sequencial}")
    print(f"Tempo de execução médio: {execution_medio_cscan_sequencial}")

    print("SSTF")
    seek_media_sstf_sequencial = statistics.mean(lista_seek_count_sstf_SEQUENCIAL)
    execution_medio_sstf_sequencial = statistics.mean(lista_execution_time_sstf_SEQUENCIAL)
    print(f"Quantidade de seek média: {seek_media_sstf_sequencial}")
    print(f"Tempo de execução médio: {execution_medio_sstf_sequencial}")

    histograma_medias(
        [statistics.mean(lista_seek_count_cscan_ALEATORIA), statistics.mean(lista_seek_count_cscan_SEQUENCIAL),
         statistics.mean(lista_seek_count_sstf_ALEATORIA), statistics.mean(lista_seek_count_sstf_SEQUENCIAL)],
        'Comparação de Quantidade de Seeks por Algoritmo e Tipo de Lista',
        'Média de Quantidade de Seeks',
        ['Aleatórias', 'Sequenciais']
    )


def main():
    start_choices = ["Iniciar", "Cancelar"]
    input_option_question = inquirer.List(
        "start",
        message="Análise de algoritmos de disco C-SCAN e SSTF",
        choices=start_choices)
    start_answer = inquirer.prompt([input_option_question]) or {}

    if start_answer.get("start") == "Cancelar":
        print("Operação cancelada pelo usuário.")
        exit()

    if start_answer.get("start") == "Iniciar":
        case_choices = ["Primeiro Caso", "Segundo Caso", "Terceiro Caso", "Cancelar"]
        input_case_question = inquirer.List(
            "case",
            message="Escolha um caso de estudo para executar:",
            choices=case_choices)
        case_answer = inquirer.prompt([input_case_question]) or {}

        if case_answer.get("case") == "Cancelar":
            print("Operação cancelada pelo usuário.")
            exit()
        elif case_answer.get("case") == "Primeiro Caso":
            primeiro_caso(True)
        elif case_answer.get("case") == "Segundo Caso":
            segundo_caso()
        elif case_answer.get("case") == "Terceiro Caso":
            terceiro_caso()


if __name__ == "__main__":
    main()
