def calculate_latency(current_head_position, next_block, was_seek=False):
    rotational_latency = 4  # 4ms de tempo de rotação
    transfer_time = 4 / 400  # Tempo de transferência de 4KB a 400MB/s

    if was_seek or current_head_position // 4 != next_block // 4:
        seek_time = 4  # 4ms de tempo de busca
    else:
        seek_time = 0  # Não há tempo de busca se estiver na mesma trilha

    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency


class CScan:
    def __init__(self, requests, head, name):
        self.head = head
        self.requests = requests
        self.name = name
        self.total_seeks = 0
        self.total_latency = 0
        self.seeks_progression = []
        self.latency_progression = []
        self.disk_size = 1000

    def execute(self):
        # Requests à direita da cabeça
        right = [r for r in self.requests if r >= self.head]
        # Requests à esquerda da cabeça
        left = [r for r in self.requests if r < self.head]

        # Processar requests à direita
        for request in right:
            self.process_request(request)

        # Simula mover a cabeça para o início do disco
        self.total_seeks += self.disk_size - self.head
        self.head = 0

        # Processar requests à esquerda
        for request in left:
            self.process_request(request)

    def process_request(self, request):
        was_seek = self.head // 4 != request // 4
        self.total_latency += calculate_latency(self.head, request, was_seek)
        self.latency_progression.append(self.total_latency)
        self.total_seeks += abs(self.head - request)
        self.head = request
        self.seeks_progression.append(self.total_seeks)
