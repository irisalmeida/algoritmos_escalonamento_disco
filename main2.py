import random
import matplotlib.pyplot as plt
from FScan import FScan
from CScan import CScan
import CScan2


def gerar_graficos(algoritmo1, algoritmo2):
    # Plotar gráficos de progressão de latência e seeks
    plt.figure(figsize=(18, 6))

    plt.subplot(1, 3, 1)
    plt.plot(range(1, len(algoritmo1.latency_progression) + 1), algoritmo1.latency_progression, marker='o',
             color='blue', linestyle='-', linewidth=2, label=algoritmo1.name)
    plt.plot(range(1, len(algoritmo2.latency_progression) + 1), algoritmo2.latency_progression, marker='s', color='red',
             linestyle='--', linewidth=2, label=algoritmo2.name)
    plt.xlabel('Número de Requisições')
    plt.ylabel('Latência Acumulada (ms)')
    plt.title('Progressão da Latência para Lista de Requisições')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 2)
    plt.plot(range(1, len(algoritmo1.seeks_progression) + 1), algoritmo1.seeks_progression, marker='o', color='blue',
             linestyle='-', linewidth=2, label=algoritmo1.name)
    plt.plot(range(1, len(algoritmo2.seeks_progression) + 1), algoritmo2.seeks_progression, marker='s', color='red',
             linestyle='--', linewidth=2, label=algoritmo2.name)
    plt.xlabel('Número de Requisições')
    plt.ylabel('Número de Seeks')
    plt.title('Progressão do Número de Seeks para Lista de Requisições')
    plt.legend()
    plt.grid(True)

    plt.subplot(1, 3, 3)
    plt.plot(algoritmo1.latency_progression, algoritmo1.seeks_progression, marker='o', color='blue', linestyle='-',
             linewidth=2, label=algoritmo1.name)
    plt.plot(algoritmo2.latency_progression, algoritmo2.seeks_progression, marker='s', color='red', linestyle='--',
             linewidth=2, label=algoritmo2.name)
    plt.xlabel('Latência Acumulada (ms)')
    plt.ylabel('Número de Seeks')
    plt.title('Número de Seeks vs. Latência')
    plt.legend()
    plt.grid(True)

    plt.tight_layout()
    plt.show()


