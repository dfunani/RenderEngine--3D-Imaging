"""
Module Summary: This module renders a line and writes its information to a file.
"""

from engines.renders import render_lines, render_model, render_triangle_outline
from models.primitives import Line, Triangle
from models.types.exceptions import ArgumentError
from models.vectors import RGB, Vector2

def render_scene(filename="output/main") -> None:
    """
    Renders a line and writes its information to a file.

    Example:
    --------
    line = Line(10, 20, 100, 150, (255, 0, 0))  # Define the line
    render_line(line, 200, 200, "output.txt")  # Render the line to "output.txt"
    """
    lines = []
    try:
        lines.append(Line(Vector2(13, 20), Vector2(80, 40), RGB(0, 255, 0)))
        lines.append(Line(Vector2(20, 13), Vector2(40, 80), RGB(255, 0, 0)))
        lines.append(Line(Vector2(80, 40), Vector2(13, 20), RGB(125, 75, 25)))
        lines.append(Line(Vector2(10, 20), Vector2(100, 150), RGB(0, 0, 255)))
    except (ArgumentError, ValueError, TypeError) as error:
        raise RuntimeError(f"Couldn't create Line(s). Error: {error}")

    triangles = []
    try:
        triangle1 = Triangle([Vector2(10, 70), Vector2(50, 160), Vector2(70, 80)], RGB(0, 0, 255))
        triangle2 = Triangle([Vector2(180, 50), Vector2(150, 1), Vector2(70, 180)], RGB(255, 0, 0))
        triangle3 = Triangle([Vector2(180, 150), Vector2(120, 160), Vector2(130, 180)], RGB(0, 255, 0))
        triangle4 = Triangle([Vector2(10, 10), Vector2(100, 30), Vector2(190, 160)], RGB(255, 0, 0))
        triangles.extend([triangle1, triangle2, triangle3, triangle4])
    except (ArgumentError, ValueError, TypeError) as error:
        raise RuntimeError(f"Couldn't create Triangle(s). Error: {error}")

    try:
        render_lines(lines, f"{filename}_lines")
        render_model("obj/african_head.obj", f"{filename}_model")
        render_triangle_outline(triangles, f"{filename}_triangle_outline")
    except (ArgumentError, ValueError, TypeError) as error:
        raise RuntimeError(f"Couldn't render scene. Error: {error}")

    print("Successful: Created Line Scene and exported Successfully")

if __name__ == "__main__":
    render_scene()

