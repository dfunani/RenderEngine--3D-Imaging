from models.interfaces.constants import Resolution
def test_constants():
    assert type(Resolution.__WIDTH__) == int
    assert (Resolution.__WIDTH__) == 1024
    assert type(Resolution.__HEIGHT__) == int
    assert (Resolution.__HEIGHT__) == 768
    