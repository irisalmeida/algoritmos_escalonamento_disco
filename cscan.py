
from datetime import datetime

with open("./data/lista_numeros_aleatorios.txt", "r") as f:
    lines = f.readlines()
    numbers_str = lines[0].strip()[1:-1].split(', ')
    requests_aleatorio = [int(num_str) for num_str in numbers_str]

with open("./data/lista_numeros_sequenciais.txt", "r") as f:
    lines = f.readlines()
    numbers_str = lines[0].strip()[1:-1].split(', ')
    requests_sequenciais = [int(num_str) for num_str in numbers_str]


def CSCAN(requests, start_position):

        path = ''
        for i in range(start_position, len(requests)):
            path += str(requests[i]) + '->'

        for i in range(0, start_position):
            path += str(requests[i]) + '->'

        return path


def calculate_latency_cscan(current_block, target_block, was_seek=False):
    rotational_latency = 4  
    transfer_time = 4 / 400  
    
    if was_seek or current_block // 4 != target_block // 4:
        seek_time = 4  
    else:
        seek_time = 0  
    
    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency


def cscan_with_latency(requests, start_block):

    cscan_path = CSCAN(requests, start_block)

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

        was_seek = current_block // 4 != next_block // 4  
        total_seeks += 1 if was_seek else 0
        total_latency += calculate_latency_cscan(current_block, next_block, was_seek)
        sequence.append(next_block)
        current_block = next_block

        requests.remove(next_block)  

    return sequence, total_seeks, total_latency



"""

Correção futura:
-chamada para CSCAN e a atribuição do caminho resultante, mas não a está usando para nada
-dois tipos diferentes de solicitações (requests) não são passadas como argumento para a função CSCAN(corrigir em todo código)
"""

