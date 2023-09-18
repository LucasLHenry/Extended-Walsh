import list_functions


# (x,y) indexing for matrices
# ⌈ (0,0) (1,0) (2,0) ⌉
# | (0,1) (1,1) (2,1) |
# ⌊ (0,2) (1,2) (2,2) ⌋

class BMatrix:
    """A rectangular 2d list class, only allowed to contain True and False"""

    def __init__(self, matrix_list: [[int]] = None, width: int = 1, height: int = 1,
                 default_value=False) -> None:
        """
        Can construct a matrix from either a 2d list or a width, height, and (optional) default value.
        Will raise TypeError if the 2d list is not rectangular or is made up of anything other than ints
        """
        if matrix_list is not None:  # for list-based constructor
            if not list_functions.is_rectangular(matrix_list):  # only works on rectangular lists
                raise TypeError("matrix_list must be a rectangular 2d list")
            if not list_functions.is_binary(matrix_list):
                raise TypeError("matrix_list must be binary")
            (self._width, self._height) = len(matrix_list), len(matrix_list[0])
            self._row_list = [[bool(val) for val in row] for row in matrix_list]  # convert to boolean

        else:  # for size-based constructor
            self._row_list = []
            if not list_functions.element_is_binary(default_value):
                raise TypeError("matrix_list must only contain 0, 1, True, and False")
            for _ in range(height):
                self._row_list.append([default_value] * width)
            self._width = width
            self._height = height

        # generate column list
        self._col_list = list_functions.convert_row_col(self._row_list)

    def __len__(self) -> int:
        return self._height * self._width

    def __repr__(self) -> str:
        out_str = ""
        for (i, row) in enumerate(self._row_list):
            row_str = " "
            for item in row:
                row_str += str(int(item)) + " "
            if i == 0:
                out_str += "⌈" + row_str + "⌉\n"
            elif i == len(self._row_list) - 1:
                out_str += "⌊" + row_str + "⌋"
            else:
                out_str += "|" + row_str + "|\n"
        return out_str

    def __iter__(self):
        yield from self._row_list

    def get_at(self, x: int, y: int) -> bool:
        """
        Return the item at position (x, y) from the matrix.
        Will raise IndexError if indices are out of bounds (no wrapping)
        """
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise IndexError("indices out of bounds")
        return self._row_list[y][x]

    def set_at(self, x: int, y: int, val) -> None:
        """
        Set the value of position (x, y) to val. Will raise
        IndexError if indices are out of bounds (no wrapping)
        """
        if x < 0 or y < 0 or x >= self._width or y >= self._height:
            raise IndexError("indices out of bounds")
        if not list_functions.element_is_binary(val):
            raise TypeError("val must be binary")
        self._row_list[y][x] = val
        self._col_list[x][y] = val

    #  THESE METHODS WORK, I JUST DON'T NEED THE OVERHEAD RIGHT NOW
    def append_right(self, other_mat: "BMatrix") -> None:
        """Appends another BMatrix to the right of the current one"""
        (other_width, other_height) = other_mat.get_dimensions()
        if not self._height == other_height:
            raise ValueError("matrices must have the same height")
        self._col_list += other_mat.get_col_list()
        self._row_list = list_functions.convert_row_col(self._col_list)
        self._width += other_width

    def append_below(self, other_mat: "BMatrix") -> None:
        """Appends another BMatrix below the current one"""
        (other_width, other_height) = other_mat.get_dimensions()
        if not self._width == other_width:
            raise ValueError("matrices must have the same height")
        self._row_list += other_mat.get_row_list()
        self._col_list = list_functions.convert_row_col(self._row_list)
        self._height += other_height

    def get_row_list(self) -> [[bool]]:
        """Returns a row list representing the matrix"""
        return self._row_list

    def get_col_list(self) -> [[int]]:
        """Returns a column list representing the matrix"""
        return self._col_list

    def get_row(self, y: int) -> [int]:
        """Returns the row with the specified index"""
        if y < 0 or y >= self._height:
            raise IndexError("index out of bounds")
        return self._row_list[y]

    def get_col(self, x: int) -> [int]:
        """Returns the column with the specified index"""
        if x < 0 or x >= self._height:
            raise IndexError("index out of bounds")
        return self._col_list[x]

    def get_dimensions(self) -> (int, int):
        """Returns a (width, height) tuple representing the dimensions of the matrix"""
        return self._width, self._height

    def is_square(self) -> bool:
        """Returns true if the matrix is square, false if not"""
        return self._width == self._height


mat = BMatrix([[1, 0, 0], [0, 1, 1], [0, 1, 1]])
print(mat)

