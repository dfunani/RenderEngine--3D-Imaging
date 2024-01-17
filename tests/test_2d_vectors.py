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
from models.geometry.vectors_2d import Vector2


def init_vector2(v1_x=1, v1_y=2, v2_x=3, v2_y=4) -> tuple[Vector2, Vector2]:
    """
    Initialize two Vector2 instances for testing.

    Parameters:
    - v1_x (int, optional): The x-coordinate of the first vector. Defaults to 1.
    - v1_y (int, optional): The y-coordinate of the first vector. Defaults to 2.
    - v2_x (int, optional): The x-coordinate of the second vector. Defaults to 3.
    - v2_y (int, optional): The y-coordinate of the second vector. Defaults to 4.

    Returns:
    tuple[Vector2, Vector2]: A tuple containing two initialized Vector2 instances.
    """
    v1 = Vector2(v1_x, v1_y)
    v2 = Vector2(v2_x, v2_y)
    return v1, v2


def test_2d_vector():
    """
    Test for basic initialization of Vector2 instances.
    """
    v1, v2 = init_vector2()
    assert v1 and v2


def test_2d_vector_error_1():
    """
    Test for raising TypeError when an invalid argument is provided.
    """
    with raises(TypeError):
        init_vector2("")


def test_2d_vector_error_2():
    """
    Test for raising TypeError when invalid arguments are provided.
    """
    with raises(TypeError):
        init_vector2(1, 3, 4, "")


def test_2d_vector_error_3():
    """
    Test for raising TypeError when an invalid argument is provided.
    """
    with raises(TypeError):
        init_vector2(v1_x="")


def test_2d_vector_eq():
    """
    Test for the equality of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 1, 2)
    assert v1 == v2


def test_2d_vector_ne():
    """
    Test for the inequality of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 1, 3)
    assert v1 != v2


def test_2d_vector_lt():
    """
    Test for the less than comparison of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 3, 3)
    assert v1 < v2


def test_2d_vector_le():
    """
    Test for the less than or equal to comparison of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 1, 2)
    assert v1 <= v2


def test_2d_vector_gt():
    """
    Test for the greater than comparison of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 1, 1)
    assert v1 > v2


def test_2d_vector_ge():
    """
    Test for the greater than or equal to comparison of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 1, 2)
    assert v1 >= v2


def test_2d_vector_add():
    """
    Test for the addition of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 3, 4)
    result = v1 + v2
    assert result == Vector2(4, 6)


def test_2d_vector_sub():
    """
    Test for the subtraction of two Vector2 instances.
    """
    v1, v2 = init_vector2(3, 4, 1, 2)
    result = v1 - v2
    assert result == Vector2(2, 2)


def test_2d_vector_mul_scalar():
    """
    Test for multiplying a Vector2 instance by a scalar.
    """
    v1 = init_vector2(1, 2)[0]
    result = v1 * 2
    assert result == Vector2(2, 4)


def test_2d_vector_mul_vector():
    """
    Test for the multiplication of two Vector2 instances.
    """
    v1, v2 = init_vector2(2, 3, 1, 2)
    result = v1 * v2
    assert result == Vector2(2, 6)


def test_2d_vector_div_scalar():
    """
    Test for dividing a Vector2 instance by a scalar.
    """
    v1 = init_vector2(4, 6)[0]
    result = v1 / 2
    assert result == Vector2(2.0, 3.0)


def test_2d_vector_norm():
    """
    Test for calculating the Euclidean norm of a Vector2 instance.
    """
    v1 = init_vector2(3, 4)[0]
    result = v1.norm()
    assert result == 5.0


def test_2d_vector_normalize():
    """
    Test for normalizing a Vector2 instance.
    """
    v1 = init_vector2(3, 4)[0]
    result = v1.normalize()
    assert repr(result) == "Vector2(0.6, 0.8)"


def test_2d_vector_dot():
    """
    Test for calculating the dot product of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 3, 4)
    result = v1.dot(v2)
    assert result == 11


def test_2d_vector_length_squared():
    """
    Test for calculating the squared length of a Vector2 instance.
    """
    v1 = init_vector2(3, 4)[0]
    result = v1.length_squared()
    assert result == 25


def test_2d_vector_cross():
    """
    Test for calculating the custom "cross product" of two Vector2 instances.
    """
    v1, v2 = init_vector2(1, 2, 3, 4)
    result = v1.cross(v2)
    assert result == Vector2(2, -2)
