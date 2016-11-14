import jinja2
import os


class Template(object):

    def __init__(self, name, resources, definition):
        self.resources = resources
        self.name = name
        path, filename = os.path.split(definition['abs_path'])
        env = jinja2.Environment(
            loader=jinja2.FileSystemLoader(path))
        self.template = env.get_template(filename)

    def render(self, user_code):
        return self.template.render(class_name="example", user_code=user_code)
