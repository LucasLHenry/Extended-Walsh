from bmatrix import BMatrix
import walshlib
from itertools import product
import configparser
from collections import namedtuple
import list_functions
from matrix_functions import *
import os

try:
    config = configparser.ConfigParser()
    config.read("./config.ini")
    seed_size = int(config["config"]["SeedSize"])
    pattern_size = int(config["config"]["PatternSize"])
    allow_non_square = False if config["config"]["AllowNonSquare"].upper() == "NO" else True
    order = int(config["config"]["Order"])
    file_type = config["config"]["OutputFileType"]
    output_folder = config["config"]["OutputPath"]
except ValueError:
    raise ValueError("config parameters of incorrect type")
except KeyError:
    raise ValueError("missing parameter from config file / config file not found")

if file_type.upper() not in ["JPG", "PNG"]:
    raise ValueError("config error: only png and jpg file types allowed")
else:
    file_type = file_type.lower()


def generate_possible_matrices(size: int):
    yield from product(product([True, False], repeat=size), repeat=size)


def printProgressBar(iteration, total, prefix='', suffix='', decimals=1, length=100, fill='█', printEnd="\r"):
    """
    Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        length      - Optional  : character length of bar (Int)
        fill        - Optional  : bar fill character (Str)
        printEnd    - Optional  : end character (e.g. "\r", "\r\n") (Str)
    """
    percent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {percent}% {suffix}', end=printEnd)
    # Print New Line on Complete
    if iteration == total:
        print()


folder_name = output_folder + f"_s{seed_size}p{pattern_size}_o{order}"
os.makedirs(folder_name, exist_ok=True)
os.chdir(folder_name)

file_count = 0
total_seeds = 2 ** (seed_size ** 2)
total_patterns = 2 ** (pattern_size ** 2)
total_files = total_seeds * total_patterns

for seed in generate_possible_matrices(seed_size):
    seed_mat = BMatrix(list_functions.tuple_to_list(seed))
    for pattern in generate_possible_matrices(pattern_size):
        pattern_mat = BMatrix(list_functions.tuple_to_list(pattern))
        out_mat = walshlib.generate_walsh(seed_mat, pattern_mat, order)
        filecode = generate_filecode(seed_mat, pattern_mat, order)
        filecode += "." + file_type
        print_matrix(out_mat, filecode)
        file_count += 1
        printProgressBar(file_count, total_files)

os.chdir("..")

print(f"finished successfully, creating {file_count} files")
