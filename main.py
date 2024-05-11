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

    cscan_ord = Cscan(requests_ord, 500)
    seek_sequence_cscan_ord, seek_count_cscan_ord, execution_time_cscan_ord = cscan_ord.execute()
    media_tempo_execucao_cscan_ord = statistics.mean(execution_time_cscan_ord)

    sstf_ord = Sstf(requests_ord, 500)
    seek_sequence_sstf_ord, seek_count_sstf_ord, execution_time_sstf_ord = sstf_ord.execute()
    media_tempo_execucao_sstf_ord = statistics.mean(execution_time_sstf_ord)

    cscan_aleat = Cscan(requests_aleat, 500)
    seek_sequence_cscan_aleat, seek_count_cscan_aleat, execution_time_cscan_aleat = cscan_aleat.execute()
    media_tempo_execucao_cscan_aleat = statistics.mean(execution_time_cscan_aleat)

    sstf_aleat = Sstf(requests_aleat, 500)
    seek_sequence_sstf_aleat, seek_count_sstf_aleat, execution_time_sstf_aleat = sstf_aleat.execute()
    media_tempo_execucao_sstf_aleat = statistics.mean(execution_time_sstf_aleat)

    if should_print_and_plot:
        print("C-SCAN lista ordenada:")
        print(f"Contagem de seeks: {seek_count_cscan_ord}")
        print(f"Média tempo de execução: {media_tempo_execucao_cscan_ord}\n")

        print("SSTF lista ordenada:")
        print(f"Contagem de seeks: {seek_count_sstf_ord}")
        print(f"Média tempo de execução: {media_tempo_execucao_sstf_ord}\n")

        print("C-SCAN lista aleatória:")
        print(f"Contagem de seeks: {seek_count_cscan_aleat}")
        print(f"Média tempo de execução: {media_tempo_execucao_cscan_aleat}\n")

        print("SSTF lista aleatória:")
        print(f"Contagem de seeks: {seek_count_sstf_aleat}")
        print(f"Média tempo de execução: {media_tempo_execucao_sstf_aleat}\n")

        plt.figure(figsize=(10, 5))
        plt.plot(seek_sequence_cscan_aleat, marker='o', color='purple')
        plt.title('Comportamento Circular do Algoritmo C-SCAN')
        plt.xlabel('Sequência de Requisições')
        plt.ylabel('Posição no Disco')
        plt.xticks(range(len(seek_sequence_cscan_aleat)), labels=seek_sequence_cscan_aleat)
        plt.grid(True)
        plt.show()

    return seek_count_cscan_ord, media_tempo_execucao_cscan_ord, seek_count_sstf_ord, media_tempo_execucao_sstf_ord, seek_count_cscan_aleat, media_tempo_execucao_cscan_aleat, seek_count_sstf_aleat, media_tempo_execucao_sstf_aleat


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


def plota_grafico_comparacao_execution_time(media_execution_time_cscan, media_execution_time_sstf, xlabel, ylabel,
                                            title):
    algorithms = ['C-SCAN', 'SSTF']
    execution_times_avg = [media_execution_time_cscan, media_execution_time_sstf]

    plt.figure(figsize=(10, 5))
    bars = plt.barh(algorithms, execution_times_avg, color=['purple', 'green'])

    for bar, value in zip(bars, execution_times_avg):
        plt.text(bar.get_width(), bar.get_y() + bar.get_height() / 2, f'{value:.4f}',
                 va='center', ha='left')

    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    plt.title(title)

    plt.subplots_adjust(left=0.1, right=0.9, top=0.9, bottom=0.2)
    plt.tight_layout()
    plt.show()


