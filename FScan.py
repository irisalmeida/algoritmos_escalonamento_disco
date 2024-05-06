import time
import random
import matplotlib.pyplot as plt


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
    def __init__(self, initial_head_position, total_requests, max_queue_size, name):
        self.name = name
        self.current_head_position = initial_head_position
        self.active_queue = []
        self.max_queue_size = max_queue_size
        self.total_requests = total_requests
        self.total_seeks = 0
        self.total_latency = 0
        self.latency_progression = []
        self.seeks_progression = []
        self.execution_time = 0

    def setup_queues(self):
        while self.total_requests and len(self.active_queue) < self.max_queue_size:
            self.active_queue.append(self.total_requests.pop(0))

    def execute(self):
        before = time.time()

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
                        self.total_latency += calculate_latency_fscan(self.current_head_position,
                                                                      self.active_queue[index], was_seek)
                        self.current_head_position = self.active_queue[index]
                        self.active_queue.pop(index)
                        self.latency_progression.append(self.total_latency)
                        self.seeks_progression.append(self.total_seeks)
                    else:
                        index += 1
            else:
                for i in range(index, -1, -1):
                    if self.active_queue[i] < self.current_head_position:
                        self.process_request(self.active_queue[i])
                        was_seek = self.current_head_position // 4 != self.active_queue[i] // 4
                        self.total_seeks += 1 if was_seek else 0
                        self.total_latency += calculate_latency_fscan(self.current_head_position, self.active_queue[i],
                                                                      was_seek)
                        self.current_head_position = self.active_queue[i]
                        self.active_queue.pop(i)
                        self.latency_progression.append(self.total_latency)
                        self.seeks_progression.append(self.total_seeks)

            if not self.active_queue and self.total_requests:
                self.waiting_queue_to_active()

        after = time.time()
        self.execution_time = (after - before) * 1000

    def waiting_queue_to_active(self):
        self.setup_queues()

    def process_request(self, request):
        print(f"Processando request {request}. Posição atual do cabeçote: {self.current_head_position}")
