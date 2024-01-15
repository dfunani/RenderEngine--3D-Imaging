# test_renders.py

"""
Module Summary: Contains tests for rendering functions and utilities.

Returns:
    Tests:
        test_render_only: Test for rendering a single line and verifying the 
        output file.
        test_render_only_error_offscreen: Test for raising an IndexError when 
        rendering a line off-screen.
        test_writer: Test for writing an image buffer to a file and verifying 
        the output file.
"""

from os import listdir, remove, getcwd
from pytest import raises
from models.primitives import Line
from engines.renders import render_triangle_outline, file_writer
from utils.generators import frame_buffer
cwd = getcwd()

def test_render_only():
    """
    Test for rendering a single line and verifying the output file.
    """
    line = Line((0, 0), (-800, -599), (255, 0, 0))
    render_triangle_outline([line], "tests/output/test_render")
    assert "test_render.ppm" in listdir("tests/output/")
    remove("tests/output/test_render.ppm")


def test_render_only_error_offscreen():
    """
    Test for raising an IndexError when rendering a line off-screen.
    """
    line = Line((0, 0), (1000, 1000), (255, 0, 0))
    with raises(IndexError):
        render_triangle_outline([line])


def test_writer():
    """
    Test for writing an image buffer to a file and verifying the output file.
    """
    image = frame_buffer()
    file_writer(image, "tests/output/test_writer")
    assert "test_writer.ppm" in listdir("tests/output/")
    remove("tests/output/test_writer.ppm")
