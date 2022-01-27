import pytest
import respx
from httpx import Response

from lib import schema


def test_get_url_trailing_slash_base():
    assert (
        schema.get_url("http://base.url/", "schema.json")
        == "http://base.url/schema.json"
    )


def test_get_url_no_trailing_slash_base():
    assert (
        schema.get_url("http://base.url", "schema.json")
        == "http://base.url/schema.json"
    )


def test_get_url_with_anchor():
    assert (
        schema.get_url("http://base.url", "schema.json#foobar")
        == "http://base.url/schema.json"
    )


@pytest.mark.anyio
@respx.mock
async def test_collect_schemas():
    respx.get("https://example.com/schema.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "anyOf": [
                    {"$ref": "relative-schema1.json#"},
                    {"$ref": "relative-schema2.json#foo"},
                    {"$ref": "relative-schema2.json#bar"},
                    {"$ref": "https://explicit.external.ref/schema3.json"},
                    {"$ref": "#internal-ref4"},
                ],
            },
        )
    )
    for filename in ["relative-schema1.json", "relative-schema2.json"]:
        respx.get(f"https://example.com/{filename}").mock(
            return_value=Response(
                200,
                json={
                    "$schema": "http://json-schema.org/draft-07/schema#",
                    "type": "object",
                    "properties": {"num": {"type": "number"}},
                },
            )
        )

    result = await schema.collect_schemas(
        [schema.RemoteSchema(url="https://example.com/schema.json")]
    )
    urls = [s.url for s in result]

    assert len(respx.calls) == 3
    assert len(urls) == 3
    assert "https://example.com/schema.json" in urls
    assert "https://example.com/relative-schema1.json" in urls
    assert "https://example.com/relative-schema2.json" in urls
    assert all([s.fetched for s in result])


@pytest.mark.anyio
@respx.mock
async def test_collect_schemas_with_duplicates():
    respx.get("https://example.com/schema.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {
                    "created": {"$ref": "date.json#"},
                    "modified": {"$ref": "date.json#"},
                },
            },
        )
    )
    respx.get("https://example.com/date.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {
                    "d": {"type": "number"},
                    "m": {"type": "number"},
                    "y": {"type": "number"},
                },
            },
        )
    )

    result = await schema.collect_schemas(
        [schema.RemoteSchema(url="https://example.com/schema.json")]
    )
    urls = [s.url for s in result]

    assert len(respx.calls) == 2
    assert len(urls) == 2
    assert "https://example.com/schema.json" in urls
    assert "https://example.com/date.json" in urls
    assert all([s.fetched for s in result])


@pytest.mark.anyio
@respx.mock
async def test_collect_schemas_with_multiple_levels():
    respx.get("https://example.com/schema.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {
                    "relative1": {"$ref": "relative-schema1.json#"},
                },
            },
        )
    )
    respx.get("https://example.com/relative-schema1.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "properties": {
                    "relative2": {"$ref": "relative-schema2.json#"},
                },
            },
        )
    )
    respx.get("https://example.com/relative-schema2.json").mock(
        return_value=Response(
            200,
            json={
                "$schema": "http://json-schema.org/draft-07/schema#",
                "type": "object",
                "properties": {"num": {"type": "number"}},
            },
        )
    )

    result = await schema.collect_schemas(
        [schema.RemoteSchema(url="https://example.com/schema.json")]
    )
    urls = [s.url for s in result]

    assert len(respx.calls) == 3
    assert len(urls) == 3
    assert "https://example.com/schema.json" in urls
    assert "https://example.com/relative-schema1.json" in urls
    assert "https://example.com/relative-schema2.json" in urls
    assert all([s.fetched for s in result])
