import pygame


class Character(pygame.sprite.Group):

    def __init__(self, resources, name, definition):
        super(Character, self).__init__()
        self.name = name
        self.resources = resources
        self.builders = {}
        self.builders_list = []
        self.active_sprite = 0
        sprite_names = definition['sprites']
        for name in sprite_names:
            self.builders_list.append(name)
            sprite_builder = self.resources.load_resource('sprites', name)
            self.builders[name] = sprite_builder

    def set_active_sprite(self, spriteindex):
        if spriteindex is not None:
            self.active_sprite = spriteindex

    def build_sprites(self):
        for name, builder in self.builders.items():
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
