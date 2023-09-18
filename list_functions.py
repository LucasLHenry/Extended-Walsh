def is_rectangular(mat: [[None]]) -> bool:
    """Given a 2d list, returns whether the list is rectangular"""
    try:
        width = len(mat[0])
        for item in mat:
            if not len(item) == width:
                return False
    except IndexError or TypeError:
        return False
    return True


def element_is_binary(val) -> bool:
    if not isinstance(val, bool):
        if not isinstance(val, int):
            return False
        if val not in [0, 1]:
            return False
    return True


def is_binary(mat: [[None]]) -> bool:
    """Given a 2d list, returns whether the list is binary"""
    try:
        for row in mat:
            for val in row:
                if not element_is_binary(val):
                    return False
    except IndexError or TypeError:
        return False
    return True


def flip(mat: [[None]]):
    """Given a list or BMatrix, switch true to false or false to true elementwise"""
    out_mat = []
    if hasattr(mat, "__iter__"):
        for item in mat:
            out_mat.append(flip(item))
        return out_mat
    else:
        return not mat


def is_flat(mat: [[None]]) -> bool:
    for item in mat:
        if hasattr(item, "__iter__"):
            return False
    return True


def tuple_to_list(mat: [[None]]):
    out_mat = []
    if hasattr(mat, "__iter__"):
        if is_flat(mat):
            return list(mat)
        for el in mat:
            out_mat.append(tuple_to_list(el))
        return out_mat
    else:
        return mat


def convert_row_col(mat: [[None]]) -> [[None]]:
    if not is_rectangular(mat):
        raise TypeError("list must be rectangular")
    col_list = []
    for i in range(len(mat[0])):
        col_list.append([row[i] for row in mat])
    return col_list
