

class Project(object):

    def __init__(self, resources, events, filename=None):
        self.resources = resources
        self.events = events
        self.needs_save = False
        self.code_status = "undef"
        self.active_sprite = None
        self.stage_background = None
        self.name = None
        self.abspath = None
        if filename is None:
            self.new()
        else:
            self.load(filename=filename)

    def new(self):
        project_def = {
            'name': "untitled",
            'characters': {},
            'background': {
                'type': 'solid',
                'color': "255, 255, 255",
            },
        }
        project_def = self.resources.create_new_project(
            project_def=project_def)

        self.load_def(project_def)

    def load(self, filename):
        project_def = self.resources.load_project(filename)
        self.abspath = filename
        self.load_def(project_def)

    def load_def(self, project_def):
        self.name = project_def['name']
        self.stage_background = project_def['background']
        self.events.send('projload')

    def save(self, filename):
        self.abspath = filename
        self.resources.save_project(filename)

    def play(self):
        self.events.send('preplay')
        if self.code_status == "undef":
            self.events.send('play')
        else:
            # TODO: warn about errors in the code
            pass
