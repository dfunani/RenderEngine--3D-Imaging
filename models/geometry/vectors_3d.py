"""
A module containing a 3D vector class representing a point or direction in three-dimensional space.

Classes:
    Vector3: A class representing a 3D vector with various mathematical operations.

Usage Example:
    v = Vector3(1.0, 2.0, 3.0)
    v_normalized = v.normalize()
    length = v.length()
"""

from math import sqrt
from typing import Union


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
        __mul__(other): Multiplies the vector by another vector or a scalar.
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

    def __init__(
        self,
        x: Union[int, float] = 0.0,
        y: Union[int, float] = 0.0,
        z: Union[int, float] = 0.0,
    ) -> None:
        """Initialize a 3D vector with specified coordinates."""
        self.x = x
        self.y = y
        self.z = z

    def __repr__(self) -> str:
        """Return a string representation of the Vector3 instance."""
        return f"Vector3({self.x}, {self.y}, {self.z})"

    def __eq__(self, other: "Vector3") -> bool:
        """Check if two vectors are equal."""
        return (
            isinstance(other, Vector3)
            and self.x == other.x
            and self.y == other.y
            and self.z == other.z
        )

    def __ne__(self, other: "Vector3") -> bool:
        """Check if two vectors are not equal."""
        return not self.__eq__(other)

    def __gt__(self, other: "Vector3") -> bool:
        """Compare vectors based on magnitude."""
        return self.length() > other.length()

    def __ge__(self, other: "Vector3") -> bool:
        """Check if the magnitude of the vector is greater than or equal to another."""
        return self.length() >= other.length()

    def __lt__(self, other: "Vector3") -> bool:
        """Check if the magnitude of the vector is less than another."""
        return self.length() < other.length()

    def __le__(self, other: "Vector3") -> bool:
        """Check if the magnitude of the vector is less than or equal to another."""
        return self.length() <= other.length()

    def __add__(
        self, other: Union["Vector3", int, float]
    ) -> Union["Vector3", TypeError]:
        """Add another vector or scalar to the current vector."""
        if isinstance(other, (int, float)):
            return Vector3(self.x + other, self.y + other, self.z + other)
        if isinstance(other, Vector3):
            return Vector3(self.x + other.x, self.y + other.y, self.z + other.z)
        raise TypeError(f"Unsupported operand type for +: {other}")

    def __sub__(
        self, other: Union["Vector3", int, float]
    ) -> Union["Vector3", TypeError]:
        """Subtract another vector or scalar from the current vector."""
        if isinstance(other, (int, float)):
            return Vector3(self.x - other, self.y - other, self.z - other)
        if isinstance(other, Vector3):
            return Vector3(self.x - other.x, self.y - other.y, self.z - other.z)
        raise TypeError(f"Unsupported operand type for -: {other}")

    def __mul__(
        self, other: Union["Vector3", int, float]
    ) -> Union["Vector3", TypeError]:
        """Multiply the vector by another vector or a scalar."""
        if isinstance(other, (int, float)):
            return Vector3(self.x * other, self.y * other, self.z * other)
        if isinstance(other, Vector3):
            return Vector3(self.x * other.x, self.y * other.y, self.z * other.z)
        raise TypeError(f"Unsupported operand type for *: {other}")

    def __truediv__(
        self, scalar: Union[int, float]
    ) -> Union["Vector3", ZeroDivisionError]:
        """Divide the vector by a scalar."""
        if scalar == 0:
            raise ZeroDivisionError("Division by zero")
        return Vector3(self.x / scalar, self.y / scalar, self.z / scalar)

    def __getitem__(self, index: int) -> Union[IndexError, int, float]:
        """Get the value at the specified index (0, 1, or 2)."""
        if index == 0:
            return self.x
        if index == 1:
            return self.y
        if index == 2:
            return self.z
        raise IndexError("Vector3 index out of range")

    def __setitem__(
        self, index: int, value: Union[int, float, "Vector3"]
    ) -> Union[None, IndexError]:
        """Set the value at the specified index (0, 1, or 2)."""
        if index == 0:
            self.x = value
        if index == 1:
            self.y = value
        if index == 2:
            self.z = value
        raise IndexError("Vector3 index out of range")

    def __pow__(self, exponent: Union[int, float]) -> "Vector3":
        """Raise each component to the specified exponent."""
        return Vector3(self.x**exponent, self.y**exponent, self.z**exponent)

    def __neg__(self) -> "Vector3":
        """Return the negation of the vector."""
        return Vector3(-self.x, -self.y, -self.z)

    def __pos__(self) -> "Vector3":
        """Return a copy of the vector."""
        return Vector3(self.x, self.y, self.z)

    def dot(self, other: "Vector3") -> Union[int, float]:
        """Calculate the dot product with another vector."""
        return self.x * other.x + self.y * other.y + self.z * other.z

    def cross(self, other: "Vector3") -> "Vector3":
        """Calculate the cross product with another vector."""
        return Vector3(
            self.y * other.z - self.z * other.y,
            self.z * other.x - self.x * other.z,
            self.x * other.y - self.y * other.x,
        )

    def length(self) -> float:
        """Calculate the length (magnitude) of the vector."""
        return sqrt(self.x**2 + self.y**2 + self.z**2)

    def length_squared(self) -> Union[int, float]:
        """Calculate the squared length of the vector."""
        return self.x**2 + self.y**2 + self.z**2

    def normalize(self) -> "Vector3":
        """Return a normalized copy of the vector."""
        length = self.length()
        if length != 0:
            return self / length
        return Vector3()

    def norm(self) -> float:
        """Calculate the Euclidean norm of the vector."""
        return sqrt(self.length_squared())
