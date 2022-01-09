import urllib
from pathlib import Path
from tempfile import TemporaryDirectory

from requests.exceptions import RequestException

from lib.http import Server
from lib.renderer import render_schema
from lib.schema import RemoteSchema, collect_schemas


class handler(Server):
    def do_GET(self):
        qs = urllib.parse.parse_qs(urllib.parse.urlparse(self.path).query)
        if not qs.get("url"):
            return self.redirect("/")

        url = qs["url"][0]

        try:
            schemas = collect_schemas([RemoteSchema(url=url)])
        except RequestException as e:
            return self.response(500, "text/plain", str(e))

        with TemporaryDirectory() as tempdir:
            for i, schema in enumerate(schemas):
                filename = Path(tempdir) / schema.filepath.lstrip("/")
                filename.parent.mkdir(parents=True, exist_ok=True)
                if i == 0:
                    target_filename = filename
                with open(filename, "wb") as f:
                    f.write(schema.schema)

            rendered = render_schema(target_filename)

        return self.response(200, "text/html", rendered)
