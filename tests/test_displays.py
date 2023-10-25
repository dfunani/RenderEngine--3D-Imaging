from displays.drawers import Drawer
from os import listdir, remove

from models.interfaces.responses import Response

def test_drawer_sphere():
    assert Drawer.drawSpheres(spheres=3, filename="test_displays_spheres", extension="ppm") == Response.success
    assert "test_displays_spheres.ppm" in listdir()
    remove("test_displays_spheres.ppm")

def test_drawer_gradient():
    assert Drawer.drawColorGradient(filename="test_displays_gradient", extension="ppm") == Response.success
    assert "test_displays_gradient.ppm" in listdir()
    remove("test_displays_gradient.ppm")