def segundo_caso():
    requests_aleat = [random.randint(0, 999) for _ in range(10000)]
    requests_ord = requests_aleat.copy()
    requests_ord.sort()

    seek_count_pq_cscan_ord, media_tempo_execucao_pq_cscan_ord, seek_count_pq_sstf_ord, media_tempo_execucao_pq_sstf_ord, seek_count_pq_cscan_aleat, media_tempo_execucao_pq_cscan_aleat, seek_count_pq_sstf_aleat, media_tempo_execucao_pq_sstf_aleat = primeiro_caso(
        False)

    cscan_ord = Cscan(requests_ord, 500)
    _, seek_count_gd_cscan_ord, execution_time_gd_cscan_ord = cscan_ord.execute()
    media_tempo_execucao_gd_cscan_ord = statistics.mean(execution_time_gd_cscan_ord)
    print("C-SCAN lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_cscan_ord}")
    print(f"Média tempo de execução: {media_tempo_execucao_gd_cscan_ord}\n")

    sstf_ord = Sstf(requests_ord, 500)
    _, seek_count_gd_sstf_ord, execution_time_gd_sstf_ord = sstf_ord.execute()
    media_tempo_execucao_gd_sstf_ord = statistics.mean(execution_time_gd_sstf_ord)
    print("SSTF lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_sstf_ord}")
    print(f"Média tempo de execução: {media_tempo_execucao_gd_sstf_ord}\n")

    plota_grafico_comparacao_seek_count(seek_count_pq_cscan_ord, seek_count_pq_sstf_ord, 'Quantidade de Seeks',
                                        'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista pequena e ordenada')
    plota_grafico_comparacao_execution_time(media_tempo_execucao_pq_cscan_ord, media_tempo_execucao_pq_sstf_ord,
                                            'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação da média do tempo de execução entre C-SCAN e SSTF para uma lista pequena e ordenada')

    plota_grafico_comparacao_seek_count(seek_count_gd_cscan_ord, seek_count_gd_sstf_ord, 'Quantidade de Seeks',
                                        'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista com 10 mil elementos e ordenada')
    plota_grafico_comparacao_execution_time(media_tempo_execucao_gd_cscan_ord, media_tempo_execucao_gd_sstf_ord,
                                            'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação da média do tempo de execução entre C-SCAN e SSTF para uma lista com 10 mil elementos e ordenada')

    cscan_aleat = Cscan(requests_aleat, 500)
    _, seek_count_gd_cscan_aleat, execution_time_gd_cscan_aleat = cscan_aleat.execute()
    media_tempo_gd_execucao_cscan_aleat = statistics.mean(execution_time_gd_cscan_aleat)
    print("C-SCAN lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_cscan_aleat}")
    print(f"Média tempo de execução: {media_tempo_gd_execucao_cscan_aleat}\n")

    sstf_aleat = Sstf(requests_aleat, 500)
    _, seek_count_gd_sstf_aleat, execution_time_gd_sstf_aleat = sstf_aleat.execute()
    media_tempo_gd_execucao_sstf_aleat = statistics.mean(execution_time_gd_sstf_aleat)
    print("SSTF lista ordenada 10 mil elementos:")
    print(f"Contagem de seeks: {seek_count_gd_sstf_aleat}")
    print(f"Média tempo de execução: {media_tempo_gd_execucao_sstf_aleat}\n")

    plota_grafico_comparacao_seek_count(seek_count_pq_cscan_aleat, seek_count_pq_sstf_aleat, 'Quantidade de Seeks',
                                        'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista pequena e aleatória')
    plota_grafico_comparacao_execution_time(media_tempo_execucao_pq_cscan_aleat, media_tempo_execucao_pq_sstf_aleat,
                                            'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação da média do tempo de execução entre C-SCAN e SSTF para uma lista pequena e aleatória')

    plota_grafico_comparacao_seek_count(seek_count_gd_cscan_aleat, seek_count_gd_sstf_aleat, 'Quantidade de Seeks',
                                        'Algoritmo',
                                        'Comparação da Contagem de Seeks entre C-SCAN e SSTF para uma lista com 10 mil elementos e aleatória')
    plota_grafico_comparacao_execution_time(media_tempo_gd_execucao_cscan_aleat, media_tempo_gd_execucao_sstf_aleat,
                                            'Tempo de execução (ms)',
                                            'Algoritmo',
                                            'Comparação da média do tempo de execução entre C-SCAN e SSTF para uma lista com 10 mil elementos e aleatória')


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
            ax.annotate('{:.4f}'.format(height),  # Formatação para duas casas decimais
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
        lista_execution_time_cscan_ALEATORIA.append(statistics.mean(execution_time_cscan))

        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_ALEATORIA.append(seek_count_sstf)
        lista_execution_time_sstf_ALEATORIA.append(statistics.mean(execution_time_sstf))

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
        lista_execution_time_cscan_SEQUENCIAL.append(statistics.mean(execution_time_cscan))

        sstf = Sstf(lista, 500)
        _, seek_count_sstf, execution_time_sstf = sstf.execute()
        lista_seek_count_sstf_SEQUENCIAL.append(seek_count_sstf)
        lista_execution_time_sstf_SEQUENCIAL.append(statistics.mean(execution_time_sstf))

    print("\nLISTAS SEQUENCIAIS")
    print("C-SCAN:")
    seek_media_cscan_sequencial = statistics.mean(lista_seek_count_cscan_SEQUENCIAL)
    execution_medio_cscan_sequencial = statistics.mean(lista_execution_time_cscan_SEQUENCIAL)
    print(f"Quantidade de seek média: {seek_media_cscan_sequencial}")
    print(f"Tempo de execução médio: {execution_medio_cscan_sequencial}")

    print("SSTF:")
    seek_media_sstf_sequencial = statistics.mean(lista_seek_count_sstf_SEQUENCIAL)
    execution_medio_sstf_sequencial = statistics.mean(lista_execution_time_sstf_SEQUENCIAL)
    print(f"Quantidade de seek média: {seek_media_sstf_sequencial}")
    print(f"Tempo de execução médio: {execution_medio_sstf_sequencial}")

    histograma_medias(
        [seek_media_cscan_aleatoria, seek_media_cscan_sequencial, seek_media_sstf_aleatoria,
         seek_media_sstf_sequencial],
        'Comparação de Quantidade de Seeks por Algoritmo e Tipo de Lista',
        'Média de Quantidade de Seeks',
        ['Aleatórias', 'Sequenciais']
    )

    histograma_medias(
        [execution_medio_cscan_aleatoria, execution_medio_cscan_sequencial, execution_medio_sstf_aleatoria,
         execution_medio_sstf_sequencial],
        'Comparação de Tempo de Execução por Algoritmo e Tipo de Lista',
        'Média de Tempo de Execução (ms)',
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
