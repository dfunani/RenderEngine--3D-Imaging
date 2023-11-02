from models.interfaces.constants import Resolution


def test_constants():
    assert isinstance(Resolution.__WIDTH__, int)
    assert (Resolution.__WIDTH__) == 1024
    assert isinstance(Resolution.__HEIGHT__, int)
    assert (Resolution.__HEIGHT__) == 768
