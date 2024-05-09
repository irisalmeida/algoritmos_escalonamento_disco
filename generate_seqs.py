import random
import random

import inquirer
import matplotlib.pyplot as plt
import statistics

import numpy as np
from algorithms import Cscan, Sstf
import generate_seqs



def generate_reqs(n):
    return random.sample(range(0, 1000), n)

amount = range(5, 905, 50)

for a in amount:
    reqs = generate_reqs(a)
    with open("data/reqs_aleatorias.txt", "a") as f:
        f.writelines(str(reqs))
        f.writelines("\n")

    with open("data/reqs_sequenciais.txt", "a") as f:
        reqs.sort()
        f.writelines(str(reqs))
        f.writelines("\n")



