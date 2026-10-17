from starlette.testclient import TestClient

from api.index import app


def test_view_no_url():
    client = TestClient(app)
    response = client.get("/view", follow_redirects=False)
    assert response.status_code == 307
    assert response.headers["location"] == "/"


def test_view_with_valid_url(httpx2_mock):
    httpx2_mock.add_response(
        url="https://example.com/foobar.json",
        json={
            "$schema": "http://json-schema.org/draft-07/schema#",
            "type": "object",
            "properties": {"num": {"type": "number"}},
        },
    )
    client = TestClient(app)
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 200
    assert b"<!DOCTYPE html>" in response.content


def test_view_with_invalid_url(httpx2_mock):
    httpx2_mock.add_response(url="https://example.com/foobar.json", content=b"not json")
    client = TestClient(app)
    response = client.get("/view?url=https%3A//example.com/foobar.json")
    assert response.status_code == 500
