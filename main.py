from bmatrix import BMatrix
import walshlib
import configparser
import list_functions as lf
import matrix_functions as mf
from helper_functions import printProgressBar
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



folder_name = output_folder + f"_s{seed_size}p{pattern_size}_o{order}"
os.makedirs("../IMAGES/" + folder_name, exist_ok=True)
os.chdir(folder_name)

file_count = 0
total_seeds = 2 ** (seed_size ** 2)
total_patterns = 2 ** (pattern_size ** 2)
total_files = total_seeds * total_patterns

print(f"total files to print: {total_files}")
walsh_generator = walshlib.Walsh_Generator(seed_size, pattern_size, order)
for output_matrix, filecode in walsh_generator.generate_all_from_settings():
    filecode += "." + file_type
    mf.print_matrix(output_matrix, filecode)
    file_count += 1
    printProgressBar(file_count, total_files)

os.chdir("..")

print(f"finished successfully, creating {file_count} files at {os.path.abspath(os.path.curdir)}/{output_folder}")
