import os
import yaml
import shutil
import tempfile
import zipfile


class Project(object):

    def __init__(self, filename=None):

        self.temp_dir = tempfile.mkdtemp(prefix="wiggler-")
        self.def_filename = os.path.join(self.temp_dir, "project.yaml")
        self.resources_dir = os.path.join(self.temp_dir, "resources")
        if filename is None:
            self.create_new()
        else:
            self.unpack_projectfile(filename)
        self.load()
        self.needs_save = False

    def create_new(self):
        os.mkdir(self.resources_dir)
        project_def = {
            'name': "untitled",
            'characters': None,
            'background': {
                'type': 'solid',
                'color': "255, 255, 255",
            },
        }
        with open(self.def_filename, "w") as project_file:
            yaml.dump(project_def, project_file)

    def unpack_projectfile(self, project_filename):
        with zipfile.ZipFile(project_filename, 'r') as project_file:
            project_file.extractall(self.temp_dir)

    def load(self):
        with open(self.def_filename) as project_file:
            defs = yaml.load(project_file.read())
        self.name = defs['name']
        self.characters = defs['characters']
        self.background = defs['background']

    def save(self, project_filename):
        with zipfile.ZipFile(project_filename, 'w') as project_file:
            for root, dirs, files in os.walk(self.temp_dir):
                rel_path = os.path.relpath(root, start=self.temp_dir)
                project_file.write(root, rel_path)
                for filename in files:
                    project_file.write(
                        os.path.join(root, filename),
                        os.path.join(rel_path, filename))

    def cleanup(self):
        shutil.rmtree(self.temp_dir)
