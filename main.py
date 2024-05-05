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
    input_option_question = inquirer.List(  # Question for user input
            "input_option",
            message="Como deseja usar os dados?",
            choices=choices,
        )
    
    answer = inquirer.prompt([input_option_question])

    if answer.get("input_option") == choices[1]:  # Cancelar
        print("Operação cancelada pelo usuário.")
        exit()

    seqs = get_seq_files()
    if not seqs:
        print("Erro ao ler sequências: diretório de dados não existe.")
        exit()

    if answer.get("input_option") == choices[0]:
        print("C-SCAN:")
        # Use lista_numeros_aleatorios.txt
        path_sequenciais, path_aleatorio = cscan.CSCAN(cscan.requests_sequenciais, cscan.requests_aleatorio, 6)



        # Use lista_numeros_aleatorios.txt
        sequence, total_seeks, total_latency = cscan.cscan_with_latency(cscan.requests_aleatorio, 6)
        print("Tempo total de latência (aleatório):", total_latency, "ms")

        # Use lista_numeros_sequenciais.txt
        sequence, total_seeks, total_latency = cscan.cscan_with_latency(cscan.requests_sequenciais, 6)
        print("Tempo total de latência (sequencial):", total_latency, "ms")

        """print("Caminho para solicitações sequenciais:", path_sequenciais)
        print("-------------------------")
        print("Caminho para solicitações aleatórias:", path_aleatorio)
        """


if __name__ == "__main__":
    main()


