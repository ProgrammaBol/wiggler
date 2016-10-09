import os

def file_load(root_path, filepath):
    file_handle = open(filepath, "r")
    resource_name = os.path.relpath(os.path.splitext(filepath)[0], root_path)
    return {resource_name: file_handle}


def loader(path, root_path=None):
    results = {}
    if os.path.isdir(path):
        if root_path is None:
            root_path=path
        for dirpath, dirs, files in os.walk(path):
            for filename in files:
                results.update(file_load(root_path, os.path.join(dirpath,filename)))
    else:
        if root_path is None:
            raise Exception("load on files needs a root path")
        results.update(file_load(root_path, path))
    return results
