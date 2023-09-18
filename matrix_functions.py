from bmatrix import BMatrix
import matplotlib.pyplot as plt


def generate_matcode(mat: BMatrix) -> str:
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
    pattern hex code '_o' order". One hexadecimal character per row of the binary matrix
    """
    out_str = "s" + generate_matcode(seed)
    out_str += "_p" + generate_matcode(pattern)
    out_str += "_o" + str(order)
    return out_str


def print_matrix(matrix: BMatrix, filename: str) -> None:
    """Using matplotlib to display the matrix"""
    plt.style.use('_mpl-gallery-nogrid')
    _, ax = plt.subplots()
    ax.imshow(matrix.get_row_list())
    plt.savefig(filename)
    plt.close('all')