from math import sqrt

from numpy import eye


class Matrix:
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        self.data = eye(rows, cols)

    def __getitem__(self, indices: tuple[int, int]) -> float:
        i, j = indices
        return self.data[i, j]

    def __setitem__(self, indices: tuple[int, int], value: float) -> None:
        i, j = indices
        self.data[i, j] = value

    @staticmethod
    def identity():
        return eye(4)
