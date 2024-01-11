"""
Vector Operations Module

This module defines a versatile Vector class for vector operations, including
basic arithmetic, comparison, and vector-specific operations such as dot product
and cross product.

Classes:
    Vector: Base Class for vectors with various mathematical operations.
    Vector2: Represents a 2D vector with various mathematical operations.
    Vector3: Represents a 3D vector with various mathematical operations.
    RGB: Represents a 3D vector with various mathematical operations, used to represent Colour.

Usage:
    from vectors import Vector, Vector2, Vector3, RGB

    # Create vectors
    old_vector = Vector(1, 2, 3)
    new_vector = Vector(1, 2, 3)
    vector3 = Vector3(1, 2, 3)
    color = RGB(224, 25, 6)

    # Perform operations
    result_addition = old_vector + new_vector
    result_dot_product = old_vector @ new_vector
    result_cross_product = old_vector.cross(new_vector)

    # Other vector methods and comparisons
    len_old_vector = len(old_vector)
    bool_old_vector = bool(old_vector)
    normalized_old_vector = old_vector.normalize()

"""
from math import sqrt
from typing import Union
from models.types.exceptions import ArgumentError


class Vector:
    """
    Vector Class

    Represents a vector with various mathematical operations.

    Methods:
        __init__: Initializes a Vector object with given coordinates.
        __str__: Returns a string representation of the Vector object.
        __eq__: Checks if two Vector objects are equal.
        __ne__: Checks if two Vector objects are not equal.
        __lt__: Checks if the norm of the current Vector is less than the norm of another.
        __le__: Checks if the norm of the current Vector is less than or equal
                to the norm of another.
        __gt__: Checks if the norm of the current Vector is greater than the norm of another.
        __ge__: Checks if the norm of the current Vector is greater
                than or equal to the norm of another.
        __len__: Returns the number of coordinates in the Vec.
        __add__: Adds two Vector objects element-wise.
        __sub__: Subtracts one Vector object from another element-wise.
        __mul__: Multiplies a Vector object by a scalar or element-wise by another Vec.
        __rmul__: Allows scalar multiplication on the right side.
        __matmul__: Calculates the dot product of two Vector objects.
        __bool__: Checks if any coordinate in the Vector is non-zero.
        __getitem__: Gets the value of a specific coordinate in the Vec.
        __xor__: Performs bitwise XOR with another vector.
        __lshift__: Performs left bit shift on each coordinate of the vector.
        norm: Calculates the norm (length) of the Vec.
        normalize: Normalizes the Vector to a specified length.

    Usage:
        vector = Vector(1, 2, 3)
        result = vector + Vector(4, 5, 6)
    """

    def __init__(self, *args: tuple[Union[int, float]]) -> None:
        """
        Initializes a Vector object with given coordinates.

        Args:
            args (float): Variable number of coordinates for the vector.

        Raises:
            TypeError: If any argument is not of type int or float.
            ArgumentError: If no arguments are provided.
        """
        for index, arg in enumerate(args):
            if not isinstance(arg, (int, float)):
                raise TypeError(f"Argument at position {index} is an INVALID type.")
        if not args:
            raise ArgumentError("No arguments were provided.")
        self.coordinates = args

    def __str__(self) -> str:
        """
        Returns a string representation of the Vector object.

        Returns:
            str: A Descriptive string representation of the Vector object.
        """
        coordinates_str = ", ".join(map(str, self.coordinates))
        return f"{self.__class__.__name__} with Coordinates: ({coordinates_str})"

    def __eq__(self, other: "Vector") -> bool:
        """
        Checks if two Vector objects are equal.

        Args:
            other (Vector): Another Vector object for comparison.

        Returns:
            bool: True if the vectors are equal, False otherwise.
        """
        if isinstance(other, Vector):
            return self.coordinates == other.coordinates
        return False

    def __ne__(self, other: "Vector") -> bool:
        """
        Checks if two Vector objects are not equal.

        Args:
            other (Vector): Another Vector object for comparison.

        Returns:
            bool: True if the vectors are not equal, False if they are equal.
        """
        return not self.__eq__(other)

    def __lt__(self, other: Union["Vector", int, float]) -> Union[bool, ValueError]:
        """
        Checks if the norm of the vector is less than the norm of
        another vector or a scalar.

        Args:
            other (Union[Vector, int, float]): Another Vector object,
            scalar, or float for comparison.

        Returns:
            bool: True if the norm of the vector is less than the norm of
            the other value, False otherwise.
        """
        if isinstance(other, Vector):
            return self.norm() < other.norm()
        if isinstance(other, (int, float)):
            return self.norm() < other
        raise ValueError("Comparison is only defined for vectors or scalar values.")

    def __le__(self, other: Union["Vector", int, float]) -> Union[bool, ValueError]:
        """
        Checks if the norm of the vector is less than or equal to the norm of another
        vector or a scalar.

        Args:
            other (Union[Vector, int, float]): Another Vector object, scalar, or float
            for comparison.

        Returns:
            bool: True if the norm of the vector is less than or equal to the norm of the
            other value, False otherwise.
        """
        if isinstance(other, Vector):
            return self.norm() <= other.norm()
        if isinstance(other, (int, float)):
            return self.norm() <= other
        raise ValueError("Comparison is only defined for vectors or scalar values.")

    def __gt__(self, other: Union["Vector", int, float]) -> Union[bool, ValueError]:
        """
        Checks if the norm of the vector is greater than the norm of another vector or
        a scalar.

        Args:
            other (Union[Vector, int, float]): Another Vector object, scalar, or float
            for comparison.

        Returns:
            bool: True if the norm of the vector is greater than the norm of the other
            value, False otherwise.
        """
        if isinstance(other, Vector):
            return self.norm() > other.norm()
        if isinstance(other, (int, float)):
            return self.norm() > other
        raise ValueError("Comparison is only defined for vectors or scalar values.")

    def __ge__(self, other: Union["Vector", int, float]) -> Union[bool, ValueError]:
        """
        Checks if the norm of the vector is greater than or equal to the norm of
        another vector or a scalar.

        Args:
            other (Union[Vector, int, float]): Another Vector object, scalar, or
            float for comparison.

        Returns:
            bool: True if the norm of the vector is greater than or equal to the norm
            of the other value, False otherwise.
        """
        if isinstance(other, Vector):
            return self.norm() >= other.norm()
        if isinstance(other, (int, float)):
            return self.norm() >= other
        raise ValueError("Comparison is only defined for vectors or scalar values.")

    def __len__(self) -> int:
        """
        Returns the number of coordinates in the vector.

        Returns:
            int: The number of coordinates in the vector.
        """
        return len(self.coordinates)

    def __add__(
        self, other: Union["Vector", int, float]
    ) -> Union["Vector", ValueError]:
        """
        Adds two vectors element-wise or adds a scalar to each coordinate.

        Args:
            other (Union[Vector, int, float]): Another Vector object, scalar, or float for addition.

        Returns:
            Vector: A new Vector resulting from the element-wise addition.
        """
        if isinstance(other, Vector) and len(self.coordinates) == len(
            other.coordinates
        ):
            result_coordinates = [
                a + b for a, b in zip(self.coordinates, other.coordinates)
            ]
            return Vector(*result_coordinates)
        if isinstance(other, (int, float)):
            result_coordinates = [comp + other for comp in self.coordinates]
            return Vector(*result_coordinates)
        raise ValueError("Addition is only defined for vectors or scalar values.")

    def __sub__(
        self, other: Union["Vector", int, float]
    ) -> Union["Vector", ValueError]:
        """
        Subtracts another vector element-wise.

        Args:
            other (Vector): Another Vector object for subtraction.

        Returns:
            Vector: A new Vector resulting from the element-wise subtraction.
        """
        if isinstance(other, Vector) and len(self.coordinates) == len(
            other.coordinates
        ):
            result_coordinates = [
                a - b for a, b in zip(self.coordinates, other.coordinates)
            ]
            return Vector(*result_coordinates)
        if isinstance(other, (int, float)):
            result_coordinates = [comp - other for comp in self.coordinates]
            return Vector(*result_coordinates)
        raise ValueError(
            "Subtraction is only defined for vectors of the same dimension."
        )

    def __mul__(self, f: Union["Vector", int, float]) -> Union["Vector", ValueError]:
        """
        Multiplies the vector by a scalar or performs element-wise multiplication.

        Args:
            f (Union[int, float, Vector]): The scalar or another Vector for multiplication.

        Returns:
            Vector: A new Vector resulting from the multiplication.
        """
        if isinstance(f, (int, float)):
            result_coordinates = [comp * f for comp in self.coordinates]
            return Vector(*result_coordinates)
        if isinstance(f, Vector) and len(self.coordinates) == len(f.coordinates):
            result_coordinates = [
                a * b for a, b in zip(self.coordinates, f.coordinates)
            ]
            return Vector(*result_coordinates)
        raise ValueError(
            "Multiplication is only defined for scalar or vector operands."
        )

    def __rmul__(self, f: Union["Vector", int, float]) -> Union["Vector", ValueError]:
        """
        Multiplies the vector by a scalar when the scalar is on the right side.

        Args:
            f (Union[int, float]): The scalar for multiplication.

        Returns:
            Vector: A new Vector resulting from the multiplication.
        """
        return self.__mul__(f)

    def __matmul__(self, other) -> int:
        """
        Calculates the dot product of two vectors.

        Args:
            other (Vector): Another Vector object for the dot product.

        Returns:
            float: The dot product of the two vectors.
        """
        return self.dot(other)

    def __bool__(self) -> bool:
        """
        Checks if any coordinate in the vector is non-zero.

        Returns:
            bool: True if any coordinate in the vector is non-zero, False otherwise.
        """
        return any(coord != 0 for coord in self.coordinates)

    def __getitem__(self, index: int) -> Union[int, float]:
        """
        Gets the coordinate at the specified index.

        Args:
            index (int): The index of the coordinate to retrieve.

        Returns:
            float: The value of the coordinate at the specified index.
        """
        return self.coordinates[index]

    def __xor__(self, other: "Vector") -> Union["Vector", ValueError]:
        if isinstance(other, Vector) and len(self.coordinates) == len(
            other.coordinates
        ):
            # Bitwise XOR for each corresponding coordinate
            result_coordinates = [
                a ^ b for a, b in zip(self.coordinates, other.coordinates)
            ]
            return Vector(*result_coordinates)
        raise ValueError(
            "Bitwise XOR is only defined for vectors of the same dimension."
        )

    # def __lshift__(self, shift_amount):
    #     # Left bit shift for each coordinate
    #     result_coordinates = [coord << shift_amount for coord in self.coordinates]
    #     return Vector(*result_coordinates)

    def dot(self, other: "Vector") -> Union["Vector", ValueError]:
        """
        Calculates the dot product of two vectors.

        Args:
            other (Vector): Another Vector object for the dot product.

        Returns:
            float: The dot product of the two vectors.
        """
        if isinstance(other, Vector) and len(self.coordinates) == len(other.coordinates):
            return sum(a * b for a, b in zip(self.coordinates, other.coordinates))
        raise ValueError("Dot product is only defined for vectors of the same dimension.")

    def norm(self)  -> float:
        """
        Calculates the Euclidean norm (length) of the vector.

        Returns:
            float: The Euclidean norm of the vector.
        """
        return sqrt(sum(comp**2 for comp in self.coordinates))

    def normalize(self, l: int = 1) -> "Vector":
        """
        Normalizes the vector to a specified length.

        Args:
            l (float, optional): The desired length for the normalized vector. Defaults to 1.

        Returns:
            Vector: A new Vector representing the normalized vector.
        """
        length = self.norm()
        return Vector(*[comp * l / length for comp in self.coordinates])


