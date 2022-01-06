import urllib
from http.server import BaseHTTPRequestHandler
from tempfile import NamedTemporaryFile

import requests
from json_schema_for_humans.generation_configuration import GenerationConfiguration
from json_schema_for_humans.schema.intermediate_representation import (
    build_intermediate_representation,
)
from json_schema_for_humans.template_renderer import TemplateRenderer
from requests.exceptions import RequestException


class handler(BaseHTTPRequestHandler):
    def _response(self, code, content_type, body):
        self.send_response(code)
        self.send_header("Content-type", content_type)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def _redirect(self, location):
        body = f"""
        <!DOCTYPE html>
        <html lang="en">
          <head>
            <meta charset="utf-8">
            <title>Redirecting&hellip;</title>
            <meta http-equiv="refresh" content="0; url={location}" />
            <script>location="{location}"</script>
            <meta name="robots" content="noindex">
          </head>
          <body>
            <h1>Redirecting&hellip;</h1>
            <p>
              This page has moved to
              <a href="{location}">{location}</a>.
            </p>
          </body>
        </html>
        """
        self.send_response(302)
        self.send_header("Location", location)
        self.end_headers()
        self.wfile.write(body.encode("utf-8"))

    def do_GET(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if not qs.get("url"):
            return self._redirect("/")

        url = qs["url"][0]

        try:
            resp = requests.get(url)
            resp.raise_for_status()
        except RequestException as e:
            return self._response(500, "text/plain", str(e))

        # TODO: try/catch. What errors does this throw?
        rendered = self._render_schema(resp.content)

        return self._response(200, "text/html", rendered)

    def _render_schema(self, schema):
        config = GenerationConfiguration(
            minify=False,
            description_is_markdown=True,
            deprecated_from_description=False,
            show_breadcrumbs=True,
            collapse_long_descriptions=False,
            default_from_description=False,
            expand_buttons=True,
            copy_css=False,
            copy_js=False,
            link_to_reused_ref=True,
            recursive_detection_depth=25,
            template_name="js",
            custom_template_path=None,
            show_toc=False,
            examples_as_yaml=False,
            with_footer=True,
            footer_show_time=False,
        )

        template_renderer = TemplateRenderer(config)

        with NamedTemporaryFile(suffix='.json') as tmp:
            tmp.write(schema)
            tmp.seek(0)
            intermediate_schema = build_intermediate_representation(tmp, None)

        return template_renderer.render(intermediate_schema)
