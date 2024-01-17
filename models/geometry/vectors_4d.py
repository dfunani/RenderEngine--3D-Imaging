"""
vectors_4d.py - Module for 4D vector operations.

This module defines the Vector4 class, which represents a 4D vector in four-dimensional space.
The Vector4 class provides various mathematical operations and methods commonly used in
geometry and computer graphics. It is designed to handle operations relevant to reading
.obj files and writing TGA files in a 4D context.

Classes:
    Vector4: A class representing a 4D vector with various mathematical operations.

Usage Example:
    v = Vector4(1.0, 2.0, 3.0, 1.0)
    v_normalized = v.normalize()
    length = v.length()
    
"""

from typing import Union
from math import sqrt

from models.interfaces.vectors import Vector


class Vector4(Vector):
    """
    A 4D vector class representing a point or direction in four-dimensional space.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.
        z (float): The z-coordinate of the vector.
        w (float): The w-coordinate of the vector.

    Methods:
        __init__(x=0.0, y=0.0, z=0.0, w=1.0): Initializes a new Vector4 instance.
        __repr__(): Returns a string representation of the vector.
        __eq__(other): Checks if two vectors are equal.
        __ne__(other): Checks if two vectors are not equal.
        __gt__(other): Compares vectors based on magnitude.
        __ge__(other): Checks if the magnitude of the vector is greater than or equal to another.
        __lt__(other): Checks if the magnitude of the vector is less than another.
        __le__(other): Checks if the magnitude of the vector is less than or equal to another.
        __add__(other): Adds another vector or scalar to the current vector.
        __sub__(other): Subtracts another vector or scalar from the current vector.
        __mul__(other): Multiplies the vector by another vector or a scalar.
        __truediv__(scalar): Divides the vector by a scalar.
        __getitem__(index): Gets the value at the specified index (0, 1, 2, or 3).
        __setitem__(index, value): Sets the value at the specified index (0, 1, 2, or 3).
        __pow__(exponent): Raises each component to the specified exponent.
        __neg__(): Returns the negation of the vector.
        __pos__(): Returns a copy of the vector.
        dot(other): Calculates the dot product with another vector.
        length(): Calculates the length (magnitude) of the vector.
        length_squared(): Calculates the squared length of the vector.
        normalize(): Returns a normalized copy of the vector.
        norm(): Calculates the Euclidean norm of the vector.
        cross(other): Calculates the cross product with another vector
        (for 4D vectors, returns Vector4(0, 0, 0, 1)).
        homogenize(): Homogenizes the vector by dividing x, y, and z components by w.

    Usage Example:
        v = Vector4(1.0, 2.0, 3.0, 1.0)
        v_normalized = v.normalize()
        length = v.length()
    """

    def __init__(
        self,
        x: Union[int, float] = 0.0,
        y: Union[int, float] = 0.0,
        z: Union[int, float] = 0.0,
        w: Union[int, float] = 1.0,
    ) -> None:
        """Initialize a 4D vector with specified coordinates."""
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def __repr__(self) -> str:
        """Return a string representation of the Vector4 instance."""
        return f"Vector4({self.x}, {self.y}, {self.z}, {self.w})"

    def __eq__(self, other: "Vector4") -> bool:
        """Check if two vectors are equal."""
        if isinstance(other, Vector4):
            return (
                self.x == other.x
                and self.y == other.y
                and self.z == other.z
                and self.w == other.w
            )
        return False

    def __add__(
        self, other: Union["Vector4", int, float]
    ) -> Union["Vector4", TypeError]:
        """Add another vector or scalar to the current vector."""
        if isinstance(other, (int, float)):
            return Vector4(
                self.x + other, self.y + other, self.z + other, self.w + other
            )
        if isinstance(other, Vector4):
            return Vector4(
                self.x + other.x, self.y + other.y, self.z + other.z, self.w + other.w
            )
        raise TypeError(f"Unsupported operand type for +: {other}")

    def __sub__(
        self, other: Union["Vector4", int, float]
    ) -> Union["Vector4", TypeError]:
        """Subtract another vector or scalar from the current vector."""
        if isinstance(other, (int, float)):
            return Vector4(
                self.x - other, self.y - other, self.z - other, self.w - other
            )
        if isinstance(other, Vector4):
            return Vector4(
                self.x - other.x, self.y - other.y, self.z - other.z, self.w - other.w
            )
        raise TypeError(f"Unsupported operand type for -: {other}")

    def __mul__(
        self, other: Union["Vector4", int, float]
    ) -> Union["Vector4", TypeError]:
        """Multiply the vector by another vector or a scalar."""
        if isinstance(other, (int, float)):
            return Vector4(
                self.x * other, self.y * other, self.z * other, self.w * other
            )
        if isinstance(other, Vector4):
            return Vector4(
                self.x * other.x, self.y * other.y, self.z * other.z, self.w * other.w
            )
        raise TypeError(f"Unsupported operand type for *: {other}")

    def __truediv__(
        self, other: Union["Vector4", int, float]
    ) -> Union["Vector4", ZeroDivisionError, TypeError]:
        """Divide the vector by a vector or scalar."""
        if isinstance(other, Vector4):
            return Vector4(
                self.x / other.x, self.y / other.y, self.z / other.z, self.w / other.w
            )
        if isinstance(other, (int, float)):
            if other != 0:
                return Vector4(
                    self.x / other, self.y / other, self.z / other, self.w / other
                )
            raise ZeroDivisionError("Division by zero")
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def __neg__(self) -> "Vector4":
        """Return the negation of the vector."""
        return Vector4(-self.x, -self.y, -self.z, -self.w)

    # def __getitem__(self, index: int) -> Union[IndexError, int, float]:
    #     """Get the value at the specified index (0, 1, 2, or 3)."""
    #     if index == 0:
    #         return self.x
    #     if index == 1:
    #         return self.y
    #     if index == 2:
    #         return self.z
    #     if index == 3:
    #         return self.w
    #     raise IndexError("Vector4 index out of range")

    # def __setitem__(
    #     self, index: int, value: Union[int, float, "Vector4"]
    # ) -> Union[None, IndexError]:
    #     """Set the value at the specified index (0, 1, 2, or 3)."""
    #     if index == 0:
    #         self.x = value
    #     if index == 1:
    #         self.y = value
    #     if index == 2:
    #         self.z = value
    #     if index == 3:
    #         self.w = value
    #     raise IndexError("Vector4 index out of range")

    def __pow__(self, exponent: Union[int, float]) -> "Vector4":
        """Raise each component to the specified exponent."""
        return Vector4(
            self.x**exponent,
            self.y**exponent,
            self.z**exponent,
            self.w**exponent,
        )

    def __pos__(self) -> "Vector4":
        """Return a copy of the vector."""
        return Vector4(self.x, self.y, self.z, self.w)

    def dot(self, other: "Vector4") -> Union[int, float]:
        """Calculate the dot product with another vector."""
        if isinstance(other, Vector4):
            return (
                self.x * other.x
                + self.y * other.y
                + self.z * other.z
                + self.w * other.w
            )
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def length(self) -> float:
        """Calculate the length (magnitude) of the vector."""
        return sqrt(self.x**2 + self.y**2 + self.z**2 + self.w**2)

    def length_squared(self) -> Union[int, float]:
        """Calculate the squared length of the vector."""
        return self.x**2 + self.y**2 + self.z**2 + self.w**2

    def normalize(self) -> "Vector4":
        """Return a normalized copy of the vector."""
        length = self.length()
        if length != 0:
            return self / length
        return Vector4()

    def norm(self) -> float:
        """Calculate the Euclidean norm of the vector."""
        return sqrt(self.length_squared())

    def cross(self) -> "Vector4":
        """
        Calculate the cross product with another vector.
        For 4D vectors, the cross product is always Vector4(0, 0, 0, 1).
        """
        return Vector4(0, 0, 0, 1)

    def homogenize(self) -> "Vector4":
        """Homogenize the vector by dividing x, y, and z components by w."""
        if self.w != 0:
            return Vector4(self.x / self.w, self.y / self.w, self.z / self.w, 1.0)
        return Vector4()
