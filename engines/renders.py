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

from models.objects import Model
from models.primitives import Line  # Import the Line class from your objects module
from utils.generators import frame_buffer

WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image


def render_model(model_filename: str, output_filename: str = "model") -> None:
    model = Model(model_filename)
    white = (255, 0, 0)
    image = frame_buffer()

    for face_index in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(face_index)
        for i in range(3):
            v0 = model.get_vertex(face[i])
            v1 = model.get_vertex(face[(i + 1) % 3])
            x0 = int((v0[0] + 1.0) * WIDTH / 2.0)
            y0 = int((v0[1] + 1.0) * HEIGHT / 2.0)
            x1 = int((v1[0] + 1.0) * WIDTH / 2.0)
            y1 = int((v1[1] + 1.0) * HEIGHT / 2.0)
            for x, y in [(x0, y0), (x1, y1)]:
                if 0 <= x0 < WIDTH and 0 <= y0 < HEIGHT:
                    image[y0][x0] = white

                if 0 <= x1 < WIDTH and 0 <= y1 < HEIGHT:
                    image[y1][x1] = white

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


def file_writer(image, filename="untitled") -> None:
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
