"""Test module for the app entry points
"""
from os import listdir, remove, getcwd

from app import main

cwd = getcwd()


def test_main():
    """Testing main"""
    assert main("tests/output/test_main") == {
        "message": "Successful: Created Line Scene and exported Successfully",
        "error": "",
    }
    assert "test_main.ppm" in listdir(cwd + "/tests/output")
    remove(cwd + "/tests/output/test_main.ppm")
