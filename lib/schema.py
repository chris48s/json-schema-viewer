import asyncio
import urllib.parse
from dataclasses import dataclass

import httpx


@dataclass(eq=False)
class RemoteSchema:
    url: str
    schema: bytes = None

    @property
    def fetched(self):
        return bool(self.schema)

    def __eq__(self, other):
        return self.url == other.url

    @property
    def filepath(self):
        return urllib.parse.urlparse(self.url).path


def is_url(loc):
    return urllib.parse.urlparse(loc).scheme != ""


def get_base(url):
    return url.rpartition("/")[0]


def get_url(base, schema):
    url, _ = urllib.parse.urldefrag(
        urllib.parse.urljoin(f"{base.rstrip('/')}/", schema)
    )
    return url


def get_remote_ref_urls(node, base_url):
    refs = []
    if isinstance(node, list):
        for v in node:
            if isinstance(v, dict) or isinstance(v, list):
                refs = refs + get_remote_ref_urls(v, base_url)
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                if not is_url(v) and not v.startswith("#") and not v.startswith("/"):
                    refs.append(get_url(base_url, v))
            if isinstance(v, dict) or isinstance(v, list):
                refs = refs + get_remote_ref_urls(v, base_url)
    return list(set(refs))


async def get_remote_schema_refs(client, schema):
    r = await client.get(schema.url)
    r.raise_for_status()
    schema.schema = r.content

    refs = get_remote_ref_urls(r.json(), get_base(schema.url))
    return [RemoteSchema(url=ref) for ref in refs]


async def collect_schemas(schemas):
    client = httpx.AsyncClient()
    futures = [get_remote_schema_refs(client, s) for s in schemas if not s.fetched]

    for refs in await asyncio.gather(*futures):
        for ref in refs:
            if ref not in schemas:
                schemas.append(ref)

    if all([s.fetched for s in schemas]):
        return schemas

    return await collect_schemas(schemas)
