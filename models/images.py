"""
imaging Module

This module provides the ObjectImage class for reading, writing, and 
performing operations on Object image files.

Classes:
- ObjectImage: Class for reading and writing Object image files and performing 
image operations.

Usage:
from images import ObjectImage

# Create a ObjectImage object
image = ObjectImage()

# Read a Object image file
image.read_file("input.ext")

# Perform operations (e.g., flip horizontally)
image.flip_horizontally()

# Write the modified image to a new Object image file
image.write_file("output.ext")
"""

from PIL import Image, UnidentifiedImageError
from numpy import array, fliplr, flipud, zeros, uint8
from models.types.exceptions import ObjectImageError

class ObjectColor:
    def __init__(self, r=0, g=0, b=0, a=255):
        self.r = r
        self.g = g
        self.b = b
        self.a = a

class ObjectImage:
    """
    ObjectImage class for reading and writing Object image files and performing
    image operations.
    """

    def __init__(self, width, height, color_format=ObjectColor) -> None:
        """
        Initialize ObjectImage object.
        """
        self.width = width
        self.height = height
        self.color_format = color_format
        self.pixels = zeros((width, height, 4), dtype=uint8)

    def set(self, x, y, color):
        self.pixels[x, y] = [color.r, color.g, color.b, color.a]

    def get(self, x, y):
        return self.pixels[x, y]

    def read_file(self, filename: str) -> bool:
        """
        Read a Object image file and store it as a PIL Image.

        Parameters:
        - filename (str): The path to the Object image file.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            with Image.open(filename) as img:
                data = array(img)
                self.pixels = Image.fromarray(data)
            return True
        except (TypeError, ValueError, FileNotFoundError, UnidentifiedImageError) as e:
            raise ObjectImageError(str(e)) from e

    def write_file(self, filename: str) -> bool:
        """
        Write the current image to a Object image file.

        Parameters:
        - filename (str): The path to save the Object image file.

        Returns:
        - bool: True if successful, False otherwise.
        """
        try:
            self.pixels.save(filename)
            return True
        except (TypeError, ValueError, FileNotFoundError, UnidentifiedImageError) as e:
            raise ObjectImageError(str(e)) from e

    def flip_horizontally(self) -> bool:
        """
        Flip the image horizontally.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.pixels:
            self.pixels = Image.fromarray(fliplr(array(self.pixels)))
            return True
        return False

    def flip_vertically(self) -> bool:
        """
        Flip the image vertically.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.pixels:
            self.pixels = Image.fromarray(flipud(array(self.pixels)))
            return True
        return False
