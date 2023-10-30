import sys
from displays.drawers import Drawer
from models.interfaces.responses import Response
from logging import error, warning, info, INFO


def main() -> Response:
    result: list = []
    result.append(Drawer.drawSpheres())
    result.append(Drawer.drawColorGradient())
    result.append(Drawer.drawLightEmission())
    if all(r == Response.success or r == Response.warning for r in result):
        return Response.success
    else:
        return Response.error


if __name__ == "__main__":
    from logging import basicConfig

    basicConfig(
        filename="app.log",
        filemode="a",
        format="%(name)s - %(levelname)s - %(message)s",
        level=INFO,
    )
    info("======================== Render Engine Started =============================")
    if main() != Response.error:
        info("Render Engine Stopped")
    else:
        error("Render Engine Stopped - Errors Encountered")
    info("============================================================================")
