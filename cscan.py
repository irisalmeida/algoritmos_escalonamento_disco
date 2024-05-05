
from datetime import datetime

with open("./data/lista_numeros_aleatorios.txt", "r") as f:
    lines = f.readlines()
    numbers_str = lines[0].strip()[1:-1].split(', ')
    requests_aleatorio = [int(num_str) for num_str in numbers_str]

with open("./data/lista_numeros_sequenciais.txt", "r") as f:
    lines = f.readlines()
    numbers_str = lines[0].strip()[1:-1].split(', ')
    requests_sequenciais = [int(num_str) for num_str in numbers_str]


def generate_path(requests, start_position):
    path = []

    # Percorre os blocos a partir da posição inicial até o final da lista de solicitações
    for i in range(start_position, len(requests)):
        path.append(requests[i])

    # Percorre os blocos do início até a posição inicial
    for i in range(0, start_position):
        path.append(requests[i])

    return path


def CSCAN(requests_sequenciais, requests_aleatorio, start_position):
    path_sequenciais = generate_path(requests_sequenciais, start_position)
    path_aleatorio = generate_path(requests_aleatorio, start_position)

    return path_sequenciais, path_aleatorio



def calculate_latency_cscan(current_block, target_block, was_seek=False):
    rotational_latency = 2  
    transfer_time = 4 / 125  
    
    if was_seek or current_block // 8 != target_block // 8:
        seek_time = 4  
    else:
        seek_time = 0  
    
    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency


def cscan_with_latency(requests, start_block):
    cscan_path = generate_path(requests, start_block)

    current_block = start_block
    total_seeks = 0
    total_latency = 0
    sequence = []

    requests.sort()  

    while requests:
        next_block = None
      
        for block in requests:
            if block >= current_block:
                next_block = block
                break
        
        if next_block is None:
            next_block = requests[0]

        was_seek = current_block // 8 != next_block // 8 
        total_seeks += 1 if was_seek else 0
        # Aqui, em vez de calcular o caminho novamente, usamos o caminho gerado anteriormente
        total_latency += calculate_latency_cscan(current_block, next_block, was_seek) #passa o  cscan_path??
        sequence.append(next_block)
        current_block = next_block

        requests.remove(next_block)  

    return sequence, total_seeks, total_latency


