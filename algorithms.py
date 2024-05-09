from typing import Tuple, List
import time


class Cscan():
    def __init__(self, requests, start_position) -> None:
        self.disk_size = 1000
        self.requests = requests
        self.start_position = start_position
        self.seek_count = 0
        self.left = []
        self.right = []
        self.seek_sequence = []
        self.execution_time = 0


    def execute(self) -> Tuple[List[int], int]:
        before = time.time()
        self.left.append(0)
        self.right.append(self.disk_size - 1)
        for request in self.requests:
            if request < self.start_position:
                self.left.append(request)
            else:
                self.right.append(request)
        self.left.sort()
        self.right.sort()

        cur_pos = self.start_position
        self.seek_sequence.append(cur_pos)

        for next_pos in self.right:
            self.seek_sequence.append(next_pos)
            delta_distance = abs(cur_pos - next_pos)
            self.seek_count += delta_distance
            cur_pos = next_pos

        cur_pos = 0
        self.seek_count += (self.disk_size - 1)

        for next_pos in self.left:
            self.seek_sequence.append(next_pos)
            delta_distance = abs(cur_pos - next_pos)
            self.seek_count += delta_distance
            cur_pos = next_pos

        after = time.time()
        self.execution_time = (after - before) * 1000

        return self.seek_sequence, self.seek_count, self.execution_time


class Sstf():
    def __init__(self, requests, start_position) -> None:
        self.disk_size = 1000
        self.requests = requests
        self.start_position = start_position
        self.seek_count = 0
        self.left = []
        self.right = []
        self.seek_sequence = []
        self.execution_time = 0


    def execute(self):
            before = time.time()
            l = len(self.requests)
            diff = [0] * l

            for i in range(l):
                diff[i] = [0, 0]

            seek_count = 0


            seek_sequence = [0] * (l + 1)

            head = self.start_position
            for i in range(l):
                seek_sequence[i] = head
                Sstf.calculateDifference(self.requests, head, diff)
                index = Sstf.findMin(diff)

                diff[index][1] = True


                seek_count += diff[index][0]

                head = self.requests[index]


            seek_sequence[len(seek_sequence) - 1] = head
            after = time.time()
            self.execution_time = (after - before) * 1000

            return seek_sequence, seek_count, self.execution_time



    @staticmethod
    def calculateDifference(queue, head, diff):
        for i in range(len(diff)):
            diff[i][0] = abs(queue[i] - head)

    @staticmethod
    def findMin(diff):

        index = -1
        minimum = 999999999

        for i in range(len(diff)):
            if (not diff[i][1] and
                    minimum > diff[i][0]):
                minimum = diff[i][0]
                index = i
        return index