"""
Module Summary: Contains object classes for line rendering.

Returns:
    Classes:
        Line: Represents a line object with defined endpoints and color.
"""

from typing import Union

from models.vectors import Vector2, RGB, Vector3
from utils.generators import HEIGHT, WIDTH


class Line:
    """
    Represents a line between two points.

    Attributes:
        point_1 (Vector2): Coordinates of the starting point (x, y).
        x0 (int, float): x-coordinate of the starting point.
        y0 (int, float): y-coordinate of the starting point.
        point_2 (Vector2): Coordinates of the ending point (x, y).
        x1 (int, float): x-coordinate of the ending point.
        y1 (int, float): y-coordinate of the ending point.
        color (str): Color of the line.

    methods:
        __init__: Initializes a Line object with coordinates and color.
        __str__: Returns a string representation of the Line object.
        swap_if_steep: Determines if the line is steep and swaps the
        coordinates if necessary.
        interpolation: Calculates the interpolation parameter for a given x-coordinate.
        get_y_value: Calculates the y-coordinate value for a given interpolation parameter.
    """

    def __init__(
        self,
        point_1: Vector2,
        point_2: Vector2,
        color: RGB,
    ) -> None:
        """
        Initializes a Line object with coordinates and color.

        Args:
            point_1 (Vector2): Coordinates of the
                starting point (x, y).
            point_2 (Vector2): Coordinates of the
                ending point (x, y).
            color (RGB): Color of the line.
        """
        if not isinstance(point_1, Vector2):
            raise TypeError("Point 1 must be a 2D Vector")
        if not isinstance(point_2, Vector2):
            raise TypeError("Point 2 must be a 2D Vector")
        if not isinstance(color, RGB):
            raise TypeError("Color must be RGB")
        self.x0, self.y0 = point_1.coordinates
        self.x1, self.y1 = point_2.coordinates
        self.color = color

    def __str__(self) -> str:
        """
        Returns a string representation of the Line object.

        Returns:
            str: String representation of the Line object.
        """
        return f"Line from ({self.x0}, {self.y0}) to ({self.x1}, {self.y1}) with {self.color}"

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


class Triangle:
    """
    Represents a triangle in 2D space.

    Attributes:
        vertices (list[Vector2]): List of three Vector2 vertices (x, y).
        color (RGB): RGB color of the triangle.
    """

    def __init__(self, vertices: list[Vector2], color: RGB):
        """
        Initializes a Triangle object with vertices and color.

        Args:
            vertices (list[Vector2]): List of three vertices (x, y).
            color (Tuple[Vector3]): RGB color of the triangle.
        """
        if len(vertices) != 3:
            raise ValueError("A triangle must have three Vector2 vertices.")
        self.vertices = vertices
        self.color = color

    def draw_vertices(self, lines) -> list[Line]:
        self.swap()
        lines.append(Line(self.vertices[0], self.vertices[1], self.color))
        lines.append(Line(self.vertices[1], self.vertices[2], self.color))
        lines.append(Line(self.vertices[2], self.vertices[0], self.color))
        return lines

    def draw_triangle(self, image):
        t0, t1, t2 = self.vertices[0], self.vertices[1], self.vertices[2]

        if t0.y == t1.y == t2.y:
            return image  # I don't care about degenerate triangles

        # Sort the vertices, t0, t1, t2 lower-to-upper (bubblesort)
        self.swap()

        total_height = t2.y - t0.y

        for i in range(int(total_height) + 1):  # Adjusted the loop range
            second_half = i > t1.y - t0.y or t1.y == t0.y
            segment_height = t2.y - t1.y if second_half else t1.y - t0.y
            alpha = i / total_height
            beta = (i - (t1.y - t0.y) if second_half else 0) / segment_height

            A = t0 + (t2 - t0) * alpha
            B = t1 + (t2 - t1) * beta if second_half else t0 + (t1 - t0) * beta

            if A.coordinates[0] > B.coordinates[0]:
                A, B = B, A

            for j in range(
                max(0, int(A.coordinates[0])),
                min(WIDTH - 1, int(B.coordinates[0])) + 1,
            ):
                # Adjust the starting point for the second half of the triangle
                y_index = (
                    max(0, min(HEIGHT - 1, int(t0.y + i)))
                    if not second_half
                    else max(0, min(HEIGHT - 1, int(t1.y + i)))
                )
                image[y_index][j] = self.color

        return image


    def swap(self) -> None:
        if self.vertices[0].y > self.vertices[1].y:
            self.vertices[0], self.vertices[1] = self.vertices[1], self.vertices[0]
        if self.vertices[0].y > self.vertices[2].y:
            self.vertices[0], self.vertices[2] = self.vertices[2], self.vertices[0]
        if self.vertices[1].y > self.vertices[2].y:
            self.vertices[1], self.vertices[2] = self.vertices[2], self.vertices[1]
