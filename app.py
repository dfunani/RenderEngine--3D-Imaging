"""
Module Summary: This module renders a line and writes its information to a file.
"""

from models.images import ObjectImage
from models.types.exceptions import ObjectImageError


if __name__ == "__main__":
    # Example usage:
    image = ObjectImage()
    try:
        if image.read_file("obj/african_head.obj"):
            image.flip_vertically()
            image.write_file("output.tga")
    except ObjectImageError as e:
        print(e)
