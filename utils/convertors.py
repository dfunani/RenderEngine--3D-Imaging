# Specializations for Vect
from models.vectors import Vector2, Vector2f, Vector2i, Vector3, Vector3f, Vector3i


def float_to_int_vector2(v: Vector2f) -> Vector2i:
    """Convert Vect with float components to Vect with int components."""
    return Vector2i(int(v.x + 0.5), int(v.y + 0.5), int(v.z + 0.5))


def int_to_float_vector2(v: Vector2i) -> Vector2f:
    """Convert Vect with int components to Vect with float components."""
    return Vector2f(v.x, v.y, v.z)


def float_to_int_vector3(v: Vector3f) -> Vector3i:
    """Convert Vect with float components to Vect with int components."""
    return Vector3i(int(v.x + 0.5), int(v.y + 0.5), int(v.z + 0.5))


def int_to_float_vector3(v: Vector3i) -> Vector3f:
    """Convert Vect with int components to Vect with float components."""
    return Vector3f(v.x, v.y, v.z)

# Define ostream-like output for Vector2 and Vect
def Vector2_to_str(v: Vector2) -> str:
    """Return a string representation for Vector2."""
    return f"({v.x}, {v.y})\n"


def Vect_to_str(v: Vector3) -> str:
    """Return a string representation for Vect."""
    return f"({v.x}, {v.y}, {v.z})\n"