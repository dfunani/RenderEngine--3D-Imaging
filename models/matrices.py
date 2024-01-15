class Matrix:
    def __init__(self, rows, cols):
        self.m = [[0.0] * cols for _ in range(rows)]
        self.rows = rows
        self.cols = cols

    @property
    def nrows(self):
        return self.rows

    @property
    def ncols(self):
        return self.cols

    @classmethod
    def identity(cls, dimensions):
        E = cls(dimensions, dimensions)
        for i in range(dimensions):
            for j in range(dimensions):
                E[i][j] = 1.0 if i == j else 0.0
        return E

    def __getitem__(self, i):
        return self.m[i]

    def __mul__(self, a):
        assert self.cols == a.rows
        result = Matrix(self.rows, a.cols)
        for i in range(self.rows):
            for j in range(a.cols):
                result[i][j] = sum(self.m[i][k] * a.m[k][j] for k in range(self.cols))
        return result

    def transpose(self):
        result = Matrix(self.cols, self.rows)
        for i in range(self.rows):
            for j in range(self.cols):
                result[j][i] = self.m[i][j]
        return result

    def inverse(self):
        assert self.rows == self.cols
        # augmenting the square matrix with the identity matrix of the same dimensions A => [AI]
        result = Matrix(self.rows, self.cols * 2)
        for i in range(self.rows):
            for j in range(self.cols):
                result[i][j] = self.m[i][j]
        for i in range(self.rows):
            result[i][i + self.cols] = 1
        # first pass
        for i in range(self.rows - 1):
            # normalize the first row
            for j in range(result.cols - 1, -1, -1):
                result[i][j] /= result[i][i]
            for k in range(i + 1, self.rows):
                coeff = result[k][i]
                for j in range(result.cols):
                    result[k][j] -= result[i][j] * coeff
        # normalize the last row
        for j in range(result.cols - 1, self.rows - 1, -1):
            result[self.rows - 1][j] /= result[self.rows - 1][self.rows - 1]
        # second pass
        for i in range(self.rows - 1, 0, -1):
            for k in range(i - 1, -1, -1):
                coeff = result[k][i]
                for j in range(result.cols):
                    result[k][j] -= result[i][j] * coeff
        # cut the identity matrix back
        truncate = Matrix(self.rows, self.cols)
        for i in range(self.rows):
            for j in range(self.cols):
                truncate[i][j] = result[i][j + self.cols]
        return truncate

    def __str__(self):
        result_str = ""
        for i in range(self.rows):
            for j in range(self.cols):
                result_str += str(self.m[i][j])
                if j < self.cols - 1:
                    result_str += "\t"
            result_str += "\n"
        return result_str