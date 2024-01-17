from math import sqrt

from numpy import eye





class Vector3:
    def __init__(self, x: float = 0.0, y: float = 0.0, z: float = 0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __gt__(self, other):
        # Compare based on the magnitude of the vectors
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5

    def __pow__(self, exponent):
        # Exponentiation of each component
        return Vector3(self.x**exponent, self.y**exponent, self.z**exponent)

    def __add__(self, other):
        return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, scalar):
        return Vector3(scalar * self.x, scalar * self.y, scalar * self.z)

    def __truediv__(self, scalar):
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        else:
            raise IndexError("Vector3 index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.z = value
        else:
            raise IndexError("Vector3 index out of range")

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self):
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def normalize(self):
        length = self.length()
        if length != 0:
            return self / length
        else:
            return Vector3()

    def norm(self):
        return (self.x**2 + self.y**2 + self.z**2) ** 0.5


class Vector4:
    def __init__(self, x=0, y=0, z=0, w=1):
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __mul__(self, scalar):
        return Vector4(
            self.x * scalar, self.y * scalar, self.z * scalar, self.w * scalar
        )

    def __repr__(self):
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"

    def __getitem__(self, index):
        if index == 0:
            return self.x
        elif index == 1:
            return self.y
        elif index == 2:
            return self.z
        elif index == 3:
            return self.w
        else:
            raise IndexError("Vector4 index out of range")

    def __setitem__(self, index, value):
        if index == 0:
            self.x = value
        elif index == 1:
            self.y = value
        elif index == 2:
            self.y = value
        elif index == 3:
            self.y = value
        else:
            raise IndexError("Vector4 index out of range")

    def __truediv__(self, scalar):
        if self.w == 0:
            return Vector4()
        return Vector4(
            scalar / self.x, scalar / self.y, scalar / self.z, scalar / self.w
        )


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
