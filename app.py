from displays.drawers import Drawer
from models.interfaces.responses import Response

def main() -> Response:
    result: list = []
    result.append(Drawer.drawSpheres())
    result.append(Drawer.drawColorGradient())
    if all(r == Response.success or r == Response.warning for r in result):
        return Response.success
    else:
        return Response.error

if __name__ == "__main__":
    main()
