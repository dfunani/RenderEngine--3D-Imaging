"""
Module Summary: This module renders a line and writes its information to a file.
"""

from engines.renders import render_line
from models.objetcs import Line
from models.types.exceptions import ArgumentError


def main(filename="output/main") -> None:
    """
    Renders a line and writes its information to a file.

    Example:
    --------
    line = Line(10, 20, 100, 150, (255, 0, 0))  # Define the line
    render_line(line, 200, 200, "output.txt")  # Render the line to "output.txt"
    """
    lines = []
    try:
        lines.append(Line((13, 20), (80, 40), (0, 255, 0)))
        lines.append(Line((20, 13), (40, 80), (255, 0, 0)))
        lines.append(Line((80, 40), (13, 20), (125, 75, 25)))
        lines.append(Line((10, 20), (100, 150), (0, 0, 255)))
    except (ArgumentError, ValueError, TypeError) as error:
        return {"message": "Couldn't Create Line(s)", "error": str(error)}

    try:
        render_line(lines, filename)
    except (ArgumentError, ValueError, TypeError) as error:
        return {"message": "Couldn't Render Line Scene", "error": str(error)}

    return {"message": "Successful: Created Line Scene and exported Successfully", "error": ""}


if __name__ == "__main__":
    main()