def main():
    # Listas Sequenciais
    requests_sm = [10, 20, 30, 40, 45, 60, 70, 80, 90]
    requests_md = [47, 52, 57, 60, 64, 82, 93, 96, 113, 119, 135, 137, 183, 185, 190, 199, 203, 221, 233, 237, 242, 277,
                   292, 312, 347, 358, 364, 378, 379, 382, 444, 447, 456, 476, 481, 489, 490, 506, 541, 543, 550, 564,
                   569, 572, 576, 588, 589, 595, 597, 607, 611, 630, 630, 632, 640, 662, 666, 670, 690, 724, 734, 738,
                   746, 764, 769, 773, 777, 781, 795, 801, 803, 820, 831, 842, 848, 855, 858, 862, 864, 870, 871, 874,
                   877, 878, 890, 903, 908, 912, 930, 935, 937, 948, 963, 976, 983, 991, 998]
    requests_bg = list(range(10000))

    # Listas Aleatórias
    requests_sm_sh = [40, 10, 45, 70, 30, 90, 80, 60, 20]
    requests_md_sh = [481, 862, 379, 113, 572, 632, 82, 277, 185, 983, 890, 864, 589, 119, 476, 877, 456, 190, 607, 60,
                      746, 242, 903, 724, 908, 378, 666, 858, 382, 781, 199, 991, 347, 183, 912, 963, 662, 358, 842,
                      597, 489, 935, 937, 611, 820, 52, 543, 630, 795, 734, 690, 803, 878, 630, 292, 564, 640, 764, 930,
                      871, 576, 137, 801, 364, 447, 93, 777, 135, 998, 588, 848, 773, 64, 550, 57, 221, 738, 569, 595,
                      976, 233, 444, 47, 870, 96, 874, 855, 948, 831, 541, 490, 769, 312, 237, 203, 506, 584, 670]
    requests_bg_sh = list(range(10000))
    random.shuffle(requests_bg_sh)

    # # CScan
    # cscan = CScan2.CScan(requests=requests_bg, head=50, name="CScan para lista ordenada")
    # cscan.execute()
    #
    # cscan_sh = CScan2.CScan(requests=requests_bg_sh, head=50, name="CScan para lista aleatória")
    # cscan_sh.execute()
    # print("Ordenado")
    # # print("Tempo de execucao: ", fscan.execution_time, "ms") # adicionar nome do algoritmo aqui e embaixo
    # print(f"Total de seeks: {cscan.total_seeks}")
    # print(f"Total de latência: {cscan.total_latency} ms")
    #
    # print("Aleatorio")
    # # print("Tempo de execucao: ", fscan_sh.execution_time, "ms")
    # print(f"Total de seeks: {cscan_sh.total_seeks}")
    # print(f"Total de latência: {cscan_sh.total_latency} ms")
    # gerar_graficos(cscan, cscan_sh)

    # # FScan
    # active_list_size = 5
    # fscan = FScan(initial_head_position=50, total_requests=requests_bg, max_queue_size=active_list_size, name="FScan para lista ordenada")
    # fscan.execute()
    #
    # fscan_sh = FScan(initial_head_position=50, total_requests=requests_bg_sh, max_queue_size=active_list_size, name="FScan para lista aleatória")
    # fscan_sh.execute()
    # print("Ordenado")
    # print("Tempo de execucao: ", fscan.execution_time, "ms") # adicionar nome do algoritmo aqui e embaixo
    # print(f"Total de seeks: {fscan.total_seeks}")
    # print(f"Total de latência: {fscan.total_latency} ms")
    #
    # print("Aleatorio")
    # print("Tempo de execucao: ", fscan_sh.execution_time, "ms")
    # print(f"Total de seeks: {fscan_sh.total_seeks}")
    # print(f"Total de latência: {fscan_sh.total_latency} ms")
    # gerar_graficos(fscan, fscan_sh)

    # CScan vs FScan
    active_list_size = 5
    fscan = FScan(initial_head_position=50, total_requests=requests_bg.copy(), max_queue_size=active_list_size, name="FScan para lista ordenada")
    fscan.execute()

    fscan_sh = FScan(initial_head_position=50, total_requests=requests_bg_sh.copy(), max_queue_size=active_list_size, name="FScan para lista aleatória")
    fscan_sh.execute()
    print(fscan.name)
    print(f"Tempo de execucao: {fscan.execution_time} ms")
    print(f"Total de seeks: {fscan.total_seeks}")
    print(f"Total de latência: {fscan.total_latency} ms")

    print(fscan_sh.name)
    print(f"Tempo de execucao: {fscan_sh.execution_time} ms")
    print(f"Total de seeks: {fscan_sh.total_seeks}")
    print(f"Total de latência: {fscan_sh.total_latency} ms")

    cscan = CScan2.CScan(requests=requests_bg.copy(), head=50, name="CScan para lista ordenada")
    cscan.execute()

    cscan_sh = CScan2.CScan(requests=requests_bg_sh.copy(), head=50, name="CScan para lista aleatória")
    cscan_sh.execute()
    print(cscan.name)
    # print("Tempo de execucao: ", fscan.execution_time, "ms")
    print(f"Total de seeks: {cscan.total_seeks}")
    print(f"Total de latência: {cscan.total_latency} ms")

    print(cscan_sh.name)
    # print("Tempo de execucao: ", fscan_sh.execution_time, "ms")
    print(f"Total de seeks: {cscan_sh.total_seeks}")
    print(f"Total de latência: {cscan_sh.total_latency} ms")

    # gerar_graficos(fscan, cscan)
    gerar_graficos(fscan_sh, cscan_sh)


if __name__ == "__main__":
    main()
