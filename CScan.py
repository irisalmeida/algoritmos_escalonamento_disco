def calculate_latency_cscan(seek_time):
    rotational_latency = 2
    transfer_time = 4 / 125
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
        self.execution_time = 0

    def execute(self):
        distance = 0
        left = []
        right = []
        disk_size = 1000

        self.seeks_progression.append(self.head)
        left.append(0)
        right.append(disk_size - 1)

        for request in self.requests:
            if request < self.head:
                left.append(request)
            else:
                right.append(request)

        left.sort()
        right.sort()

        for i in range(len(right)):
            next_block = right[i]
            self.seeks_progression.append(next_block)
            seek_time = 4 if self.head // 8 != next_block // 8 else 0
            self.total_latency += calculate_latency_cscan(seek_time)
            self.latency_progression.append(self.total_latency)
            self.total_seeks += distance
            self.seeks_progression.append(self.total_seeks)
            self.head = next_block

        self.head = 0
        self.total_seeks += (disk_size - 1)

        for i in range(len(left)):
            next_block = left[i]
            self.seeks_progression.append(next_block)
            seek_time = 4 if self.head // 8 != next_block // 8 else 0
            self.total_latency += calculate_latency_cscan(seek_time)
            self.latency_progression.append(self.total_latency)
            distance = abs(self.head - self.head)
            self.total_seeks += distance
            self.head = next_block
            self.seeks_progression.append(self.total_seeks)


def CSCAN(requests_sequenciais, requests_aleatorio, start_position):
    # size = max(requests_sequenciais + requests_aleatorio) + 1
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
        right.append(disk_size - 1)

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
            seek_time = 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            seek_count += distance
            cur_track = next_block

        cur_track = 0
        seek_count += (disk_size - 1)

        for i in range(len(left)):
            next_block = left[i]
            seek_sequence.append(next_block)
            seek_time = 4 if cur_track // 8 != next_block // 8 else 0
            total_latency += calculate_latency_cscan(seek_time)
            distance = abs(cur_track - head)
            seek_count += distance
            cur_track = next_block

        return seek_sequence, seek_count, total_latency

    seek_sequence_sequenciais, total_seeks_sequenciais, total_latency_sequenciais = cscan_internal(requests_sequenciais,
                                                                                                   start_position)
    seek_sequence_aleatorio, total_seeks_aleatorio, total_latency_aleatorio = cscan_internal(requests_aleatorio,
                                                                                             start_position)

    return seek_sequence_sequenciais, seek_sequence_aleatorio, total_latency_sequenciais, total_latency_aleatorio
