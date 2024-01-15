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


from random import randint
from models.matrices import Matrix
from models.objects import Model
from models.primitives import Line, Triangle
from models.vectors import (
    RGB,
    Vector2,
    Vector3,
)  # Import the Line class from your objects module
from utils.generators import HEIGHT, WIDTH, frame_buffer


def m2v(m):
    return Vector3(m[0][0] / m[3][0], m[1][0] / m[3][0], m[2][0] / m[3][0])


def v2m(v):
    m = Matrix(4, 1)
    m[0][0] = v.x
    m[1][0] = v.y
    m[2][0] = v.z
    m[3][0] = 1.0
    return m


def viewport(x, y, w, h, depth=255):
    m = Matrix.identity(4)
    m[0][3] = x + w / 2.0
    m[1][3] = y + h / 2.0
    m[2][3] = depth / 2.0

    m[0][0] = w / 2.0
    m[1][1] = h / 2.0
    m[2][2] = depth / 2.0
    return m


def translation(v):
    Tr = Matrix.identity(4)
    Tr[0][3] = v.x
    Tr[1][3] = v.y
    Tr[2][3] = v.z
    return Tr


def zoom(factor):
    Z = Matrix.identity(4)
    Z[0][0] = Z[1][1] = Z[2][2] = factor
    return Z


def rotation_x(cosangle, sinangle):
    R = Matrix.identity(4)
    R[1][1] = R[2][2] = cosangle
    R[1][2] = -sinangle
    R[2][1] = sinangle
    return R


def rotation_y(cosangle, sinangle):
    R = Matrix.identity(4)
    R[0][0] = R[2][2] = cosangle
    R[0][2] = sinangle
    R[2][0] = -sinangle
    return R


def rotation_z(cosangle, sinangle):
    R = Matrix.identity(4)
    R[0][0] = R[1][1] = cosangle
    R[0][1] = -sinangle
    R[1][0] = sinangle
    return R


def render_line_matrix(
    model_filename="obj/cube.obj", output_filename: str = "triangle"
):
    model = Model(model_filename)

    image = frame_buffer()
    VP = viewport(WIDTH / 4, WIDTH / 4, WIDTH / 2, HEIGHT / 2)

    x = Vector3(1.0, 0.0, 0.0)
    y = Vector3(0.0, 1.0, 0.0)
    o = Vector3(0.0, 0.0, 0.0)
    o = m2v(VP * v2m(o))
    x = m2v(VP * v2m(x))
    y = m2v(VP * v2m(y))

    line1 = Line(o, x, RGB(255, 0,   0))
    line2 = Line(o, y, RGB(0,   255, 0))
    image = line1.draw_line_matrix(image)
    image = line2.draw_line_matrix(image)

    for i in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(i)
        for j in range(3):  # Vertices of a face are 0-indexed
            wp0 = model.get_vertex(face[j])
            wp1 = model.get_vertex(face[(j + 1) % 3])  # Use % 3 to wrap around

            sp0 = m2v(VP * v2m(wp0))
            sp1 = m2v(VP * v2m(wp1))
            line4 = Line(sp0, sp1, RGB(255, 255, 255))
            line4.draw_line_matrix(image)
            T = zoom(1.5)
            sp0 = m2v(VP * T * v2m(wp0))
            sp1 = m2v(VP * T * v2m(wp1))
            line3 = Line(sp0, sp1, RGB(255, 255, 0))
            image = line3.draw_line_matrix(image)
    file_writer(image, output_filename)


def render_sideview_triangles(
    triangles: list[Triangle] = None, filename: str = "triangle"
):
    image = frame_buffer()
    lines = []
    # scene "2d mesh"
    l1 = Line(Vector2(20, 34), Vector2(744, 400), RGB(255, 0, 0))
    l2 = Line(Vector2(120, 434), Vector2(444, 400), RGB(0, 255, 0))
    l3 = Line(Vector2(330, 463), Vector2(594, 200), RGB(0, 0, 255))

    # screen Line
    l4 = Line(Vector2(10, 10), Vector2(790, 10), RGB(255, 255, 255))
    lines.extend([l1, l2, l3, l4])
    for line in lines:
        image = line.draw_line(image)
    file_writer(image, filename)


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


def render_model_barycentric(model_filename, output_filename="output_model"):
    model = Model(model_filename)
    zbuffer = [-float("inf") for _ in range(WIDTH * HEIGHT)]

    image = frame_buffer()

    for face_index in range(1, len(model.faces) + 1):  # Faces are 1-indexed
        face = model.get_face(face_index)
        pts = [model.world2screen(model.get_vertex(face[i])) for i in range(3)]
        image = model.draw_model_barycentric(pts, zbuffer, image, RGB(255, 255, 255))

    file_writer(image, output_filename, debug=False)


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
                if debug:
                    print(pixel)
                file.write(bytes(pixel))
