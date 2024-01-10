"""
Module Summary: Contains functions for rendering lines on images.

This module provides functions for rendering lines on images using various algorithms.

Functions:
    render_line: Renders a line on an image given its dimensions and output file.

Returns:
    Functions:
        render_line: Renders a line on an image.
"""


from models.objetcs import Line  # Import the Line class from your objects module
from utils.generators import frame_buffer

WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image

def render_line(line: Line, filename="untitled") -> None:
    """
    Renders the scene described by the line and saves the image to a specified filename.

    Args:
        line (Line): A Line object defining the line to be rendered.
        filename (str, optional): The name of the output file. Defaults to "untitled".
    """
    image = frame_buffer()

    # Calculate differences between start and end points
    dx, dy = line.interpolate()

    # Determine the direction of the line
    x_increment, y_increment = line.change_direction()

    error = dx - dy  # Determine initial error

    x0 = int(line.x0)
    y0 = int(line.y0)
    x1 = int(line.x1)
    y1 = int(line.y1)

    while x0 != x1 or y0 != y1:
        # Color the current pixel as part of the line
        image[y0][x0] = line.color

        # Calculate error for next pixel
        error_2 = 2 * error

        if error_2 > -dy:
            error -= dy
            x0 += x_increment

        if error_2 < dx:
            error += dx
            y0 += y_increment

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
