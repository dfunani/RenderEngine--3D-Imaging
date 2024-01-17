"""
test_2d_vectors.py - Test module for the Vector3 class representing 3D vectors.

This module contains a set of unit tests to ensure the correct functionality
of the Vector3 class, which represents 3D vectors. The tests cover various
methods and operations defined in the Vector3 class, including vector
arithmetic, comparison, and mathematical operations.

Tested Methods and Operations:
- Initialization (__init__)
- String representation (__repr__)
- Equality (__eq__) and inequality (__ne__)
- Magnitude comparison (__gt__, __ge__, __lt__, __le__)
- Vector arithmetic: addition (__add__), subtraction (__sub__), multiplication (__mul__)
- Scalar division (__truediv__)
- Indexing (__getitem__ and __setitem__)
- Exponentiation (__pow__)
- Negation (__neg__) and positive copy (__pos__)
- Dot product calculation (dot)
- Cross product calculation (cross)
- Vector magnitude calculation (length)
- Squared vector magnitude calculation (length_squared)
- Vector normalization (normalize)
- Euclidean norm calculation (norm)

Usage:
    To run the tests, execute this module as the main program:
    ```
    python test_2d_vectors.py
    ```

    If all tests pass, a success message will be displayed.

Author:
    [Your Name]

Date:
    [Current Date]
"""

from math import isclose

from models.geometry.vectors_3d import Vector3


def test_init():
    """Test initialization of Vector3 instances."""
    vec = Vector3(1.0, 2.0, 3.0)
    assert vec.x == 1.0
    assert vec.y == 2.0
    assert vec.z == 3.0


def test_repr():
    """Test the __repr__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    assert repr(vec) == "Vector3(1.0, 2.0, 3.0)"


def test_eq():
    """Test the __eq__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(1.0, 2.0, 3.0)
    assert vec1 == vec2


def test_ne():
    """Test the __ne__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    assert vec1 != vec2


def test_gt():
    """Test the __gt__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    assert vec2 > vec1


def test_ge():
    """Test the __ge__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    assert vec2 >= vec1


def test_lt():
    """Test the __lt__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    assert vec1 < vec2


def test_le():
    """Test the __le__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    assert vec1 <= vec2


def test_add():
    """Test the __add__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    result = vec1 + vec2
    assert result == Vector3(5.0, 7.0, 9.0)


def test_sub():
    """Test the __sub__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    result = vec1 - vec2
    assert result == Vector3(-3.0, -3.0, -3.0)


def test_mul():
    """Test the __mul__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    result_vec = vec1 * vec2
    assert result_vec == Vector3(4.0, 10.0, 18.0)

    result_scalar = vec1 * 2
    assert result_scalar == Vector3(2.0, 4.0, 6.0)


def test_truediv():
    """Test the __truediv__ method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    scalar = 2.0
    result = vec1 / scalar
    assert result == Vector3(0.5, 1.0, 1.5)


def test_getitem():
    """Test the __getitem__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    assert vec[0] == 1.0
    assert vec[1] == 2.0
    assert vec[2] == 3.0


def test_setitem():
    """Test the __setitem__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    vec[0] = 4.0
    assert vec == Vector3(4.0, 2.0, 3.0)


def test_pow():
    """Test the __pow__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = vec**2
    assert result == Vector3(1.0, 4.0, 9.0)


def test_neg():
    """Test the __neg__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = -vec
    assert result == Vector3(-1.0, -2.0, -3.0)


def test_pos():
    """Test the __pos__ method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = +vec
    assert result == Vector3(1.0, 2.0, 3.0)


def test_dot():
    """Test the dot method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    result = vec1.dot(vec2)
    assert result == 32.0


def test_cross():
    """Test the cross method."""
    vec1 = Vector3(1.0, 2.0, 3.0)
    vec2 = Vector3(4.0, 5.0, 6.0)
    result = vec1.cross(vec2)
    assert result == Vector3(-3.0, 6.0, -3.0)


def test_length():
    """Test the length method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = vec.length()
    assert isclose(result, 3.741657, abs_tol=1e-6)


def test_length_squared():
    """Test the length_squared method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = vec.length_squared()
    assert result == 14.0


def test_normalize():
    """Test the normalize method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = vec.normalize()
    assert isclose(result.length(), 1.0, abs_tol=1e-6)


def test_norm():
    """Test the norm method."""
    vec = Vector3(1.0, 2.0, 3.0)
    result = vec.norm()
    assert isclose(result, 3.741657, abs_tol=1e-6)
