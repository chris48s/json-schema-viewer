import responses
from starlette.testclient import TestClient

from api.index import app


def test_view_no_url():
    client = TestClient(app)
    response = client.get("/view", allow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


@responses.activate
def test_view_with_valid_url():
    client = TestClient(app)
    responses.add(
        responses.GET,
        "https://example.com/foobar.json",
        json={
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {"num": {"type": "number"}},
        },
        status=200,
    )
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


@responses.activate
def test_view_with_invalid_url():
    client = TestClient(app)
    responses.add(
        responses.GET,
        "https://example.com/foobar.json",
        body="not json",
        status=200,
    )
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 500
