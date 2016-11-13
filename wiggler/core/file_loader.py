import json
import os


def file_load(root_path, filepath, metadata):
    file_handle = open(filepath, "r")
    resource_name = os.path.relpath(os.path.splitext(filepath)[0], root_path)
    try:
        resource_metadata = metadata[os.path.filename]
    except (KeyError, TypeError):
        resource_metadata = None
    return resource_name, file_handle, resource_metadata


def metadata_load(dirpath):
    try:
        with open(os.path.join(dirpath, "metadata.json")) as metadata_file:
            metadata = json.load(metadata_file)
        return metadata
    except OSError:
        return None


def loader(path, root_path=None):
    results = {}
    if os.path.isdir(path):
        if root_path is None:
            root_path = path
        for dirpath, dirs, files in os.walk(path):
            metadata = metadata_load(dirpath)
            for filename in files:
                file_path = os.path.join(dirpath, filename)
                resource_name, file_handle = file_load(root_path,
                                                       file_path,
                                                       metadata)
                results.add(resource_name, file_handle, metadata)
    else:
        if root_path is None:
            raise Exception("load on files needs a root path")
        results.update(file_load(root_path, path))
    print results
    return results
