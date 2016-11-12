import pygame


class Musics(object):

    def __init__(self, resources, definition):
        filename = definition['abs_path']
        pygame.mixer.music.load(filename)

    def play(self):
        # Argument "music" is ignored
        pygame.mixer.music.play()
