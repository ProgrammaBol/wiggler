import pygame


class Character(pygame.sprite.Group):

    def __init__(self, resources, name, definition):
        super(Character, self).__init__()
        self.name = name
        self.resources = resources
        self.sprite_builders = {}
        self.spritedef_list = []
        sprite_names = definition['sprites']
        for name in sprite_names:
            self.spritedef_list.append(name)
            sprite_builder = self.resources.load_resource('sprites', name)
            self.sprite_builders[name] = sprite_builder

    def build_sprites(self):
        for name, sprite in self.sprite_builders.items():
            self.add(sprite.build())

    def destroy_sprites(self):
        self.empty()

    def get_sprite(self, name=None, index=None):
        if name is not None:
            return self.sprite_builders[name]
        if index is not None:
            return self.sprite_builders[self.spritedef_list[index]]
