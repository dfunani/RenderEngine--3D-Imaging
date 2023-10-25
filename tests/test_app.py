from app import main
from models.interfaces.responses import Response
from os import listdir, remove

def test_app():
    assert main() == Response.success
    assert "untitled_gradient.ppm" in listdir()
    assert "untitled_spheres.ppm" in listdir()
    remove("untitled_gradient.ppm")
    remove("untitled_spheres.ppm")
    