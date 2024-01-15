"""
Module Summary: Contains object classes for line rendering and 2D triangle rendering.

Returns:
    Classes:
        Line: Represents a line object with defined endpoints and color.
        Triangle: Represents a triangle in 2D space.

Description:
    This module provides classes for rendering lines and triangles in 2D space. 
    The Line class represents a line between two points, and the Triangle class 
    represents a triangle 
    defined by three vertices. These classes include methods for rendering lines 
    and triangles on an image.

Classes:
    Line:
        Represents a line between two points.

        Attributes:
            point_1 (Vector2): Coordinates of the starting point (x, y).
            x0 (int, float): x-coordinate of the starting point.
            y0 (int, float): y-coordinate of the starting point.
            point_2 (Vector2): Coordinates of the ending point (x, y).
            x1 (int, float): x-coordinate of the ending point.
            y1 (int, float): y-coordinate of the ending point.
            color (str): Color of the line.

        Methods:
            __init__: Initializes a Line object with coordinates and color.
            __str__: Returns a string representation of the Line object.
            swap_if_steep: Determines if the line is steep and swaps the
            coordinates if necessary.
            interpolation: Calculates the interpolation parameter for a given x-coordinate.
            get_y_value: Calculates the y-coordinate value for a given interpolation parameter.
            draw_line: Renders the line on an image.

    Triangle:
        Represents a triangle in 2D space.

        Attributes:
            vertices (list[Vector2]): List of three Vector2 vertices (x, y).
            color (RGB): RGB color of the triangle.

        Methods:
            __init__: Initializes a Triangle object with vertices and color.
            __str__: Returns a string representation of the Triangle object.
            draw_vertices: Appends each vertex as a line to the list of lines to be rendered.
            draw_triangle: Renders the triangle on an image.
            swap: Swaps the vertices of the triangle if needed.
"""

from typing import Union

from models.vectors import Vector2, RGB
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

    Methods:
        __init__: Initializes a Line object with coordinates and color.
        __str__: Returns a string representation of the Line object.
        swap_if_steep: Determines if the line is steep and swaps the
        coordinates if necessary.
        interpolation: Calculates the interpolation parameter for a given x-coordinate.
        get_y_value: Calculates the y-coordinate value for a given interpolation parameter.
        draw_line: Renders the line on an image.
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

    def draw_line(self, image: list) -> list:
        """
        Renders the line on an image.

        Args:
            image (list): List of Bytes to write each Vertex/Pixel.

        Returns:
            image (list): Updated List of Bytes to write each Vertex/Pixel.
        """
        steep = self.swap_if_steep()
        for x in range(int(self.x0), int(self.x1) + 1):
            y = self.get_y_value(x)
            if steep:
                image[x][y] = self.color
            else:
                image[y][x] = self.color
        return image


class Triangle:
    """
    Represents a triangle in 2D space.

    Attributes:
        vertices (list[Vector2]): List of three Vector2 vertices (x, y).
        color (RGB): RGB color of the triangle.

    Methods:
        __init__: Initializes a Triangle object with vertices and color.
        __str__: Returns a string representation of the Line object.
        draw_vertices: Appends each vertex as a line to the list of lines to be rendered.
        draw_triangle: Renders the triangle on an image.
        swap: Swaps the vertices of the triangle if needed.
    """

    def __init__(
        self, vertex_1: Vector2, vertex_2: Vector2, vertex_3: Vector2, color: RGB
    ) -> None:
        """
        Initializes a Triangle object with vertices and color.

        Args:
            vertex_1 (Vector2): 2D Vertices (x, y).
            vertex_2 (Vector2): 2D Vertices (x, y).
            vertex_3 (Vector2): 2D Vertices (x, y).
            color (RGB): RGB color of the triangle.
        """
        self.vertex_1 = vertex_1
        self.vertex_2 = vertex_2
        self.vertex_3 = vertex_3
        self.color = color

    def __str__(self) -> str:
        """
        Returns a string representation of the Line object.

        Returns:
            str: String representation of the Line object.
        """
        vertex_string = f"({self.vertex_1}), ({self.vertex_2}), ({self.vertex_3})"
        return f"Triangle with Vertices {vertex_string} with {self.color}"

    def draw_vertices(self, lines: list[Line]) -> list[Line]:
        """
        Append each vertice to the list of lines to be rendered
        in an image.

        Args:
            lines (list[Line]): List of Lines to draw.

        Returns:
            list[Lines]: List of the lines to be drawn.
        """
        self.swap()
        lines.append(Line(self.vertex_1, self.vertex_2, self.color))
        lines.append(Line(self.vertex_2, self.vertex_3, self.color))
        lines.append(Line(self.vertex_3, self.vertex_1, self.color))
        return lines

    def draw_triangle(self, image: list) -> list:
        """
        Draw each vertex to the image plane.

        Args:
            image (list): List of Bytes to write each Vertex/Pixel.

        Returns:
            image (list): Updated List of Bytes to write each Vertex/Pixel.
        """
        vertex_1, vertex_2, vertex_3 = self.vertex_1, self.vertex_2, self.vertex_3

        if vertex_1.y == vertex_2.y == vertex_3.y:
            return image  # I don't care about degenerate triangles

        # Sort the vertices, vertex_1, vertex_2, vertex_3 lower-to-upper (bubblesort)
        self.swap()

        total_height = vertex_3.y - vertex_1.y

        for i in range(int(total_height) + 1):  # Adjusted the loop range
            second_half = i > vertex_2.y - vertex_1.y or vertex_2.y == vertex_1.y
            segment_height = (
                vertex_3.y - vertex_2.y if second_half else vertex_2.y - vertex_1.y
            )
            alpha = i / total_height
            beta = (
                i - (vertex_2.y - vertex_1.y) if second_half else 0
            ) / segment_height

            alpha_vertex = vertex_1 + (vertex_3 - vertex_1) * alpha
            beta_vertex = (
                vertex_2 + (vertex_3 - vertex_2) * beta
                if second_half
                else vertex_1 + (vertex_2 - vertex_1) * beta
            )

            if alpha_vertex.x > beta_vertex.x:
                alpha_vertex, beta_vertex = beta_vertex, alpha_vertex

            for j in range(
                max(0, int(alpha_vertex.x)),
                min(WIDTH - 1, int(beta_vertex.x)) + 1,
            ):
                # Adjust the starting point for the second half of the triangle
                y_index = (
                    max(0, min(HEIGHT - 1, int(vertex_1.y + i)))
                    if not second_half
                    else max(0, min(HEIGHT - 1, int(vertex_2.y + i)))
                )
                image[int(y_index)][int(j)] = self.color

        return image

    def swap(self) -> None:
        """
        Swaps the Vertices:
            1. if Vertex 2 is Greater Vertex 3.
            2. if Vertex 1 is Greater Vertex 3.
            3. if Vertex 2 is Greater Vertex 3.
        """
        if self.vertex_1.y > self.vertex_2.y:
            self.vertex_1, self.vertex_2 = self.vertex_2, self.vertex_1
        if self.vertex_1.y > self.vertex_3.y:
            self.vertex_1, self.vertex_3 = self.vertex_3, self.vertex_1
        if self.vertex_2.y > self.vertex_3.y:
            self.vertex_2, self.vertex_3 = self.vertex_3, self.vertex_2
