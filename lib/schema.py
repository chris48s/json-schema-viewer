import urllib.parse
from dataclasses import dataclass

import requests


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
    return urllib.parse.urljoin(f"{base.rstrip('/')}/", schema)


def get_remote_refs(node, base_url):
    refs = []
    if isinstance(node, list):
        for v in node:
            if isinstance(v, dict) or isinstance(v, list):
                refs = refs + get_remote_refs(v, base_url)
    if isinstance(node, dict):
        for k, v in node.items():
            if k == "$ref" and isinstance(v, str):
                if not is_url(v) and not v.startswith("#") and not v.startswith("/"):
                    refs.append(get_url(base_url, v))
            if isinstance(v, dict) or isinstance(v, list):
                refs = refs + get_remote_refs(v, base_url)
    return list(set(refs))


def collect_schemas(schemas):
    for schema in schemas:
        if schema.fetched:
            continue
        r = requests.get(schema.url)
        r.raise_for_status()
        refs = get_remote_refs(r.json(), get_base(schema.url))
        for ref in refs:
            new_schema = RemoteSchema(url=ref)
            if new_schema not in schemas:
                schemas.append(new_schema)
        schema.schema = r.content
    if len([s.fetched for s in schemas]) == len(schemas):
        return schemas
    return collect_schemas(schemas)
