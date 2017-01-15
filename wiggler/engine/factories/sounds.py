import pygame

def_fields = {}


class SoundChannels(object):

    def __init__(self, num_channels, reserved):
        pygame.mixer.stop()
        pygame.mixer.set_num_channels(num_channels)
        pygame.mixer.set_reserved(reserved)
        self.channels = dict()

    def loop_play(self, sound):
        channel = pygame.mixer.find_channel(True)
        channel.play(sound, loops=-1)
        self.channels[id(channel)] = channel
        return id(channel)

    def stop_loop(self, channelid):
        self.channels[channelid].stop()
        del (self.channels[channelid])

    def single_play(self, sound):
        channel = pygame.mixer.find_channel(True)
        channel.play(sound)


class Sound(object):

    def __init__(self, resources, name, definition, **params):
        filename = definition['abs_path']
        self.content = pygame.mixer.Sound(filename)
        self.channel = None
        self.name = name
        self.channels = resources.sound_channels

    def loop_play(self):
        self.channel = self.channels.loop_play(self.content)

    def loop_stop(self):
        self.channels.loop_stop(self.channel)

    def single_play(self):
        self.channels.single_play(self.content)
