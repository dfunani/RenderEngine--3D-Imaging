"""Test module for objects
    """
from pytest import raises

from models.objetcs import Line

x0 = 0
x1 = 1
y0 = 2
y1 = 3
color = (255, 0, 0)


def test_line_init():
    color = (255, 0, 0)
    line = Line((x0, y0), (x1, y1), color)
    assert line.x0 == 0
    assert line.x1 == 1
    assert line.y0 == 2
    assert line.y1 == 3


def test_line_init_error():
    with raises(TypeError):
        line = Line("(x0, y0)", (x1, y1), color)

def test_line_init_error1():
    with raises(ValueError):
        line = Line((x0, y0), (x1, y1), (20,"","color",))

def test_str():
    line = Line((x0, y0), (x1, y1), color)
    assert str(line) == "Line from (0, 2) to (1, 3) with color (255, 0, 0)"

def test_swap_if_steep():
    line = Line((x0, y0), (x1, y1), color)
    assert not line.swap_if_steep()

def test_get_y_value():
    line = Line((x0, y0), (x1, y1), color)
    y = line.get_y_value(line.x0)
    assert y == 2