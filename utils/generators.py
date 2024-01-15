# generators.py

"""
Module Summary: Contains functions for generating image-related data.

Returns:
    Functions:
        frame_buffer: Generates a frame buffer for image initialization.

"""

from models.vectors import RGB


WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image


def frame_buffer(width: int = WIDTH, height: int = HEIGHT):
    """
    Generates a frame buffer for image initialization.

    Args:
        width (int, optional): The width of the image. Defaults to 800.
        height (int, optional): The height of the image. Defaults to 600.

    Returns:
        List[List[List[int]]]: A frame buffer representing the image with initial white color.
    """
    
    return [[RGB(0, 0, 0) for _ in range(width)] for _ in range(height)]
