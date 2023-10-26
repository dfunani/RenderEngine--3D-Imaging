from models.interfaces.responses import Response

def test_response():
    for index, res in enumerate(Response, start=1):
        assert res.value == index