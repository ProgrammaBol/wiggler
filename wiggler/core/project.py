

class Project(object):

    def __init__(self, resources, events, filename=None):
        self.resources = resources
        self.events = events
        self.needs_save = False
        self.code_status = "undef"
        self.active_sprite = None
        self.stage_background = None
        self.name = None
        if filename is None:
            project_def = {
                'name': "untitled",
                'characters': {},
                'background': {
                    'type': 'solid',
                    'color': "255, 255, 255",
                },
            }
            self.load(project_def=project_def)
        else:
            self.load(filename=filename)

    def load(self, filename=None, project_def=None):
        if self.needs_save:
            # check if we want to save current project
            pass
        if project_def is not None:
            project_def = self.resources.create_new_project(
                project_def=project_def)
        if filename is not None:
            project_def = self.resources.load_project(filename)

        self.name = project_def['name']
        self.stage_background = project_def['background']
        self.events.send('projload')

    def play(self):
        self.events.send('preplay')
        if self.code_status == "undef":
            self.events.send('play')
        else:
            # TODO: warn about errors in the code
            pass
