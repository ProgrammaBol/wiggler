from wiggler.engine.sets import CostumesSet, AnimationsSet, SoundsSet
from wiggler.core.code_handler import CodeHandler

def_fields = {
    'base_class': {},
    'costumes': {},
    'animations': {},
    'sounds': {},
    'sufficiency_level': {},
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
        self.sufficiency_level = definition['self_sufficiency']
        self.user_code = definition['user_code']
        self.init_data = definition.get('init_data', {})
        additional_initdata = {
            'costumes_set': self.costumes,
            'animations_set': self.animations,
            'sounds_set': self.sounds,
        }
        self.init_data.update(additional_initdata)
        self.code_handler = CodeHandler(
            self.resources, 'sprite', self.name, self.user_code,
            self.sufficiency_level)
        self.events = params['events']

    def update_user_code(self, user_code):
        self.definition['user_code'] = user_code
        self.user_code = user_code
        self.code_handler.update_user_code(self.user_code)

    def decrease_sufficiency(self):
        if self.sufficiency_level > 1:
            self.sufficiency_level -= 1
            self.code_handler.decrease_sufficiency()

    def increase_sufficiency(self):
        if self.sufficiency_level < 10:
            self.sufficiency_level += 1
            self.code_handler.increase_sufficiency()

    def build(self):
        sprite = None
        if self.code_handler.module is not None:
            sprite = self.code_handler.module.Sprite(
                self.resources, self.events, self.init_data)
        return sprite