class Vector3(Vector):
    """
    Vector2 Class

    Represents a 2D vector with coordinates x and y.

    ...

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.

    Methods:
        __init__: Initializes a Vector2 object with given x and y coordinates.
        cross: Calculates the cross product of two 3D Vector objects.

    Usage:
        v = Vector2(1, 2)
    """

    def __init__(
        self,
        x: Union[int, float] = 0,
        y: Union[int, float] = 0,
        z: Union[int, float] = 0,
    ) -> None:
        """
        Initializes a Vector2 object with given x and y coordinates.

        Args:
            x (float): The x-coordinate of the vector.
            y (float): The y-coordinate of the vector.
            z (float): The z-coordinate of the vector.
        """
        super().__init__(x, y, z)

    def cross(self, other: 'Vector') -> "Vector":
        """
        Calculates the cross product of two 3D Vector objects.

        Args:
            other (Vector): Another 3D Vector object.

        Returns:
            Vector: A new Vector representing the cross product.

        Raises:
            ValueError: If either of the vectors is not 3D.
        """
        return Vector(
            self.coordinates[1] * other.coordinates[2]
            - self.coordinates[2] * other.coordinates[1],
            self.coordinates[2] * other.coordinates[0]
            - self.coordinates[0] * other.coordinates[2],
            self.coordinates[0] * other.coordinates[1]
            - self.coordinates[1] * other.coordinates[0],
        )


