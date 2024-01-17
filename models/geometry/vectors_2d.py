"""
geometry.vector_2d

This module defines a 2D vector class representing a point or direction in two-dimensional space.

Classes:
    Vector2:
        A 2D vector with x and y coordinates. Supports various mathematical operations.

Usage Example:
    from geometry.2d.vectors import Vector2

    # Create a vector
    v = Vector2(1.0, 2.0)

    # Perform operations
    v_normalized = v.normalize()
    length = v.length()

    # Check equality
    if v == Vector2(1.0, 2.0):
        print("Vectors are equal")

    # ... (other operations)

"""


from math import sqrt
from typing import Union

from models.interfaces.vectors import Vector


class Vector2(Vector):
    """
    A 2D vector class representing a point or direction in two-dimensional space.

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.

    Methods:
        __init__(x=0.0, y=0.0): Initializes a new Vector2 instance.
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
        __getitem__(index): Gets the value at the specified index (0 or 1).
        __setitem__(index, value): Sets the value at the specified index (0 or 1).
        __pow__(exponent): Raises each component to the specified exponent.
        __neg__(): Returns the negation of the vector.
        __pos__(): Returns a copy of the vector.
        dot(other): Calculates the dot product with another vector.
        length(): Calculates the length (magnitude) of the vector.
        length_squared(): Calculates the squared length of the vector.
        cross(other): Calculates the cross product with another vector.
        norm(): Calculates the Euclidean norm of the vector.

    Usage Example:
        v = Vector2(1.0, 2.0)
        v_normalized = v.normalize()
        length = v.length()
    """

    def __init__(
        self, x: Union[int, float] = 0.0, y: Union[int, float] = 0.0
    ) -> Union[TypeError, None]:
        """
        Initialize a 2D vector with specified coordinates.

        Parameters:
        - x (Union[int, float]): The x-coordinate of the vector. Defaults to 0.0.
        - y (Union[int, float]): The y-coordinate of the vector. Defaults to 0.0.

        Returns:
        None: This method does not return anything.

        Example:
        >>> vector = Vector2(x=3, y=4.5)
        >>> vector.x
        3
        >>> vector.y
        4.5
        """
        if not isinstance(x, (int, float)):
            raise TypeError("X value must be Int | Float")
        if not isinstance(y, (int, float)):
            raise TypeError("Y value must be Int | Float")
        self.x = x
        self.y = y

    def __repr__(self) -> str:
        """
        Return a string representation of the Vector2 instance.

        Returns:
        str: A string representation of the Vector2 instance in the format "Vector2(x, y)".

        Example:
        >>> vector = Vector2(x=3, y=4.5)
        >>> repr(vector)
        'Vector2(3, 4.5)'
        """
        return f"Vector2({self.x}, {self.y})"

    def __eq__(self, other: "Vector2") -> bool:
        """
        Check if two vectors are equal.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vectors are equal, False otherwise.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(1, 2)
        >>> vector3 = Vector2(3, 4)
        >>> vector1 == vector2
        True
        >>> vector1 == vector3
        False
        """
        if isinstance(other, Vector2):
            return self.x == other.x and self.y == other.y
        return False

    def __add__(
        self, other: Union["Vector2", int, float]
    ) -> Union["Vector2", TypeError]:
        """
        Add two vectors or add a scalar to the vector.

        Parameters:
        - other (Union["Vector2", int, float]): The vector or scalar to be added.

        Returns:
        Vector2: The result of the addition.

        Raises:
        TypeError: If the operand type is not supported.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(3, 4)
        >>> result = vector1 + vector2
        >>> repr(result)
        'Vector2(4, 6)'
        """
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x, self.y + other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x + other, self.y + other)
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def __sub__(
        self, other: Union["Vector2", int, float]
    ) -> Union["Vector2", TypeError]:
        """
        Subtract two vectors or subtract a scalar from the vector.

        Parameters:
        - other (Union["Vector2", int, float]): The vector or scalar to be subtracted.

        Returns:
        Vector2: The result of the subtraction.

        Raises:
        TypeError: If the operand type is not supported.

        Example:
        >>> vector1 = Vector2(3, 4)
        >>> vector2 = Vector2(1, 2)
        >>> result = vector1 - vector2
        >>> repr(result)
        'Vector2(2, 2)'
        """
        if isinstance(other, Vector2):
            return Vector2(self.x - other.x, self.y - other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x - other, self.y - other)
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def __mul__(
        self, other: Union["Vector2", int, float]
    ) -> Union["Vector2", TypeError]:
        """
        Multiply the vector by another vector or by a scalar.

        Parameters:
        - other (Union["Vector2", int, float]): The vector or scalar to be multiplied.

        Returns:
        Vector2: The result of the multiplication.

        Raises:
        TypeError: If the operand type is not supported.

        Example:
        >>> vector = Vector2(2, 3)
        >>> result = vector * 2
        >>> repr(result)
        'Vector2(4, 6)'
        """
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x, self.y * other.y)
        if isinstance(other, (int, float)):
            return Vector2(self.x * other, self.y * other)
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def __truediv__(
        self, other: Union["Vector2", int, float]
    ) -> Union["Vector2", TypeError]:
        """
        Divide the vector by another vector or by a scalar.

        Parameters:
        - other (Union["Vector2", int, float]): The vector or scalar to be divided.

        Returns:
        Vector2: The result of the division.

        Raises:
        TypeError: If the operand type is not supported.
        ZeroDivisionError: If dividing by zero.

        Example:
        >>> vector = Vector2(4, 6)
        >>> result = vector / 2
        >>> repr(result)
        'Vector2(2.0, 3.0)'
        """
        if isinstance(other, Vector2):
            return Vector2(self.x / other.x, self.y / other.y)
        if isinstance(other, (int, float)):
            if other != 0:
                return Vector2(self.x / other, self.y / other)
            raise ZeroDivisionError("Division by zero")
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def __neg__(self) -> "Vector2":
        """
        Negate the vector.

        Returns:
        Vector2: The negated vector.

        Example:
        >>> vector = Vector2(3, 4)
        >>> result = -vector
        >>> repr(result)
        'Vector2(-3, -4)'
        """
        return Vector2(-self.x, -self.y)

    # def __getitem__(self, index: int) -> Union[float, IndexError]:
    #     """
    #     Gets the value at the specified index (0 or 1).

    #     Args:
    #         index (int): The index of the component (0 for x, 1 for y).

    #     Returns:
    #         float: The value of the component at the specified index.

    #     Raises:
    #         IndexError: If the index is out of range (not 0 or 1).
    #     """
    #     if index == 0:
    #         return self.x
    #     if index == 1:
    #         return self.y
    #     raise IndexError("Vector2 index out of range")

    # def __setitem__(self, index: int, value: float) -> Union[IndexError, None]:
    #     """
    #     Sets the value at the specified index (0 or 1).

    #     Args:
    #         index (int): The index of the component (0 for x, 1 for y).
    #         value (float): The new value for the component.

    #     Raises:
    #         IndexError: If the index is out of range (not 0 or 1).
    #     """
    #     if index == 0:
    #         self.x = value
    #     elif index == 1:
    #         self.y = value
    #     raise IndexError("Vector2 index out of range")

    def __pow__(self, exponent: float) -> "Vector2":
        """
        Raises each component to the specified exponent.

        Args:
            exponent (float): The exponent to raise each component to.

        Returns:
            Vector2: A new Vector2 instance with components raised to the specified exponent.
        """
        return Vector2(self.x**exponent, self.y**exponent)

    def __pos__(self) -> "Vector2":
        """
        Returns a copy of the vector.

        Returns:
            Vector2: A new Vector2 instance with the same components.
        """
        return Vector2(self.x, self.y)

    def dot(self, other: "Vector2") -> Union[float, TypeError]:
        """
        Calculate the dot product of two vectors.

        Parameters:
        - other: The vector to calculate the dot product with.

        Returns:
        float: The dot product of the two vectors.

        Raises:
        TypeError: If the operand type is not supported.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(3, 4)
        >>> result = vector1.dot(vector2)
        >>> result
        11
        """
        if isinstance(other, Vector2):
            return self.x * other.x + self.y * other.y
        raise TypeError(f"Unsupported operand type: {type(other)}")

    def length(self) -> float:
        """
        Calculate the length (magnitude) of the vector.

        Returns:
        float: The length of the vector.

        Example:
        >>> vector = Vector2(3, 4)
        >>> vector.length()
        5.0
        """
        return sqrt(self.x**2 + self.y**2)

    def length_squared(self) -> float:
        """
        Calculates the squared length of the vector.

        Returns:
            float: The squared length of the vector.
        """
        return self.x**2 + self.y**2

    def normalize(self) -> "Vector2":
        """
        Normalize the vector, returning a new vector with the same direction and a length of 1.

        Returns:
        Vector2: The normalized vector.

        Example:
        >>> vector = Vector2(3, 4)
        >>> normalized_vector = vector.normalize()
        >>> repr(normalized_vector)
        'Vector2(0.6, 0.8)'
        """
        length = self.length()
        if length != 0:
            return self / length
        return Vector2()

    def norm(self) -> float:
        """
        Calculates the Euclidean norm of the vector.

        Returns:
            float: The Euclidean norm of the vector.
        """
        return sqrt(self.length_squared())

    def cross(self, other: "Vector2") -> "Vector2":
        """
        Calculates the "cross product" of two 2D vectors.

        Parameters:
            other (Vector2): The other vector.

        Returns:
            float: The "cross product" of the two vectors.

        Raises:
            TypeError: If the operand type is not supported.

        Note:
            This is a custom definition for a cross product in 2D, which may not align
            with the traditional cross product definition in 3D.
        """
        return Vector2(
            self.y * other.x - self.x * other.y,
            self.x * other.y - self.y * other.x,
        )

    def to_tuple(self) -> tuple[int, int]:
        """
        Convert the vector to a tuple of integers.

        Returns:
        tuple: A tuple containing the x and y coordinates as integers.

        Example:
        >>> vector = Vector2(3.2, 4.8)
        >>> result = vector.to_tuple()
        >>> result
        (3, 4)
        """
        return int(self.x), int(self.y)
