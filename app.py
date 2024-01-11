"""
Module Summary: This module renders a line and writes its information to a file.
"""

from engines.renders import render_line
from models.objetcs import Line


def main() -> None:
    """
    Renders a line and writes its information to a file.

    Example:
    --------
    line = Line(10, 20, 100, 150, (255, 0, 0))  # Define the line
    render_line(line, 200, 200, "output.txt")  # Render the line to "output.txt"
    """
    lines = []
    lines.append(Line((13, 20), (80, 40), (0, 255, 0)))
    lines.append(Line((20, 13), (40, 80), (255, 0, 0)))
    lines.append(Line((80, 40), (13, 20), (125, 75, 25)))
    lines.append(Line((10, 20), (100, 150), (0, 0, 255)))
    render_line(lines, "output")


if __name__ == "__main__":
    main()