class Vector2(Vector):
    """
    Vector2 Class

    Represents a 2D vector with coordinates x and y.

    ...

    Attributes:
        x (float): The x-coordinate of the vector.
        y (float): The y-coordinate of the vector.

    Methods:
        __init__: Initializes a Vector2 object with given x and y coordinates.

    Usage:
        v = Vector2(1, 2)
    """

    def __init__(
        self,
        x: Union[int, float] = 0,
        y: Union[int, float] = 0,
    ) -> None:
        """
        Initializes a Vector2 object with given x and y coordinates.

        Args:
            x (float): The x-coordinate of the vector.
            y (float): The y-coordinate of the vector.
        """
        super().__init__(x, y)


class RGB(Vector):
    """
    RGB Class

    Represents an RGB color with red (r), green (g), and blue (b) components.

    ...

    Attributes:
        r (float): The red component of the color.
        g (float): The green component of the color.
        b (float): The blue component of the color.

    Methods:
        __init__: Initializes an RGB object with given r, g, and b components.
        __str__: Returns a string representation of the RGB object.

    Usage:
        color = RGB(255, 0, 0)
    """

    def __init__(
        self,
        r: Union[int, float] = 0,
        g: Union[int, float] = 0,
        b: Union[int, float] = 0,
    ) -> None:
        """
        Initializes an RGB object with given r, g, and b components.

        Args:
            r (float): The red component of the color.
            g (float): The green component of the color.
            b (float): The blue component of the color.
        """
        super().__init__(r, g, b)

    def __str__(self) -> str:
        """
        Returns a string representation of the RGB object.

        Returns:
            str: A personalized string representation for RGB.
        """
        if self.coordinates != 3:
            raise ArgumentError("RGB Requires 3 coordinates.")
        r = self.coordinates[0]
        g = self.coordinates[1]
        b = self.coordinates[2]
        coordinates = f"(R: {r}, G: {g}, B: {b})"
        return f"RGB Color {coordinates}"
