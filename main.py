import os
from os.path import isfile, join
from typing import List


import cscan
import inquirer

DATA_DIR = "data"


def save_to_file(seq: List[int]) -> str:
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
    if not os.path.exists(DATA_DIR): return []
    data_dir_content = os.listdir(DATA_DIR)
    data_files = [f for f in data_dir_content if isfile(join(DATA_DIR, f))]
    seqs = []
    for seq_file in data_files:
        with open(join(DATA_DIR, seq_file), "r") as f:
            seq = f.readline().replace("\n", "")
            seqs.append(f"{seq_file}: {seq}")
    return seqs



def main():
    choices = ["Usar sequências pré-selecionadas", "Cancelar"]
    input_option_question = inquirer.List(
        "input_option",
        message="Como deseja usar os dados?",
        choices=choices,
    )

    answer = inquirer.prompt([input_option_question])
    if answer.get("input_option") == choices[1]:
        print("Operação cancelada pelo usuário.")
        exit()
    
    # Ler os arquivos de sequência aqui
    with open("./data/lista_numeros_aleatorios.txt", "r") as f:
        lines = f.readlines()
        numbers_str = lines[0].strip()[1:-1].split(', ')
        requests_aleatorio = [int(num_str) for num_str in numbers_str]

    with open("./data/lista_numeros_sequenciais.txt", "r") as f:
        lines = f.readlines()
        numbers_str = lines[0].strip()[1:-1].split(', ')
        requests_sequenciais = [int(num_str) for num_str in numbers_str]

    # Chamada para a função CSCAN
    if answer.get("input_option") == choices[0]:
        print("C-SCAN:")
        x, y, z, w = cscan.CSCAN(
            requests_sequenciais, requests_aleatorio, 12)
        print("ESSE:", x, y, z, w)



if __name__ == "__main__":
    main()


