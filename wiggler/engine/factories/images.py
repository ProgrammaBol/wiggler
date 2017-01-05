import pygame

def_fields = {}


class Image(object):

    def __init__(self, resources, name, definition, **params):
        filename = definition['abs_path']
        self.content = pygame.image.load(filename)
        self.name = name
