
from datetime import datetime


def calculate_latency_cscan(seek_time):
    rotational_latency = 2
    transfer_time = 4 / 125
    total_latency = seek_time + rotational_latency + transfer_time
    return total_latency


class Cscan:
    def __init__(self,requests, head,name):
        self.head=head
        self.requests = requests
        self.name = name
        self.seek_sequence=[]
        self.seeks_progression = 0
        self.latency_progression = 0


    def cscan_internal(self):
        seek_count = 0
        distance = 0
        cur_track = self.head
        left = []
        right = []
        seek_sequence = []
        total_latency = 0
        disk_size = 1000

        seek_sequence.append(self.head)
        left.append(0)
        right.append(disk_size-1)

 
        for request in self.requests:
            if request < self.head:
                left.append(request)
            else:
                right.append(request)

      
        left.sort()
        right.sort()

        
        for i in range(len(right)):
            next_block = right[i]
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            seek_count += distance
            cur_track = next_block

        
        cur_track = 0
        seek_count += (disk_size - 1)

        
        for i in range(len(left)):
            next_block = left[i]
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            distance = abs(cur_track - self.head)
            seek_count += distance
            cur_track = next_block

        self.seek_sequence = seek_sequence
        self.seeks_progression = seek_count
        self.latency_progression = total_latency
    


















def CSCAN(requests_sequenciais, requests_aleatorio, start_position):
    #size = max(requests_sequenciais + requests_aleatorio) + 1  
    disk_size = 1000

    def cscan_internal(requests, head):
        seek_count = 0
        distance = 0
        cur_track = head
        left = []
        right = []
        seek_sequence = []
        total_latency = 0

        seek_sequence.append(head)
        left.append(0)
        right.append(disk_size-1)

 
        for request in requests:
            if request < head:
                left.append(request)
            else:
                right.append(request)

      
        left.sort()
        right.sort()

        
        for i in range(len(right)):
            next_block = right[i]
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            seek_count += distance
            cur_track = next_block

        
        cur_track = 0
        seek_count += (disk_size - 1)

        
        for i in range(len(left)):
            next_block = left[i]
            seek_sequence.append(next_block)
            seek_time= 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            distance = abs(cur_track - head)
            seek_count += distance
            cur_track = next_block

        return seek_sequence, seek_count, total_latency
    
    seek_sequence_sequenciais, total_seeks_sequenciais, total_latency_sequenciais = cscan_internal(requests_sequenciais, start_position)
    seek_sequence_aleatorio, total_seeks_aleatorio, total_latency_aleatorio = cscan_internal(requests_aleatorio, start_position)

    return seek_sequence_sequenciais , seek_sequence_aleatorio, total_latency_sequenciais, total_latency_aleatorio


