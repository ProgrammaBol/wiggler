from wiggler.engine.sets import CostumesSet, AnimationsSet, SoundsSet
from wiggler.core.code_handler import CodeHandler

def_fields = {
    'base_class': {},
    'costumes': {},
    'animations': {},
    'sounds': {},
    'user_code': {},
}


class SpriteBuilder(object):

    def __init__(self, resources, name, definition, **params):
        self.resources = resources
        self.name = name
        self.definition = definition
        self.base_class = definition['base_class']
        self.costumes = CostumesSet(resources, definition['costumes'])
        self.animations = AnimationsSet(resources, definition['animations'])
        self.sounds = SoundsSet(resources, definition['sounds'])
        self.user_code = definition['user_code']
        self.init_data = definition.get('init_data', {})
        self.module_filename = params['module_file']
        self.code_handler = CodeHandler(
            self.resources, 'sprite', self.name, self.user_code,
            self.module_filename)
        self.events = params['events']

    def add_costume(self, costume_name):
        self.costumes.add(costume_name)
        if costume_name not in self.definition['costumes']:
            self.definition['costumes'].append(costume_name)
            self.definition['modified'] = True

    def del_costume(self, costume_name):
        self.costumes.remove(costume_name)
        self.definition['costumes'].remove(costume_name)
        self.definition['modified'] = True

    def update_user_code(self, user_code):
        self.definition['user_code'] = user_code
        self.user_code = user_code
        self.code_handler.update_user_code(self.user_code)

    def build(self):
        sprite = None
        extra_init_data = {
            'costumes_set': self.costumes,
            'animations_set': self.animations,
            'sounds_set': self.sounds,
        }
        self.init_data.update(extra_init_data)
        if self.code_handler.module is not None:
            sprite = self.code_handler.module.Sprite(
                self.resources, self.events, self.init_data)
        return sprite
