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
from numpy import array, fliplr, flipud
from models.types.exceptions import ObjectImageError


class ObjectImage:
    """
    ObjectImage class for reading and writing Object image files and performing
    image operations.
    """

    def __init__(self) -> None:
        """
        Initialize ObjectImage object.
        """
        self.image = None

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
                self.image = Image.fromarray(data)
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
            self.image.save(filename)
            return True
        except (TypeError, ValueError, FileNotFoundError, UnidentifiedImageError) as e:
            raise ObjectImageError(str(e)) from e

    def flip_horizontally(self) -> bool:
        """
        Flip the image horizontally.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.image:
            self.image = Image.fromarray(fliplr(array(self.image)))
            return True
        return False

    def flip_vertically(self) -> bool:
        """
        Flip the image vertically.

        Returns:
        - bool: True if successful, False if no image loaded.
        """
        if self.image:
            self.image = Image.fromarray(flipud(array(self.image)))
            return True
        return False
