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


from models.objetcs import Line  # Import the Line class from your objects module
from utils.generators import frame_buffer

WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image


def render_line(lines: list[Line], filename="untitled") -> None:
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
        for row in reversed(image[::-1]):
            for pixel in row:
                file.write(bytes(pixel))
