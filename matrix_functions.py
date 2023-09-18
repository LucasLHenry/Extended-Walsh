from bmatrix import BMatrix
import matplotlib.pyplot as plt
from itertools import product
import list_functions as lf


def generate_matcode(mat: BMatrix) -> str:
    """
    Generates a string based on the contents of a BMatrix by turning each row into it's hexadecimal
    representation [1, 1, 0] -> 0x6 -> "6",  [1, 1, 0, 1] -> 0xD -> "D"
    """
    (w, h) = mat.get_dimensions()
    row_list = mat.get_row_list()
    out_str = str(w) + "x" + str(h) + "-"
    for row in row_list:
        row_str = ""
        for item in row:
            row_str += "1" if item else "0"
        # complicated line, but pretty much takes the row and interprets it as
        # a binary number, converting it to binary
        out_str += hex(int(row_str, 2))[2:].upper()
    return out_str


def generate_filecode(seed: BMatrix, pattern: BMatrix, order: int) -> str:
    """
    Generates a filecode for the combination of seed, pattern, and order. The format is
    "'s' seed width 'x' seed height '-' seed hex code '_p' pattern width 'x' pattern height '-'
    pattern hex code '_o' order". The patterns are geneṡrated by the 'generate_matcode' function
    """
    out_str = "s" + generate_matcode(seed)
    out_str += "_p" + generate_matcode(pattern)
    out_str += "_o" + str(order)
    return out_str

def arr_from_matcode(matcode: str, width: int) -> BMatrix:
    arr_buf = []
    for mat_c in matcode:
        bin_str = bin(int(mat_c, 16))[2:].rjust(width, '0')
        row_buf = []
        for bin_c in bin_str:
            row_buf.append(int(bin_c))
        arr_buf.append(row_buf)
    return arr_buf


def print_matrix(matrix: BMatrix, filename: str) -> None:
    """Uses matplotlib to print a matrix to a given filename"""
    plt.style.use('_mpl-gallery-nogrid')
    _, ax = plt.subplots()
    ax.imshow(matrix.get_row_list())
    plt.savefig(filename)
    plt.close('all')

def generate_possible_matrices(size: int):
    for tuple_m in product(product([True, False], repeat=size), repeat=size):
        yield BMatrix(lf.tuple_to_list(tuple_m))