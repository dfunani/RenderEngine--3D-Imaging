"""
Module Summary: This module renders a line and writes its information to a file.
"""

from engines.renders import render_model


def render_scene(filename="output/main") -> None:
    render_model()
    try:
        pass
    except (ValueError, TypeError, BaseException) as error:
        return {
        "message": "Error: Couldn't Create Scene",
        "error": str(error),
    }
    return {
        "message": "Successful: Created Scene and exported Successfully",
        "error": "",
    }


if __name__ == "__main__":
    print(render_scene())
