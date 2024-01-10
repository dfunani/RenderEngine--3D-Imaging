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
    """

    def __init__(
        self,
        point_1: tuple[Union[int, float], Union[int, float]],
        point_2: tuple[Union[int, float], Union[int, float]],
        color: tuple[int, int, int],
    ):
        """
        Initializes a Line object with coordinates and color.

        Args:
            point_1 (tuple[float, float]): Coordinates of the starting point (x, y).
            point_2 (tuple[float, float]): Coordinates of the ending point (x, y).
            color (str): Color of the line.
        """
        self.x0, self.y0 = point_1
        self.x1, self.y1 = point_2
        self.color = color

    def __str__(self):
        """
        Returns a string representation of the Line object.

        Returns:
            str: String representation of the Line object.
        """
        return f"Line from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1}) with color {self.color}"

    def interpolate(self):
        """
        Calculates an interpolated point on the line for a given parameter value.

        Args:
            t (float): Parameter value for interpolation.

        Returns:
            Tuple[float, float]: The interpolated point's (x, y) coordinates.
        """
        dx = abs(self.x1 - self.x0)
        dy = abs(self.y1 - self.y0)
        return dx, dy

    def change_direction(self) -> tuple[int, int]:
        """
        Determines the direction of the line between its endpoints.

        Returns:
            tuple[int, int]: A tuple representing x and y direction increments for the line.
        """
        if self.x0 < self.x1:
            x_increment = 1
        else:
            x_increment = -1
        if self.y0 < self.y1:
            y_increment = 1
        else:
            y_increment = -1
        return x_increment, y_increment
