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
