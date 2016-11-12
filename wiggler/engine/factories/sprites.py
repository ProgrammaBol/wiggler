from wiggler.engine.sets import CostumesSet, AnimationsSet, SoundsSet
from wiggler.core.module_generator import generate_module
from wiggler.core.self_sufficiency import SelfSufficiency


class Sprite(object):

    def __init__(self, resources, name, definition):
        self.resources = resources
        self.name = name
        self.base_class = definition['base_class']
        self.costumes = CostumesSet(resources, definition['costumes'])
        self.animations = AnimationsSet(resources, definition['animations'])
        self.sounds = SoundsSet(resources, definition['sounds'])
        self.sufficiency = SelfSufficiency(
            resources, definition['self_sufficiency'])
        self.user_code = definition['user_code']
        self.init_data = definition.get('init_data', {})
        self.generated_code = ""
        additional_initdata = {
            'costumes_set': self.costumes,
            'animations_set': self.animations,
            'sounds_set': self.sounds,
        }
        self.init_data.update(additional_initdata)
        self.set_template()

    def set_template(self):
        self.template = self.sufficiency.get_template()

    def decrease_sufficiency(self):
        if self.sufficiency.level > 1:
            self.sufficiency.level -= 1
        self.set_template()

    def increase_sufficiency(self):
        if self.sufficiency < 10:
            self.sufficiency += 1
        self.set_template()

    def build(self):
        module, self.generated_code = \
            generate_module(self.name, self.template, self.user_code)
        sprite = module.Sprite(self.resources, self.init_data)
        return sprite
