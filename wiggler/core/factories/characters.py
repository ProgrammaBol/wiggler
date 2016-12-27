import pygame


class Character(pygame.sprite.Group):

    def __init__(self, resources, name, definition):
        super(Character, self).__init__()
        self.name = name
        self.resources = resources
        self.spritedef = {}
        self.spritedef_list = []
        self.active_sprite = 0
        sprite_names = definition['sprites']
        for name in sprite_names:
            self.spritedef[name] = {}
            self.spritedef_list.append(name)
            sprite_builder = self.resources.load_resource('sprites', name)
            self.spritedef[name]['builder'] = sprite_builder

    def set_active_sprite(self, spriteindex):
        if spriteindex is not None:
            self.active_sprite = spriteindex

    def regenerate_sprites(self):
        for name in self.spritedef.keys():
            self.generate_sprite_code(name)

    def generate_sprite_code(self, name):
        sprite_builder = self.get_sprite_builder(name=name)
        sprite_builder.generate_code()

    def build_sprites(self):
        for name, spritedef in self.spritedef.items():
            sprite_builder = spritedef['builder']
            self.add(sprite_builder.build(spritedef['module']))

    def destroy_sprites(self):
        self.empty()

    def get_sprite_builder(self, name=None, index=None):
        if index is None and name is None:
            index = self.active_sprite
        if name is not None:
            return self.spritedef[name]['builder']
        if index is not None:
            return self.spritedef[self.spritedef_list[index]]['builder']
