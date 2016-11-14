'''
self-sufficiency levels

0: click on variables for __init__
1: write variables on __init__
2: writ custom_update
3: write functions of prite class
4: write sprite class completely
5: wirte yaml files directly (no more ui to add stuff) (resources pane,
metadata files tabs)
6: sprite base classes removed
'''


class SelfSufficiency(object):

    def __init__(self, resources, initial_level=0):
        self.resources = resources
        self.templates = {}
        for template_name, template_def in self.resources.templates.items():
            template = self.resources.load_resource('templates', template_name)
            self.templates[template_def['self_sufficiency']] = template
        self.level = initial_level
        self.buffers_lists = [
            ['__init__'],  # level 0
            ['custom_update'],  # level 1
        ]

    def set_level(self, level):
        self.level = level

    def get_template(self):
        return self.templates[self.level]

    def get_buffers_list(self):
        return self.buffers_lists[self.level]
