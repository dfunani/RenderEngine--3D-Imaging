"""
Module Summary:
    Contains functions for rendering lines and shaded triangles on images.

Description:
    This module provides functions for rendering lines and shaded triangles on 
    images using various algorithms.
    It includes functions for rendering shaded triangles with barycentric 
    interpolation,
    rendering outlines of triangles by connecting their vertices with lines, 
    and rendering 3D models with shading
    using the Phong shading model.

Functions:
    render_triangle_shaded: Renders shaded triangles using barycentric interpolation.
    render_triangle_outline: Renders outlines of triangles by connecting their 
    vertices with lines.
    render_model_shaded: Renders a 3D model with shading using the Phong shading model.
    file_writer: Writes the image or line to a file.

Returns:
    Functions:
        render_triangle_shaded: Renders shaded triangles on an image.
        render_triangle_outline: Renders outlines of triangles on an image.
        render_model_shaded: Renders a 3D model with shading on an image.
        file_writer: Writes the line or image to a file.
"""


from models.objects import Model
from models.primitives import Triangle
from models.vectors import RGB  # Import the Line class from your objects module
from utils.generators import HEIGHT, WIDTH, frame_buffer


def render_triangle_shaded(
    triangles: list[Triangle], filename: str = "triangle"
) -> None:
    """
    Renders shaded triangles using barycentric interpolation.

    Args:
        triangles (list[Triangle]): List of Triangle objects to render.
        filename (str, optional): Name of the output PPM file. Defaults to "triangle".
    """
    # Create an empty image buffer
    image = frame_buffer()

    # Barycentric interpolation for shading
    for triangle in triangles:
        image = triangle.draw_triangle(image)

    # Save the image to a file
    file_writer(image, filename)


def render_triangle_outline(
    triangles: list[Triangle], filename: str = "triangle_outline"
) -> None:
    """
    Renders outlines of triangles by connecting their vertices with lines.

    Args:
        triangles (list[Triangle]): List of Triangle objects to render.
        filename (str, optional): Name of the output PPM file. Defaults to "triangle_outline".
    """
    # Create an empty image buffer
    image = frame_buffer()

    # Iterate through each triangle
    for triangle in triangles:
        # Get the lines representing the vertices of the triangle
        vertex_lines = triangle.draw_vertices([])

        # Draw each line on the image
        for line in vertex_lines:
            image = line.draw_line(image)

    # Save the image to a file
    file_writer(image, filename)


def render_model_shaded(
    model_filename: str, output_filename: str = "model_shaded", color=RGB(0, 0, 255)
) -> None:
    """
    Renders a 3D model with shading using the Phong shading model.

    Args:
        model_filename (str): The filename of the 3D model in OBJ format.
        output_filename (str, optional): The name of the output image file.
        Defaults to "model_shaded".
        color (RGB, optional): The color of the shaded model. Defaults to RGB(0, 0, 255).
    """
    model = Model(model_filename)
    image = frame_buffer()

    image = model.draw_model(image, color)

    # Save the image to a file
    file_writer(image, output_filename)


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
