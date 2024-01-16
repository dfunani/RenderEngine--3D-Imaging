"""
Module Summary: This module renders a line and writes its information to a file.
"""

from models.images import ObjectImage
from models.objects import Model
from models.types.exceptions import ObjectImageError


if __name__ == "__main__":
    # Example usage:
    model = Model("obj/african_head.obj")
    # image = ObjectImage()
    # try:
    #     if image.read_file("obj/african_head.obj"):
    #         image.flip_vertically()
    #         image.write_file("output.tga")
    # except ObjectImageError as e:
    #     print(e)
