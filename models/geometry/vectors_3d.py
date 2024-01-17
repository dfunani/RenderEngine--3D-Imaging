from math import sqrt

class Vector3:
    """
    A 3D vector class representing a point or direction in three-dimensional space.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
        z (float): The z-coordinate of the vector.

    Methods:
        __init__(x=0.0, y=0.0, z=0.0): Initializes a new Vector3 instance.
        __repr__(): Returns a string representation of the vector.
        __eq__(other): Checks if two vectors are equal.
        __ne__(other): Checks if two vectors are not equal.
        __gt__(other): Compares vectors based on magnitude.
        __ge__(other): Checks if the magnitude of the vector is greater than or equal to another.
        __lt__(other): Checks if the magnitude of the vector is less than another.
        __le__(other): Checks if the magnitude of the vector is less than or equal to another.
        __add__(other): Adds another vector or scalar to the current vector.
        __sub__(other): Subtracts another vector or scalar from the current vector.
        __mul__(scalar): Multiplies the vector by a scalar.
        __truediv__(scalar): Divides the vector by a scalar.
        __getitem__(index): Gets the value at the specified index (0, 1, or 2).
        __setitem__(index, value): Sets the value at the specified index (0, 1, or 2).
        __pow__(exponent): Raises each component to the specified exponent.
        __neg__(): Returns the negation of the vector.
        __pos__(): Returns a copy of the vector.
        dot(other): Calculates the dot product with another vector.
        cross(other): Calculates the cross product with another vector.
        length(): Calculates the length (magnitude) of the vector.
        length_squared(): Calculates the squared length of the vector.
        normalize(): Returns a normalized copy of the vector.
        norm(): Calculates the Euclidean norm of the vector.

    Usage Example:
        v = Vector3(1.0, 2.0, 3.0)
        v_normalized = v.normalize()
        length = v.length()
    """

    def __init__(self, x=0.0, y=0.0, z=0.0):
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self):
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __eq__(self, other):
        return isinstance(other, Vector3) and self.x == other.x and self.y == other.y and self.z == other.z

    def __ne__(self, other):
        return not self.__eq__(other)

    def __gt__(self, other):
        return self.length() > other.length()

    def __ge__(self, other):
        return self.length() >= other.length()

    def __lt__(self, other):
        return self.length() < other.length()

    def __le__(self, other):
        return self.length() <= other.length()

    def __add__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        elif isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        else:
            raise TypeError("Unsupported operand type for +: {}".format(type(other)))

    def __sub__(self, other):
        if isinstance(other, (int, float)):
            return Vector3(self.x - other, self.y - other, self.z - other)
        elif isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        else:
            raise TypeError("Unsupported operand type for -: {}".format(type(other)))

    def __mul__(self, scalar):
        return Vector3(scalar * self.x, scalar * self.y, scalar * self.z)

    def __truediv__(self, scalar):
        if scalar == 0:
            raise ZeroDivisionError("Division by zero")
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

    def __pow__(self, exponent):
        return Vector3(self.x ** exponent, self.y ** exponent, self.z ** exponent)

    def __neg__(self):
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self):
        return Vector3(self.x, self.y, self.z)

    def dot(self, other):
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other):
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self):
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    def length_squared(self):
        return self.x ** 2 + self.y ** 2 + self.z ** 2

    def normalize(self):
        length = self.length()
        if length != 0:
            return self / length
        else:
            return Vector3()

    def norm(self):
        return sqrt(self.length_squared())

# Usage Example:
# v = Vector3(1.0, 2.0, 3.0)
# v_normalized = v.normalize()
# length = v.length()
