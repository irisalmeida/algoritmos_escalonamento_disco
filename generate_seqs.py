import random

def generate_reqs(n):
    return random.sample(range(0, 10000), n)


amount = range(5, 9005, 50)

for a in amount:
    reqs = generate_reqs(a)
    with open("data/reqs_aleatorias.txt", "a") as f:
        f.writelines(str(reqs))
        f.writelines("\n")

    with open("data/reqs_sequenciais.txt", "a") as f:
        reqs.sort()
        f.writelines(str(reqs))
        f.writelines("\n")


