import os
import shutil
import tempfile
import yaml
import zipfile


class ProjectRes(object):

    def __init__(self):

        self.temp_dir = tempfile.mkdtemp(prefix="wiggler-project-")
        self.def_filename = os.path.join(self.temp_dir, "project.yaml")
        self.resources_dir = os.path.join(self.temp_dir, "resources")
        self.filename = None

    def create_new(self, project_def):
        os.mkdir(self.resources_dir)
        with open(self.def_filename, "w") as project_file:
            yaml.dump(project_def, project_file)
        return self.load()

    def load(self, filename=None):
        if filename is not None:
            self.filename = filename
            with zipfile.ZipFile(self.filename, 'r') as project_file:
                project_file.extractall(self.temp_dir)
        with open(self.def_filename) as project_file:
            project_def = yaml.load(project_file.read())
        return project_def

    def save(self, filename=None):
        if filename is None:
            filename = self.filename
        with zipfile.ZipFile(filename, 'w') as project_file:
            for root, dirs, files in os.walk(self.temp_dir):
                rel_path = os.path.relpath(root, start=self.temp_dir)
                project_file.write(root, rel_path)
                for name in files:
                    project_file.write(
                        os.path.join(root, name),
                        os.path.join(rel_path, name))

    def cleanup(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)
