class Algorithm:
    def __init__(self, env, sequence):
        self.env = env
        self.sequence = sequence  # Sequência não ordenada
        self.head_position = 0
        self.direction = 'up'
        self.total_access_time = 0
        self.total_requests_serviced = 0

    def cscan(self):
        remaining_sectors = list(self.sequence)  # Cria uma cópia da sequência original
        while remaining_sectors:  # Continua enquanto houver setores restantes
            if self.direction == 'up':
                for sector in self.sequence:
                    if sector >= self.head_position:
                        yield self.env.timeout(1)
                        self.total_access_time += 1
                        if sector in remaining_sectors:
                            print(f"Atendendo requisição no setor {sector}")
                            remaining_sectors.remove(sector)
                            self.total_requests_serviced += 1
                self.head_position = 0
                self.direction = 'down'
                yield self.env.timeout(1)  # Adicionando yield para permitir avançar a execução
            elif self.direction == 'down':
                for sector in reversed(self.sequence):
                    if sector <= self.head_position:
                        yield self.env.timeout(1)
                        self.total_access_time += 1
                        if sector in remaining_sectors:
                            print(f"Atendendo requisição no setor {sector}")
                            remaining_sectors.remove(sector)
                            self.total_requests_serviced += 1
                self.head_position = 99
                self.direction = 'up'
                yield self.env.timeout(1)  # Adicionando yield para permitir avançar a execução
