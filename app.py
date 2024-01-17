"""
Module Summary: This module renders a line and writes its information to a file.
"""

from models.objects import ObjectCamera, ObjectModel, ObjectImage


if __name__ == "__main__":
    # Example usage:
    model = ObjectModel("obj/african_head.obj")
    camera = ObjectCamera()
    image = ObjectImage(800, 600)
    image.render_model(model, camera)
    # image = ObjectImage()
    # try:
    #     if image.read_file("obj/african_head.obj"):
    #         image.flip_vertically()
    #         image.write_file("output.tga")
    # except ObjectImageError as e:
    #     print(e)
