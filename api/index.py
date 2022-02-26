import os
from json import JSONDecodeError
from tempfile import TemporaryDirectory

from httpx import HTTPError
from starlette.applications import Starlette
from starlette.responses import RedirectResponse, Response
from starlette.routing import Route

from lib.filesystem import write_schemas
from lib.renderer import get_config, render_schema
from lib.schema import RemoteSchema, collect_schemas


async def view(request):
    url = request.query_params.get("url")
    if not url:
        return RedirectResponse(url="/")

    try:
        schemas = await collect_schemas([RemoteSchema(url=url)])
    except (HTTPError, JSONDecodeError) as e:
        return Response(str(e), status_code=500, media_type="text/plain")

    with TemporaryDirectory() as tempdir:
        target_filename = write_schemas(schemas, tempdir)
        rendered = render_schema(target_filename, get_config(request.query_params))

    return Response(rendered, status_code=200, media_type="text/html")


routes = [Route("/view", endpoint=view)]

debug = str(os.getenv("DEBUG", "false")).lower() in ["true", "1"]
app = Starlette(debug=debug, routes=routes)
