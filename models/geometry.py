"""
matrix.py

This module defines a Matrix class for basic matrix operations including matrix multiplication,
transpose, inverse, and creation of an identity matrix.

Classes:
- Matrix: Represents a matrix and provides methods for various matrix operations.

Example Usage:
    mat = Matrix(3, 3)
    print(mat.identity(3))
    print(mat.transpose())
    print(mat.inverse())
    print(mat * mat)
    print(str(mat))
"""

class Matrix:
    def __init__(self, rows: int = 0, cols: int = 0):
        """
        Initialize a Matrix object with the specified number of rows and columns.

        :param rows: Number of rows in the matrix.
        :param cols: Number of columns in the matrix.
        """
        self.m = [[0.0] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    def nrows(self) -> int:
        """
        Get the number of rows in the matrix.

        :return: Number of rows.
        """
        return self.rows

    def ncols(self) -> int:
        """
        Get the number of columns in the matrix.

        :return: Number of columns.
        """
        return self.cols

    @staticmethod
    def identity(dimensions: int) -> 'Matrix':
        """
        Create an identity matrix with the specified dimensions.

        :param dimensions: Number of rows and columns in the square matrix.
        :return: Identity matrix.
        """
        E = Matrix(dimensions, dimensions)
        for i in range(dimensions):
            for j in range(dimensions):
                E[i][j] = 1.0 if i == j else 0.0
        return E

    def __getitem__(self, i: int) -> list[float]:
        """
        Get the i-th row of the matrix.

        :param i: Index of the row.
        :return: i-th row of the matrix.
        """
        assert 0 <= i < self.rows
        return self.m[i]

    def __mul__(self, a: 'Matrix') -> 'Matrix':
        """
        Multiply the matrix by another matrix.

        :param a: Matrix to be multiplied.
        :return: Resulting matrix.
        """
        assert self.cols == a.rows
        result = Matrix(self.rows, a.cols)
        for i in range(self.rows):
            for j in range(a.cols):
                result.m[i][j] = sum(self.m[i][k] * a.m[k][j] for k in range(self.cols))
        return result

    def transpose(self) -> 'Matrix':
        """
        Transpose the matrix.

        :return: Transposed matrix.
        """
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result[j][i] = self.m[i][j]
        return result

    def inverse(self) -> 'Matrix':
        """
        Calculate the inverse of the matrix.

        :return: Inverse matrix.
        """
        assert self.rows == self.cols
        result = Matrix(self.rows, self.cols * 2)

        # Augmenting the square matrix with the identity matrix of the same dimensions a => [ai]
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self.m[i][j]
        for i in range(self.rows):
            result[i][i + self.cols] = 1

        # First pass
        for i in range(self.rows - 1):
            # Normalize the first row
            for j in range(result.cols - 1, -1, -1):
                result[i][j] /= result[i][i]
            for k in range(i + 1, self.rows):
                coeff = result[k][i]
                for j in range(result.cols):
                    result[k][j] -= result[i][j] * coeff

        # Normalize the last row
        for j in range(result.cols - 1, self.rows - 1, -1):
            result[self.rows - 1][j] /= result[self.rows - 1][self.rows - 1]

        # Second pass
        for i in range(self.rows - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                coeff = result[k][i]
                for j in range(result.cols):
                    result[k][j] -= result[i][j] * coeff

        # Cut the identity matrix back
        truncate = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                truncate[i][j] = result[i][j + self.cols]

        return truncate


    def __str__(self) -> str:
        """
        Return a string representation of the matrix.

        :return: String representation of the matrix.
        """
        return '\n'.join(['\t'.join(map(str, row)) for row in self.m])

# Example usage:
# mat = Matrix(3, 3)
# print(mat.identity(3))
# print(mat.transpose())
# print(mat.inverse())
# print(mat * mat)
# print(str(mat))
