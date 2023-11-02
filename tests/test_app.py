from app import main
from models.interfaces.responses import Response
from os import listdir, remove


def test_app():
    assert main() == Response.success
    assert "untitled_gradient.ppm" in listdir("./output/")
    assert "untitled_spheres.ppm" in listdir("./output/")
    assert "untiled_light_image.ppm" in listdir("./output/")
    remove("./output/untitled_gradient.ppm")
    remove("./output/untitled_spheres.ppm")
    remove("./output/untiled_light_image.ppm")
