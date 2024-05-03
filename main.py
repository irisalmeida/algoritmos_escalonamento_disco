import os
from os.path import isfile, join
from random import randint
from typing import List

import inquirer
import simpy

from algorithm import Algorithm

DATA_DIR = "data"



def save_to_file(seq: List[int]) -> str:
    """Save a number sequence to a file to be used later. The file name follows
    the pattern `seq_<count>`, where `count` is the number of the sequence."""
    try:
        os.makedirs(DATA_DIR)
    except FileExistsError:
        pass

    data_dir_content = os.listdir(DATA_DIR)
    data_files = [f for f in data_dir_content if isfile(join(DATA_DIR, f))]
    new_file_name = f"seq_{len(data_files)+1}.txt"
    with open(join(DATA_DIR, new_file_name), "w") as f:
        for num in seq:
            f.write(str(num))
            f.write(" ")
        f.write("\n")
    return new_file_name


def get_seq_files() -> List[str]:
    if not os.path.exists(DATA_DIR):
        return []
    data_dir_content = os.listdir(DATA_DIR)
    data_files = [f for f in data_dir_content if isfile(join(DATA_DIR, f))]
    seqs = []
    for seq_file in data_files:
        with open(join(DATA_DIR, seq_file), "r") as f:
            seq = f.readline().replace("\n", "")
            seqs.append(f"{seq_file}: {seq}")
    return seqs


def generate_seq(amount: int) -> List[int]:
    """Generate a list with <amount> random integer numbers."""
    seq = []
    count = 0
    while count < amount:
        num = randint(0, 100)
        if num not in seq:
            seq.append(num)
        count += 1
    return seq


def main():
    env = simpy.Environment()

    choices = ["Gerar sequência aleatória", "Escolher sequência",
               "Informar sequência", "Cancelar"]
    input_option_question = inquirer.List(
        "input_option",
        message="Como deseja usar os dados?",
        choices=choices,
    )
    questions = [input_option_question]
    answer: dict = inquirer.prompt(questions) or {}

    if answer.get("input_option") == choices[0]:
        seq = generate_seq(5)
        choices = ["Sim", "Não"]
        question = inquirer.List(
            "confirm_seq",
            message=f"Sequência aleatória gerada: {seq}. Confirmar?",
            choices=choices,
        )

        answer = inquirer.prompt([question]) or {}
        if answer.get("confirm_seq") == choices[0]:
            new_file = save_to_file(seq)
            print(f"Novo arquivo de sequência criado: {new_file}")
            env.process(run_simulation(env, seq))  
            env.run()  
            print("A execução continuará após a simulação terminar")

    elif answer.get("input_option") == choices[1]:
        seqs = get_seq_files()
        if not seqs:
            print("Erro ao ler sequências: diretório de dados não existe.")
            exit()

        choices = []
        for seq in seqs:
            choices.append(seq)

        print(choices)
        question = inquirer.List(
            "seq",
            message="Sequências disponíveis:",
            choices=choices
        )
        selected_seq = inquirer.prompt([question]) or {}
        selected_seq_name = selected_seq["seq"].split(":")[0].strip()
        selected_seq_values = [int(x) for x in selected_seq["seq"].split(":")[1].strip().split()]
        print(f"Utilizando sequência: {selected_seq_values}")

       
        use_cscan_question = inquirer.Confirm(
            "use_cscan",
            message="Deseja usar o algoritmo C-SCAN para simulação?"
        )
        use_cscan_answer = inquirer.prompt([use_cscan_question]) or {}
        if use_cscan_answer.get("use_cscan", False):
            print("Aguarde enquanto a simulação está em andamento...")
            env.process(run_simulation(env, selected_seq_values))  # Inicia a simulação com C-SCAN
            env.run()  
            print("A execução continuará após a simulação terminar")

        else:
            print("Simulação sem C-SCAN selecionada.")

    elif answer.get("input_option") == choices[2]:
        question = inquirer.Text(
            "seq",
            message="Informe a sequência de números desejada"
        )
        answer = inquirer.prompt([question]) or {}
        seq_str = answer.get("seq")
        seq = [int(x) for x in seq_str.split()]
        print(f"Utilizando sequência: {seq_str}.")
        new_file = save_to_file(seq)
        print(f"Nova sequência salva no arquivo: {new_file}")
        env.process(run_simulation(env, seq))  # Inicia a simulação
        env.run()  # Aguarda a simulação terminar
        print("A execução continuará após a simulação terminar")

    else:
        print("Cancelando ação.")
        exit()


def run_simulation(env, sequence):
    algorithm = Algorithm(env, sequence)
    for event in algorithm.cscan(): 
        yield event

    print("Total Access Time:", algorithm.total_access_time)
    print("Total Requests Serviced:", algorithm.total_requests_serviced)
    if algorithm.total_requests_serviced > 0:
        print("Average Response Time:", algorithm.total_access_time / algorithm.total_requests_serviced)
    else:
        print("Average Response Time: N/A")



if __name__ == "__main__":
    main()