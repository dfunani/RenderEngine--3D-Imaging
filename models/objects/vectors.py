from typing import Self
from math import sqrt


class Vector:
    def __init__(self, *args) -> None:
        self.coordinates = list(args)

    def __getitem__(self, i) -> Self:
        return self.coordinates[i]

    def __setitem__(self, i, value) -> Self:
        self.coordinates[i] = value

    def __add__(self, other) -> Self:
        if isinstance(other, Vector):
            return Vector(*(a + b for a, b in zip(self.coordinates, other)))
        return Vector(*(a + other for a in self.coordinates))

    # def __iadd__(self, other) -> Self:
    #     if isinstance(other, Vector):
    #         self.coordinates = [a + b for a, b in zip(self.coordinates, other)]
    #     else:
    #         self.coordinates = [a + other for a in self.coordinates]
    #     return self

    def __sub__(self, other) -> Self:
        if isinstance(other, Vector):
            return Vector(*(a - b for a, b in zip(self.coordinates, other)))
        return Vector(*(a - other for a in self.coordinates))

    # def __isub__(self, other) -> Self:
    #     if isinstance(other, Vector):
    #         self.coordinates = [a - b for a, b in zip(self.coordinates, other)]
    #     else:
    #         self.coordinates = [a - other for a in self.coordinates]
    #     return self

    def __mul__(self, other) -> Self:
        if isinstance(other, Vector):
            return Vector(*(a * b for a, b in zip(self.coordinates, other)))
        return Vector(*(a * other for a in self.coordinates))

    def __truediv__(self, other) -> Self:
        if isinstance(other, Vector):
            return Vector(*(a / b for a, b in zip(self.coordinates, other)))
        return Vector(*(a / other for a in self.coordinates))

    def __gt__(self, other):
        if isinstance(other, Vector):
            return all(a > b for a, b in zip(self.coordinates, other))
        else:
            return all(a > other for a in self.coordinates)

    def __neg__(self):
        return Vector(*(-a for a in self.coordinates))

    def __pow__(self, exponent):
        return Vector(*(a**exponent for a in self.coordinates))

    def __lt__(self, other):
        if isinstance(other, Vector):
            return all(a < b for a, b in zip(self.coordinates, other))
        else:
            return all(a < other for a in self.coordinates)

    def __gte__(self, other):
        if isinstance(other, Vector):
            return all(a >= b for a, b in zip(self.coordinates, other))
        else:
            return all(a >= other for a in self.coordinates)

    def __lte__(self, other):
        if isinstance(other, Vector):
            return all(a <= b for a, b in zip(self.coordinates, other))
        else:
            return all(a <= other for a in self.coordinates)

    def dot(self, other) -> float:
        return sum(a * b for a, b in zip(self.coordinates, other))

    def cross(self, other) -> Self:
        assert len(self.coordinates) == 3 and len(other) == 3
        return Vector(
            self[1] * other[2] - self[2] * other[1],
            self[2] * other[0] - self[0] * other[2],
            self[0] * other[1] - self[1] * other[0],
        )

    def norm(self) -> float:
        return sqrt(sum(a**2 for a in self.coordinates))

    def normalize(self, l=1) -> Self:
        length = self.norm()
        if length != 0:
            return Vector(*(a * (l / length) for a in self.coordinates))
        return self

    def __str__(self) -> str:
        return " ".join(str(a) for a in self.coordinates)

    def __and__(self, other):
        return (
            self.coordinates[0]
            if other == 0
            else self.coordinates[1]
            if other == 1
            else self.coordinates[2]
        )


class RGB(Vector):
    def __init__(self, red=0.0, green=0.0, blue=0.0):
        super().__init__(red, green, blue)


class Vector2Float(Vector):
    def __init__(self, x=0.0, y=0.0):
        super().__init__(x, y)


class Vector3Float(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0):
        super().__init__(x, y, z)


class Vector3Int(Vector):
    def __init__(self, x=0, y=0, z=0):
        super().__init__(x, y, z)


class Vector4Float(Vector):
    def __init__(self, x=0.0, y=0.0, z=0.0, w=0.0):
        super().__init__(x, y, z, w)
