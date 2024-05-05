import time
import random

def calculate_latency_fscan(current_head_position, next_block, was_seek=False):
    rotational_latency = 4  # 4ms de tempo de rotação
    transfer_time = 4 / 400  # Tempo de transferência de 4KB a 400MB/s

    if was_seek or current_head_position // 4 != next_block // 4:
        seek_time = 4  # 4ms de tempo de busca
    else:
        seek_time = 0  # Não há tempo de busca se estiver na mesma trilha

    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency

class FScan:
    def __init__(self, initial_head_position, total_requests, max_queue_size):
        self.current_head_position = initial_head_position
        self.active_queue = []
        self.max_queue_size = max_queue_size
        self.total_requests = total_requests
        self.total_seeks = 0
        self.total_latency = 0

    def setup_queues(self):
        while self.total_requests and len(self.active_queue) < self.max_queue_size:
            self.active_queue.append(self.total_requests.pop(0))

    def execute(self):
        self.setup_queues()

        while self.active_queue:
            next_most = min(self.active_queue, key=lambda x: abs(
                x - self.current_head_position))  # pega o primeiro menor setor mais próximo de onde está a cabeça
            # define direção de serviço das requests
            index = self.active_queue.index(next_most)
            if next_most >= self.current_head_position:  # defini que se for igual a cabeça, a direção é pra cima, atender as reqs acima
                while index < len(self.active_queue):
                    if self.active_queue[index] >= self.current_head_position:
                        self.process_request(self.active_queue[index])
                        was_seek = self.current_head_position // 4 != self.active_queue[index] // 4
                        self.total_seeks += 1 if was_seek else 0
                        self.total_latency += calculate_latency_fscan(self.current_head_position, self.active_queue[index], was_seek)
                        self.current_head_position = self.active_queue[index]
                        self.active_queue.pop(index)
                    else:
                        index += 1
            else:
                for i in range(index, -1, -1):
                    if self.active_queue[i] < self.current_head_position:
                        self.process_request(self.active_queue[i])
                        was_seek = self.current_head_position // 4 != self.active_queue[i] // 4
                        self.total_seeks += 1 if was_seek else 0
                        self.total_latency += calculate_latency_fscan(self.current_head_position, self.active_queue[i], was_seek)
                        self.current_head_position = self.active_queue[i]
                        self.active_queue.pop(i)

            if not self.active_queue and self.total_requests:
                self.waiting_queue_to_active()

    def waiting_queue_to_active(self):
        self.setup_queues()

    def process_request(self, request):
        print(f"Processando request {request}. Posição atual do cabeçote: {self.current_head_position}")

# # Exemplo de uso
# initial_head_position = 50
# total_requests = [10, 20, 30, 40, 60, 70, 80]
# max_queue_size = 3
#
# fscan = FScan(initial_head_position, total_requests, max_queue_size)
# fscan.execute()
#
# print(f"Total de seeks: {fscan.total_seeks}")
# print(f"Total de latência: {fscan.total_latency} ms")
#
#
# class FScan:
#     def __init__(self, initial_head_position, total_requests, max_queue_size):
#         self.current_head_position = initial_head_position
#         self.active_queue = []
#         self.max_queue_size = max_queue_size
#         self.total_requests = total_requests
#
#     def setup_queues(self):
#         while self.total_requests and len(self.active_queue) < self.max_queue_size:
#             self.active_queue.append(self.total_requests.pop(0))
#
#     def execute(self):
#         self.setup_queues()
#
#         while self.active_queue:
#             next_most = min(self.active_queue, key=lambda x: abs(
#                 x - self.current_head_position))  # pega o primeiro menor setor mais próximo de onde está a cabeça
#             # define direção de serviço das requests
#             index = self.active_queue.index(next_most)
#             if next_most >= self.current_head_position:  # defini que se for igual a cabeça, a direção é pra cima, atender as reqs acima
#                 while index < len(self.active_queue):
#                     if self.active_queue[index] >= self.current_head_position:
#                         self.process_request(self.active_queue[index])
#                         self.current_head_position = self.active_queue[index]
#                         self.active_queue.pop(index)
#                     else:
#                         index += 1
#             else:
#                 for i in range(index, -1, -1):
#                     if self.active_queue[i] < self.current_head_position:
#                         self.process_request(self.active_queue[i])
#                         self.current_head_position = self.active_queue[i]
#                         self.active_queue.pop(i)
#
#             if not self.active_queue and self.total_requests:
#                 self.waiting_queue_to_active()
#
#     def waiting_queue_to_active(self):
#         self.setup_queues()
#
#     def process_request(self, request):
#         print(f"Processando request {request}. Posição atual do cabeçote: {self.current_head_position}")


# Sequenciais
#requests = [10, 20, 30, 40, 45, 60, 70, 80, 90]
#requests = [47, 52, 57, 60, 64, 82, 93, 96, 113, 119, 135, 137, 183, 185, 190, 199, 203, 221, 233, 237, 242, 277, 292, 312, 347, 358, 364, 378, 379, 382, 444, 447, 456, 476, 481, 489, 490, 506, 541, 543, 550, 564, 569, 572, 576, 588, 589, 595, 597, 607, 611, 630, 630, 632, 640, 662, 666, 670, 690, 724, 734, 738, 746, 764, 769, 773, 777, 781, 795, 801, 803, 820, 831, 842, 848, 855, 858, 862, 864, 870, 871, 874, 877, 878, 890, 903, 908, 912, 930, 935, 937, 948, 963, 976, 983, 991, 998]
requests = list(range(10000)) #66.47467613220215 ms
active_list_size = 5
fscan = FScan(initial_head_position=50, total_requests=requests, max_queue_size=active_list_size)
before = time.time()
fscan.execute()
after = time.time()
tempo_de_execucao = (after - before) * 1000

# Aleatórias
#requests_sh = [40, 10, 45, 70, 30, 90, 80, 60, 20]
#requests_sh = [481, 862, 379, 113, 572, 632, 82, 277, 185, 983, 890, 864, 589, 119, 476, 877, 456, 190, 607, 60, 746, 242, 903, 724, 908, 378, 666, 858, 382, 781, 199, 991, 347, 183, 912, 963, 662, 358, 842, 597, 489, 935, 937, 611, 820, 52, 543, 630, 795, 734, 690, 803, 878, 630, 292, 564, 640, 764, 930, 871, 576, 137, 801, 364, 447, 93, 777, 135, 998, 588, 848, 773, 64, 550, 57, 221, 738, 569, 595, 976, 233, 444, 47, 870, 96, 874, 855, 948, 831, 541, 490, 769, 312, 237, 203, 506, 584, 670]
requests_sh = list(range(10000))
random.shuffle(requests_sh) #96.91786766052246 ms
fscan_sh = FScan(initial_head_position=50, total_requests=requests_sh, max_queue_size=active_list_size)
before_sh = time.time()
fscan_sh.execute()
after_sh = time.time()
tempo_de_execucao_sh = (after_sh - before_sh) * 1000
print("Ordenado")
print("Tempo de execucao: ", tempo_de_execucao, "ms")
print(f"Total de seeks: {fscan.total_seeks}")
print(f"Total de latência: {fscan.total_latency} ms")

print("Aleatorio")
print("Tempo de execucao: ", tempo_de_execucao_sh, "ms")
print(f"Total de seeks: {fscan_sh.total_seeks}")
print(f"Total de latência: {fscan_sh.total_latency} ms")
