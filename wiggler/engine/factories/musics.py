import pygame


class Musics(object):

    def __init__(self, resources, name, definition, **params):
        filename = definition['abs_path']
        self.name = name
        pygame.mixer.music.load(filename)

    def play(self):
        # Argument "music" is ignored
        pygame.mixer.music.play()
