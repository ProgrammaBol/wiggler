import jinja2
import os


class Template(object):

    def __init__(self, name, resources, definition, **params):
        self.resources = resources
        self.name = name
        path, filename = os.path.split(definition['abs_path'])
        self.env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path))
        self.template = self.env.get_template(filename)
        self.template_source = self.env.loader.get_source(
            self.env, filename)[0]
        self.section_offset = {}
        self.find_section_start()

    def find_section_start(self):
        tree = self.env.parse(self.template_source)
        for variable in tree.find_all(jinja2.nodes.Getitem):
            if variable.node.name == 'user_code':
                self.section_offset[variable.arg.value] = variable.lineno

    def render(self, user_code):
        return self.template.render(class_name="example", user_code=user_code)
