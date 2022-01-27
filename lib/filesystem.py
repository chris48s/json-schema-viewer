from pathlib import Path


def write_schemas(schemas, directory):
    for i, schema in enumerate(schemas):
        filename = Path(directory) / schema.filepath.lstrip("/")
        filename.parent.mkdir(parents=True, exist_ok=True)
        if i == 0:
            target_filename = filename
        with open(filename, "wb") as f:
            f.write(schema.schema)
    return target_filename
