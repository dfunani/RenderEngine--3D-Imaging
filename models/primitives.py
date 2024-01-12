"""
Module Summary: Contains object classes for line rendering.

Returns:
    Classes:
        Line: Represents a line object with defined endpoints and color.
"""

from typing import Union


class Line:
    """
    Represents a line between two points.

    Attributes:
        point_1 (tuple[float, float]): Coordinates of the starting point (x, y).
        x0 (float): x-coordinate of the starting point.
        y0 (float): y-coordinate of the starting point.
        point_2 (tuple[float, float]): Coordinates of the ending point (x, y).
        x1 (float): x-coordinate of the ending point.
        y1 (float): y-coordinate of the ending point.
        color (str): Color of the line.

    methods:
        __init__: Initializes a Line object with coordinates and color.
        __str__:L Returns a string representation of the Line object.
        swap_if_steep: Determines if the line is steep and swaps the
        coordinates if necessary.
        interpolation: Calculates the interpolation parameter for a given x-coordinate.
        get_y_value: Calculates the y-coordinate value for a given interpolation parameter.
    """

    def __init__(
        self,
        point_1: tuple[Union[int, float], Union[int, float]],
        point_2: tuple[Union[int, float], Union[int, float]],
        color: tuple[Union[int, float], Union[int, float], Union[int, float]],
    ) -> None:
        """
        Initializes a Line object with coordinates and color.

        Args:
            point_1 (tuple[Union[int, float], Union[int, float]]): Coordinates of the
                starting point (x, y).
            point_2 (tuple[Union[int, float], Union[int, float]]): Coordinates of the
                ending point (x, y).
            color (tuple[Union[int, float], Union[int, float],
                Union[int, float]]): Color of the line.
        """
        if not isinstance(point_1, tuple):
            raise TypeError("Point 1 must be a tuple[3] of int | float")
        if not isinstance(point_2, tuple):
            raise TypeError("Point 2 must be a tuple[3] of int | float")

        if not isinstance(color, tuple):
            raise TypeError("Color must be a tuple[3] of int | float")
        for i, v in enumerate(zip(point_1, point_2)):
            p1, p2 = v
            if not isinstance(p1, (int, float)):
                raise ValueError(f"Point 1 Coordinate[{i}] must be int | float")
            if not isinstance(p2, (int, float)):
                raise ValueError(f"Point 2 Coordinate[{i}] must be int | float")

        for i, v in enumerate(color):
            if not isinstance(v, (int, float)):
                raise ValueError(f"Color Coordinate[{i}] must be int | float")

        self.x0, self.y0 = point_1
        self.x1, self.y1 = point_2
        self.color = color

    def __str__(self) -> str:
        """
        Returns a string representation of the Line object.

        Returns:
            str: String representation of the Line object.
        """
        return f"Line from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1}) with color {self.color}"

    def swap_if_steep(self) -> bool:
        """
        Determines if the line is steep and swaps the coordinates if necessary.

        Returns:
            bool: True if the line is steep and coordinates are swapped, False otherwise.
        """
        # Determine if the line is steep
        steep = abs(self.x0 - self.x1) < abs(self.y0 - self.y1)

        if steep:
            # Swap x and y for steep selfs
            self.x0, self.y0 = self.y0, self.x0
            self.x1, self.y1 = self.y1, self.x1

        # Ensure x0 < x1
        if self.x0 > self.x1:
            self.x0, self.x1 = self.x1, self.x0
            self.y0, self.y1 = self.y1, self.y0
        return steep

    def get_y_value(self, x: Union[int, float]) -> int:
        """
        Calculates the interpolation parameter for a given x-coordinate
        to determine the y value.

        Args:
            interpolation_value (float): The interpolation
            parameter for calculating the y-coordinate.

        Returns:
            int: The calculated y-coordinate value.
        """
        interpolation_value = (x - self.x0) / (self.x1 - self.x0)
        return int(
            self.y0 * (1.0 - interpolation_value) + self.y1 * interpolation_value
        )
