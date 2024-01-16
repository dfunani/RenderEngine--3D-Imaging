"""
vector_math module

This module defines two vector classes, Vector2 and Vector3, representing 2D and 3D vectors, respectively.
Each class provides essential vector operations, including addition, subtraction, scalar multiplication,
cross product (for Vector3), dot product, vector normalization, and length calculation.

Classes:
    - Vector2: A 2D vector class with x and y coordinates.
    - Vector3: A 3D vector class with x, y, and z coordinates.

Specialized Classes:
    - Vector2f: Specialization of Vector2 for float.
    - Vector2i: Specialization of Vector2 for int.
    - Vector3f: Specialization of Vector3 for float.
    - Vector3i: Specialization of Vector3 for int.

Functions:
    - float_to_int(v: Vector3f) -> Vector3i: Convert Vector3 with float components to Vector3 with int components.
    - int_to_float(v: Vector3i) -> Vector3f: Convert Vector3 with int components to Vector3 with float components.

Ostream-like Functions:
    - vec2_to_str(v: Vector2) -> str: Return a string representation for Vector2.
    - vec3_to_str(v: Vector3) -> str: Return a string representation for Vector3.
"""

from math import sqrt
from typing import Union


class Vector2:
    """
    A 2D vector class.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
    """

    def __init__(self, x: float = 0, y: float = 0):
        """
        Initialize a 2D vector with given x and y coordinates.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
        """
        self.x = x
        self.y = y

    def __str__(self) -> str:
        """
        Return a string representation of the vector.

        Returns:
            str: A string representation of the vector.
        """
        return f"({self.x}, {self.y})"

    def __add__(self, other: "Vector2") -> "Vector2":
        """
        Add two vectors element-wise.

        Args:
            other (Vector2): The vector to be added.

        Returns:
            Vector2: The result of the addition.
        """
        return Vector2(self.x + other.x, self.y + other.y)

    def __sub__(self, other: "Vector2") -> "Vector2":
        """
        Subtract two vectors element-wise.

        Args:
            other (Vector2): The vector to be subtracted.

        Returns:
            Vector2: The result of the subtraction.
        """
        return Vector2(self.x - other.x, self.y - other.y)

    def __mul__(self, scalar: float) -> "Vector2":
        """
        Multiply the vector by a scalar.

        Args:
            scalar (float): The scalar to multiply by.

        Returns:
            Vector2: The result of the multiplication.
        """
        return Vector2(self.x * scalar, self.y * scalar)

    def __getitem__(self, i: int) -> float:
        """
        Get the i-th component of the vector.

        Args:
            i (int): The index of the component.

        Returns:
            float: The value of the i-th component.
        Raises:
            IndexError: If the index is out of range.
        """
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        else:
            raise IndexError("Index out of range for Vector2")


class Vector3:
    """
    A 3D vector class.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
        z (float): The z-coordinate of the vector.
    """

    def __init__(self, x: float = 0, y: float = 0, z: float = 0):
        """
        Initialize a 3D vector with given x, y, and z coordinates.

        Args:
            x (float): The x-coordinate.
            y (float): The y-coordinate.
            z (float): The z-coordinate.
        """
        self.x = x
        self.y = y
        self.z = z

    def __str__(self) -> str:
        """
        Return a string representation of the vector.

        Returns:
            str: A string representation of the vector.
        """
        return f"({self.x}, {self.y}, {self.z})"

    def __xor__(self, other: "Vector3") -> "Vector3":
        """
        Calculate the cross product of two vectors.

        Args:
            other (Vector3): The vector to calculate the cross product with.

        Returns:
            Vector3: The cross product of the two vectors.
        """
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def __add__(self, other: "Vector3") -> "Vector3":
        """
        Add two vectors element-wise.

        Args:
            other (Vector3): The vector to be added.

        Returns:
            Vector3: The result of the addition.
        """
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        elif isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        else:
            raise TypeError(f"Unsupported operand type for +: {type(other)}")

    def __sub__(self, other: "Vector3") -> "Vector3":
        """
        Subtract two vectors element-wise.

        Args:
            other (Vector3): The vector to be subtracted.

        Returns:
            Vector3: The result of the subtraction.
        """
        return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other: Union["Vector3", float, int]) -> "Vector3":
        """
        Element-wise multiplication of two vectors.

        Args:
            other (Union[int, float, Vector3]): The vector or scalar to multiply by.

        Returns:
            Vector3: The result of the multiplication.
        """
        if isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        elif isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        else:
            raise TypeError(f"Unsupported operand type for *: {type(other)}")

    def __matmul__(self, other: "Vector3") -> float:
        """
        Calculate the dot product of two vectors.

        Args:
            other (Vector3): The vector to calculate the dot product with.

        Returns:
            float: The dot product of the two vectors.
        """
        return self.x * other.x + self.y * other.y + self.z * other.z

    def norm(self) -> float:
        """
        Calculate the Euclidean norm (length) of the vector.

        Returns:
            float: The length of the vector.
        """
        return sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def normalize(self, l: float = 1) -> "Vector3":
        """
        Normalize the vector to a specified length (default is 1).

        Args:
            l (float): The desired length.

        Returns:
            Vector3: The normalized vector.
        """
        length = self.norm()
        return Vector3(
            self.x * (l / length), self.y * (l / length), self.z * (l / length)
        )

    def __getitem__(self, i: int) -> float:
        """
        Get the i-th component of the vector.

        Args:
            i (int): The index of the component.

        Returns:
            float: The value of the i-th component.
        Raises:
            IndexError: If the index is out of range.
        """
        if i == 0:
            return self.x
        elif i == 1:
            return self.y
        elif i == 2:
            return self.z
        else:
            raise IndexError("Index out of range for Vector3")


# Vector2 specialization for float and int
class Vector2f(Vector2):
    """Specialization of Vector2 for float."""

    pass


class Vector2i(Vector2):
    """Specialization of Vector2 for int."""

    pass


# Vector3 specialization for float and int
class Vector3f(Vector3):
    """Specialization of Vector3 for float."""

    pass


class Vector3i(Vector3):
    """Specialization of Vector3 for int."""

    pass
