import pygame

character_def_fields = {
    'sprites': {}
}


class Character(pygame.sprite.Group):

    def __init__(self, resources, name, definition, **params):
        super(Character, self).__init__()
        self.name = name
        self.resources = resources
        self.definition = definition
        self.builders = {}
        self.builders_list = []
        self.active_sprite = 0
        sprite_names = definition['sprites']
        for name in sprite_names:
            self.add_sprite(name)

    def add_sprite(self, sprite_name):
        self.builders_list.append(sprite_name)
        sprite_builder = self.resources.load_resource('sprites', sprite_name)
        self.builders[sprite_name] = sprite_builder
        if sprite_name not in self.definition['sprites']:
            self.definition['sprites'].append(sprite_name)

    def remove_sprite(self, sprite_name):
        self.builders_list.remove(sprite_name)
        del(self.biulders[sprite_name])
        self.active_sprite = 0
        self.definition['sprites'].remove(sprite_name)

    def set_active_sprite(self, spriteindex):
        if spriteindex is not None:
            self.active_sprite = spriteindex

    def build_sprites(self):
        for name, builder in self.builders.items():
            sprite = builder.build()
            if sprite is not None:
                self.add(builder.build())

    def destroy_sprites(self):
        self.empty()

    def get_sprite_builder(self, name=None, index=None):
        if index is None and name is None:
            index = self.active_sprite
        if name is not None:
            return self.builders[name]
        if index is not None:
            return self.builders[self.builders_list[index]]
