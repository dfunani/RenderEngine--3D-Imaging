from typing import Union


class Vector:
    def __ne__(self, other: "Vector") -> bool:
        """
        Check if two vectors are not equal.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vectors are not equal, False otherwise.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(3, 4)
        >>> vector1 != vector2
        True
        """
        return not self.__eq__(other)

    def __gt__(self, other: "Vector") -> bool:
        """
        Check if the vector is greater than another vector.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vector is greater than the other, False otherwise.

        Example:
        >>> vector1 = Vector2(3, 4)
        >>> vector2 = Vector2(1, 2)
        >>> vector1 > vector2
        True
        """
        return self.length() > other.length()

    def __ge__(self, other: "Vector") -> bool:
        """
        Check if the vector is greater than or equal to another vector.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vector is greater than or equal to the other, False otherwise.

        Example:
        >>> vector1 = Vector2(3, 4)
        >>> vector2 = Vector2(1, 2)
        >>> vector1 >= vector2
        True
        """
        return self.length() >= other.length()

    def __lt__(self, other: "Vector") -> bool:
        """
        Check if the vector is less than another vector.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vector is less than the other, False otherwise.

        Raises:
        TypeError: If the operand type is not supported.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(3, 4)
        >>> vector1 < vector2
        True
        """
        return self.length() < other.length()

    def __le__(self, other: "Vector") -> bool:
        """
        Check if the vector is less than or equal to another vector.

        Parameters:
        - other (Vector2): The vector to be compared.

        Returns:
        bool: True if the vector is less than or equal to the other, False otherwise.

        Example:
        >>> vector1 = Vector2(1, 2)
        >>> vector2 = Vector2(3, 4)
        >>> vector1 <= vector2
        True
        """
        return self.length() <= other.length()

    def _get_component(self, index: int) -> Union[IndexError, int, float]:
        """Get the value at the specified index."""
        if 0 <= index < len(self.__dict__):
            return getattr(self, ["x", "y", "z", "w"][index])
        raise IndexError("Vector index out of range")

    def _set_component(self, index: int, value: Union[int, float, "Vector"]) -> Union[None, IndexError]:
        """Set the value at the specified index."""
        if 0 <= index < len(self.__dict__):
            setattr(self, ["x", "y", "z", "w"][index], value)
            return None
        raise IndexError("Vector index out of range")