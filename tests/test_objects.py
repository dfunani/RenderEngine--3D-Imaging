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
    """test_line_class"""
    line = Line((x0, y0), (x1, y1), color)
    assert line.x0 == 0
    assert line.x1 == 1
    assert line.y0 == 2
    assert line.y1 == 3


def test_line_init_error():
    """test line init when error raised - Passed str not tuple"""
    with raises(TypeError):
        Line("(x0, y0)", (x1, y1), color)


def test_line_init_error1():
    """test line init when error raised - passed tuple with
    a str element
    """
    with raises(ValueError):
        Line(
            (x0, y0),
            (x1, y1),
            (
                20,
                "",
                "color",
            ),
        )


def test_str():
    """test str rep of the line class"""
    line = Line((x0, y0), (x1, y1), color)
    assert str(line) == "Line from (0, 2) to (1, 3) with color (255, 0, 0)"


def test_swap_if_steep():
    """test steep check func"""
    line = Line((x0, y0), (x1, y1), color)
    assert not line.swap_if_steep()


def test_get_y_value():
    """test getting y value"""
    line = Line((x0, y0), (x1, y1), color)
    y = line.get_y_value(line.x0)
    assert y == 2
