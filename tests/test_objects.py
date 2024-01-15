"""Test module for objects
    """
from pytest import raises
from models.vectors import RGB

from models.primitives import Line


def test_line_init():
    """test_line_class"""
    line = Line((1, 1), (1, 1), RGB())
    assert line.x0 == 0
    assert line.x1 == 1
    assert line.y0 == 2
    assert line.y1 == 3


def test_line_init_error():
    """test line init when error raised - Passed str not tuple"""
    with raises(TypeError):
        Line("(x0, y0)", (1, 1), RGB())


def test_line_init_error1():
    """test line init when error raised - passed tuple with
    a str element
    """
    with raises(ValueError):
        Line(
            (1, 1),
            (1, 1),
            (
                20,
                "",
                "color",
            ),
        )


def test_str():
    """test str rep of the line class"""
    line = Line((1, 1), (1, 1), RGB())
    assert str(line) == "Line from (0, 2) to (1, 3) with color (255, 0, 0)"


def test_swap_if_steep():
    """test steep check func"""
    line = Line((1, 1), (1, 1), RGB())
    assert not line.swap_if_steep()


def test_get_y_value():
    """test getting y value"""
    line = Line((1, 1), (1, 1), RGB())
    y = line.get_y_value(line.x0)
    assert y == 2
