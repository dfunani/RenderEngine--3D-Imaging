"""Test module for the app entry points
"""
from os import listdir, remove, getcwd

from app import render_scene

cwd = getcwd()

def test_main():
    """Testing main"""
    assert render_scene("tests/output/test_main") == {
        "message": "Successful: Created Line Scene and exported Successfully",
        "error": "",
    }
    assert "test_main.ppm" in listdir("tests/output")
    remove("tests/output/test_main.ppm")
