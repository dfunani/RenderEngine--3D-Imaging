from app import main
from models.interfaces.responses import Response
from os import listdir, remove, getcwd


def test_app():
    assert main() == Response.success
    assert "untitled_gradient.ppm" in listdir(getcwd() + "/output/")
    assert "untitled_spheres.ppm" in listdir(getcwd() + "/output/")
    assert "untiled_light_image.ppm" in listdir(getcwd() + "/output/")
    remove(getcwd() + "/output/" + "untitled_gradient.ppm")
    remove(getcwd() + "/output/" + "untitled_spheres.ppm")
    remove(getcwd() + "/output/" + "untiled_light_image.ppm")
