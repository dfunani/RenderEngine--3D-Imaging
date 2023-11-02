from displays.drawers import Drawer
from os import getcwd, listdir, remove

from models.interfaces.responses import Response


def test_drawer_sphere():
    assert (
        Drawer.drawSpheres(spheres=3, filename="test_displays_spheres", extension="ppm")
        == Response.success
    )
    assert "test_displays_spheres.ppm" in listdir(getcwd() + "/output/")
    remove(getcwd() + "/output/" + "test_displays_spheres.ppm")


def test_drawer_gradient():
    assert (
        Drawer.drawColorGradient(filename="test_displays_gradient", extension="ppm")
        == Response.success
    )
    assert "test_displays_gradient.ppm" in listdir(getcwd() + "/output/")
    remove(getcwd() + "/output/" + "test_displays_gradient.ppm")


def test_drawer_light_image():
    assert (
        Drawer.drawColorGradient(filename="test_displays_light", extension="ppm")
        == Response.success
    )
    assert "test_displays_light.ppm" in listdir(getcwd() + "/output/")
    remove(getcwd() + "/output/" + "test_displays_light.ppm")
