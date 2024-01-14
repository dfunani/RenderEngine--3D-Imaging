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
from models.primitives import Line, Triangle
from models.vectors import (
    RGB,
    Vector2,
)  # Import the Line class from your objects module
from utils.generators import frame_buffer

WIDTH = 800  # Width of the image
HEIGHT = 600  # Height of the image

def render_2Dtriangles(triangles: list[Triangle], filename="triangle"):
    """
    Adds a Triangle object to the list of triangles to render.

    Args:
        triangle (Triangle): Triangle object to add.

    Renders all triangles to a PPM file.

    Args:
        filename (str): Name of the output PPM file.
    """
    image = frame_buffer()

    for triangle in triangles:
        for y in range(int(triangle.vertices[0].y), int(triangle.vertices[2].y) + 1):
            for x in range(int(triangle.vertices[0].x), int(triangle.vertices[2].x) + 1):
                P = Vector2(x, y)
                bc_screen = triangle.barycentric(P)

                if 0 <= bc_screen.x <= 1 and 0 <= bc_screen.y <= 1 and 0 <= bc_screen.z <= 1:
                    color = (
                       int( bc_screen.x * triangle.color[0] +
                        bc_screen.y * triangle.color[0] +
                        bc_screen.z * triangle.color[0]),
                        int(bc_screen.x * triangle.color[1] +
                        bc_screen.y * triangle.color[1] +
                        bc_screen.z * triangle.color[1]),
                        int(bc_screen.x * triangle.color[2] +
                        bc_screen.y * triangle.color[2] +
                        bc_screen.z * triangle.color[2]),
                    )
                    image[y][x] = color
        

    file_writer(image, filename, debug=True)
    # image = frame_buffer()
    # for triangle in triangles:
    #     bboxmin = Vector2(WIDTH - 1, HEIGHT - 1)
    #     bboxmax = Vector2(0, 0)
    #     clamp = Vector2(WIDTH - 1, HEIGHT - 1)

    #     # Update bounding box
    #     for vertex in triangle.vertices:
    #         bboxmin.x = max(0, min(bboxmin.x, vertex.x))
    #         bboxmin.y = max(0, min(bboxmin.y, vertex.y))
    #         bboxmax.x = min(clamp.x, max(bboxmax.x, vertex.x))
    #         bboxmax.y = min(clamp.y, max(bboxmax.y, vertex.y))

    #     # Iterate over pixels inside bounding box
    #     for x in range(int(bboxmin.x), int(bboxmax.x) + 1):
    #         for y in range(int(bboxmin.y), int(bboxmax.y) + 1):
    #             P = Vector2(x, y)
    #             bc_screen = triangle.barycentric(P)

    #             # Check if the point is inside the triangle using barycentric coordinates
    #             if (
    #                 0 <= bc_screen.x <= 1
    #                 and 0 <= bc_screen.y <= 1
    #                 and 0 <= bc_screen.z <= 1
    #             ):
    #                 image[int(P.x)][int(P.y)] = triangle.color

    # file_writer(image, filename, debug=True)

def render_triangle_outline(triangles: list[Triangle], filename="triangle_outline"):
    # Render lines
    image = frame_buffer()
    # Draw vertices
    for triangle in triangles:
        lines = triangle.draw_vertices([])
        for line in lines:
            steep = line.swap_if_steep()
            for x in range(int(line.x0), int(line.x1) + 1):
                y = line.get_y_value(x)
                if steep:
                    image[x][y] = line.color
                else:
                    image[y][x] = line.color
    file_writer(image, filename)

def render_model(
    model_filename: str, output_filename: str = "model", color=RGB(0, 0, 0)
) -> None:
    """
    Renders a 3D model to an image file.

    Args:
        model_filename (str): The filename of the 3D model in OBJ format.
        output_filename (str, optional): The name of the output image file. Defaults to "model".
    """
    model = Model(model_filename)
    image = frame_buffer()

    for face_index in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(face_index)
        for i in range(3):
            v0 = model.get_vertex(face[i])
            v1 = model.get_vertex(face[(i + 1) % 3])
            x0 = int((v0.x + 1.0) * WIDTH / 2.0)
            y0 = int((v0.y + 1.0) * HEIGHT / 2.0)
            x1 = int((v1.x + 1.0) * WIDTH / 2.0)
            y1 = int((v1.y + 1.0) * HEIGHT / 2.0)
            for x, y in [(x0, y0), (x1, y1)]:
                if 0 <= x < WIDTH and 0 <= y < HEIGHT:  # Corrected indices here
                    image[y][x] = color

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


def file_writer(image, filename="untitled", debug=False) -> None:
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
