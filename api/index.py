import os
from pathlib import Path
from tempfile import TemporaryDirectory

from requests.exceptions import RequestException
from starlette.applications import Starlette
from starlette.responses import RedirectResponse, Response
from starlette.routing import Route

from lib.renderer import render_schema
from lib.schema import RemoteSchema, collect_schemas


async def view(request):
    url = request.query_params.get("url")
    if not url:
        return RedirectResponse(url="/")

    try:
        schemas = collect_schemas([RemoteSchema(url=url)])
    except RequestException as e:
        return Response(str(e), status_code=500, media_type="text/plain")

    with TemporaryDirectory() as tempdir:
        for i, schema in enumerate(schemas):
            filename = Path(tempdir) / schema.filepath.lstrip("/")
            filename.parent.mkdir(parents=True, exist_ok=True)
            if i == 0:
                target_filename = filename
            with open(filename, "wb") as f:
                f.write(schema.schema)

        rendered = render_schema(target_filename)

    return Response(rendered, status_code=200, media_type="text/html")


routes = [Route("/view", endpoint=view)]

debug = str(os.getenv("DEBUG", "false")).lower() in ["true", "1"]
app = Starlette(debug=debug, routes=routes)
