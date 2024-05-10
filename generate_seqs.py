import random


def generate_reqs(n):
    return random.sample(range(0, 1000), n)


open("data/reqs_aleatorias.txt", "w").close()
open("data/reqs_sequenciais.txt", "w").close()

amount = range(5, 905, 50)

for _ in range(56):
    for a in amount:
        reqs = generate_reqs(a)
        with open("data/reqs_aleatorias.txt", "a") as f:
            f.writelines(str(reqs) + "\n")

        with open("data/reqs_sequenciais.txt", "a") as f:
            reqs.sort()
            f.writelines(str(reqs) + "\n")
