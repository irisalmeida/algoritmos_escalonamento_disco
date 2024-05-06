
from datetime import datetime


def calculate_latency_cscan(seek_time):
    rotational_latency = 4 
    transfer_time = 4 / 400
    
    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency


def CSCAN(requests_sequenciais, requests_aleatorio, start_position):
    size = max(requests_sequenciais + requests_aleatorio) + 1  
    disk_size = 200

    def cscan_internal(requests, head):
        seek_count = 0
        distance = 0
        cur_track = head
        left = []
        right = []
        seek_sequence = []
        total_latency = 0

 
        for request in requests:
            if request < head:
                left.append(request)
            else:
                right.append(request)

      
        left.sort()
        right.sort()

        
        while right:
            
            next_block = right.pop(0)
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 4 != next_block // 4 else 0
            total_latency += calculate_latency_cscan(seek_time)
            seek_count += distance
            cur_track = next_block

        
        head = 0
        seek_count += (disk_size - 1)

        
        while left:
            next_block = left.pop(0)
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 4 != next_block // 4 else 0
            total_latency += calculate_latency_cscan(seek_time)
            distance = abs(cur_track - head)
            seek_count += distance
            cur_track = next_block

        return seek_sequence, seek_count, total_latency

    
    seek_sequence_sequenciais, total_seeks_sequenciais, total_latency_sequenciais = cscan_internal(requests_sequenciais, start_position)
    seek_sequence_aleatorio, total_seeks_aleatorio, total_latency_aleatorio = cscan_internal(requests_aleatorio, start_position)

    return seek_sequence_sequenciais , seek_sequence_aleatorio, total_latency_sequenciais, total_latency_aleatorio


