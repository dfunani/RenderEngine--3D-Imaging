from models.interfaces.responses import Response


def test_response():
    assert Response.error.value == 1
    assert Response.success.value == 2
    assert Response.warning.value == 3
