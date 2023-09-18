from bmatrix import BMatrix
import list_functions
import re
import matrix_functions as mf
import list_functions as lf


class Walsh_Generator:
    @staticmethod
    def parse_filecode(filecode: str):
        re_str = r"s(?P<s_x>.*)x(?P<s_y>.*)-(?P<s_code>.*)_p(?P<p_x>.*)x(?P<p_y>.*)-(?P<p_code>.*)_o(?P<order>.*)"
        m = re.match(re_str, filecode)
        s_x = int(m.group("s_x"))
        s_y = int(m.group("s_y"))
        s_code = str(m.group("s_code"))
        p_x = int(m.group("p_x"))
        p_y = int(m.group("p_y"))
        p_code = str(m.group("p_code"))
        order = int(m.group("order"))

        if not s_y == len(s_code):
            raise ValueError("seed dimensions and code do not match")

        if not p_y == len(p_code):
            raise ValueError("pattern dimensions and code do not match")
        
        s_mat = mf.arr_from_matcode(s_code, width=s_x)
        p_mat = mf.arr_from_matcode(p_code, width=p_x)
        return s_x, s_y, s_mat, p_x, p_y, p_mat, order

    def __init__(self, seed_size: int = 0, pattern_size: int = 0, order: int = 1, filecode: str = None):
        if filecode is not None:
            (_, _, s_mat, _, _, p_mat, order) = self.parse_filecode(filecode)
            self._seed = BMatrix(s_mat)
            self._pattern = BMatrix(p_mat)
            self._order = order
        else:
            self._seed_size = seed_size
            self._pattern_size = pattern_size
            self._order = order
    
    @staticmethod
    def walsh_iteration(seed: BMatrix, pattern: BMatrix) -> BMatrix:
        """Performs one iteration of the walsh matrix generation"""
        out_mat = []
        for p_row in pattern:
            for s_row in seed:
                row_buf = []
                for val in p_row:
                    row_buf += s_row if val else list_functions.flip(s_row)
                out_mat.append(row_buf)
        return BMatrix(out_mat)
    
    @staticmethod
    def generate_walsh(seed: BMatrix, pattern: BMatrix, order: int) -> BMatrix:
        """Performs multiple iterations of the walsh matrix generation"""
        mat_buf = seed
        for _ in range(order):
            mat_buf = Walsh_Generator.walsh_iteration(mat_buf, pattern)
        return mat_buf
    
    def set_seed(self, seed):
        """Sets the current seed, either from another BMatrix or a rectangular list"""
        if isinstance(seed, BMatrix):
            self._seed = seed
        else:
            try:
                self._seed = BMatrix(seed)
            except TypeError as e:
                raise TypeError("incorrect argument for seed") from e
    
    def get_seed(self):
        """Gets the current pattern, or raises an error if it doesn't exist"""
        try:
            return self._seed
        except AttributeError as e:
            raise AttributeError("pattern not yet set") from e
        
    def set_pattern(self, pattern):
        """Sets the current pattern, either from another BMatrix or a rectangular list"""
        if isinstance(pattern, BMatrix):
            self._pattern = pattern
        else:
            try:
                self._pattern = BMatrix(pattern)
            except TypeError as e:
                raise TypeError("incorrect argument for pattern") from e
    
    def get_pattern(self) -> BMatrix:
        """Gets the current pattern, or raises an error if it doesn't exist"""
        try:
            return self._pattern
        except AttributeError as e:
            raise AttributeError("pattern not yet set") from e
    
    def generate_from_settings(self) -> (BMatrix, str):
        filecode = mf.generate_filecode(self._seed, self._pattern, self._order)
        return self.generate_walsh(self._seed, self._pattern, self._order), filecode
    
    def generate_all_from_settings(self) -> (BMatrix, str):
        for seed in mf.generate_possible_matrices(self._seed_size):
            for pattern in mf.generate_possible_matrices(self._pattern_size):
                filecode = mf.generate_filecode(seed, pattern, self._order)
                yield self.generate_walsh(seed, pattern, self._order), filecode
        
    
    
    