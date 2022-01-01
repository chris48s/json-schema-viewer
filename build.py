#!/usr/bin/env python3

import shutil
from pathlib import Path

import json_schema_for_humans
from json_schema_for_humans.const import DEFAULT_CSS_FILE_NAME, DEFAULT_JS_FILE_NAME

base_dir = Path(json_schema_for_humans.__file__).parent


def _copyfile(src, dst):
    print(f"copying from\n{src}\nto\n{dst}\n")
    shutil.copyfile(src, dst)


_copyfile(
    base_dir / "templates" / "js" / DEFAULT_CSS_FILE_NAME,
    Path("./public") / DEFAULT_CSS_FILE_NAME,
)
_copyfile(
    base_dir / "templates" / "js" / DEFAULT_JS_FILE_NAME,
    Path("./public") / DEFAULT_JS_FILE_NAME,
)
