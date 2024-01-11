"""
Module Summary: Contains tests for vector-related classes.

Returns:
    Tests:
        test_vector_init: Test for the initialization of the Vector class.
        test_vector_error: Test for raising an error when an invalid 
        argument is provided to Vector.
        test_vector2_init: Test for the initialization of the Vector2 class.
        test_vector2_error: Test for raising an error when an invalid 
        argument is provided to Vector2.
        test_vector3_init: Test for the initialization of the Vector3 class.
        test_vector3_error: Test for raising an error when an invalid 
        argument is provided to Vector3.
        test_rgb_init: Test for the initialization of the RGB class.
        test_rgb_error: Test for raising an error when an invalid 
        argument is provided to RGB.
"""

from pytest import raises
from models.vectors import Vector, Vector2, Vector3, RGB


def test_vector_init():
    """Test for the initialization of the Vector class."""
    v = Vector(1)
    assert v.coordinates[0] == 1


def test_vector_error():
    """Test for raising an error when an invalid argument is provided to Vector."""
    with raises(TypeError):
        Vector("1")


def test_vector2_init():
    """Test for the initialization of the Vector2 class."""
    v = Vector2(1, 1)
    assert v.coordinates[0] == v.coordinates[1] == 1


def test_vector2_error():
    """Test for raising an error when an invalid argument is provided to Vector2."""
    with raises(TypeError):
        Vector2("1", 1)


def test_vector3_init():
    """Test for the initialization of the Vector3 class."""
    v = Vector3(1, 1, 1)
    assert v.coordinates[0] == v.coordinates[1] == v.coordinates[2] == 1


def test_vector3_error():
    """Test for raising an error when an invalid argument is provided to Vector3."""
    with raises(TypeError):
        Vector3("1", 1, 1)


def test_rgb_init():
    """Test for the initialization of the RGB class."""
    v = RGB(1, 1, 1)
    assert v.coordinates[0] == v.coordinates[1] == v.coordinates[2] == 1


def test_rgb_error():
    """Test for raising an error when an invalid argument is provided to RGB."""
    with raises(TypeError):
        RGB("1", 1, 1)
