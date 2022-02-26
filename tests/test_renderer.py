from pathlib import Path

from lib import renderer


def test_renderer():
    # very basic smoke test
    # this will basically just flag breaking API changes in json_schema_for_humans

    html = renderer.render_schema(
        Path.cwd() / "tests" / "testfiles" / "example.json", renderer.get_config({})
    )
    assert "<!DOCTYPE html>" in html
