from bmatrix import BMatrix
import list_functions


def walsh_iteration(seed: BMatrix, pattern: BMatrix) -> BMatrix:
    out_mat = []
    for p_row in pattern:
        for s_row in seed:
            row_buf = []
            for val in p_row:
                row_buf += s_row if val else list_functions.flip(s_row)
            out_mat.append(row_buf)
    return BMatrix(out_mat)

def generate_walsh(seed: BMatrix, pattern: BMatrix, order: int) -> BMatrix:
    mat_buf = seed
    for _ in range(order):
        mat_buf = walsh_iteration(mat_buf, pattern)
    return mat_buf

