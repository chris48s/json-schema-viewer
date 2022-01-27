import respx
from httpx import Response
from starlette.testclient import TestClient

from api.index import app


def test_view_no_url():
    client = TestClient(app)
    response = client.get("/view", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


@respx.mock
def test_view_with_valid_url():
    client = TestClient(app)
    respx.get("https://example.com/foobar.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {"num": {"type": "number"}},
            },
        )
    )
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


@respx.mock
def test_view_with_invalid_url():
    client = TestClient(app)
    respx.get("https://example.com/foobar.json").mock(
        return_value=Response(200, content="not json")
    )
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 500
