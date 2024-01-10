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
    line = Line((10, 20), (100, 150), (255, 0, 0))
    render_line(line, "output")


if __name__ == "__main__":
    main()
