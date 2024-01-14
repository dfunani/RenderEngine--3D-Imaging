"""
Module Summary: Contains functions for rendering lines on images.

This module provides functions for rendering lines on images using various algorithms.

Functions:
    render_line: Renders a line on an image given its dimensions and output file.

Returns:
    Functions:
        render_line: Renders a line on an image.
        file_writer: Write the line or image to a file.
"""

from random import randint
from models.objects import Model
from models.primitives import Line, Triangle
from models.vectors import (
    RGB,
    Vector2,
    Vector3,
)  # Import the Line class from your objects module
from utils.generators import frame_buffer

WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image


def render_triangle_shaded(triangles: list[Triangle], filename="triangle"):
    """
    Adds a Triangle object to the list of triangles to render.

    Args:
        triangle (Triangle): Triangle object to add.

    Renders all triangles to a PPM file.

    Args:
        filename (str): Name of the output PPM file.
    """
    image = frame_buffer()

    # Barycentric interpolation for shading
    for triangle in triangles:
        image = triangle.draw_triangle(image)
    file_writer(image, filename)
    

def render_triangle_outline(triangles: list[Triangle], filename="triangle_outline"):
    # Render lines
    image = frame_buffer()
    # Draw vertices
    for triangle in triangles:
        lines = triangle.draw_vertices([])
        for line in lines:
            steep = line.swap_if_steep()
            for x in range(int(line.x0), int(line.x1) + 1):
                y = line.get_y_value(x)
                if steep:
                    image[x][y] = line.color
                else:
                    image[y][x] = line.color
    file_writer(image, filename)


def render_model_shaded(
    model_filename: str, output_filename: str = "model_shaded", color=RGB(255, 255, 255)
) -> None:
    model = Model(model_filename)
    image = frame_buffer()
    light_dir = Vector3(0, 0, -1)
    for face_index in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(face_index)
        screen_coords = []
        world_coords = []
        for i in range(3):
            v = model.get_vertex(face[i])
            screen_coords.append(
                Vector2((v.x + 1.0) * WIDTH / 2.0, (v.y + 1.0) * HEIGHT / 2.0)
            )
            world_coords.append(v)

        n = (world_coords[2] - world_coords[0]) ^ (world_coords[1] - world_coords[0])
        n.normalize()
        intensity = light_dir * n
        if intensity > 0:
            triangle = Triangle([screen_coords[0], screen_coords[1], screen_coords[2]], RGB(255, 0, 0))
            image = triangle.draw_triangle(image)
    file_writer(image, output_filename)


def render_model(
    model_filename: str, output_filename: str = "model", color=RGB(255, 255, 255)
) -> None:
    """
    Renders a 3D model to an image file.

    Args:
        model_filename (str): The filename of the 3D model in OBJ format.
        output_filename (str, optional): The name of the output image file. Defaults to "model".
    """
    model = Model(model_filename)
    image = frame_buffer()

    for face_index in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(face_index)
        for i in range(3):
            v0 = model.get_vertex(face[i])
            v1 = model.get_vertex(face[(i + 1) % 3])
            x0 = int((v0.x + 1.0) * WIDTH / 2.0)
            y0 = int((v0.y + 1.0) * HEIGHT / 2.0)
            x1 = int((v1.x + 1.0) * WIDTH / 2.0)
            y1 = int((v1.y + 1.0) * HEIGHT / 2.0)
            for x, y in [(x0, y0), (x1, y1)]:
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:  # Corrected indices here
                    image[y][x] = color

    file_writer(image, output_filename)


def render_lines(lines: list[Line], filename="lines") -> None:
    """
    Renders a list of lines on an image and writes the result to a file.

    Args:
        lines (List[Line]): A list of Line objects defining the lines to be rendered.
        filename (str, optional): The name of the output file. Defaults to "untitled".
    """
    image = frame_buffer()
    for line in lines:
        steep = line.swap_if_steep()
        for x in range(int(line.x0), int(line.x1) + 1):
            y = line.get_y_value(x)
            if steep:
                image[x][y] = line.color
            else:
                image[y][x] = line.color

    file_writer(image, filename)


def file_writer(image, filename="untitled", debug=False) -> None:
    """Writes the image bytes to a file.

    Args:
        image (list): Image buffer to write.
        filename (str, optional): Name to be given to the exported file. Defaults to "untitled".
    """
    with open(f"./{filename}.ppm", "wb") as file:
        file.write(f"P6\n{WIDTH} {HEIGHT}\n255\n".encode())
        for row in reversed(image):
            for pixel in row:
                file.write(bytes(pixel))
