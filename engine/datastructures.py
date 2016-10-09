import pygame
import os
from core.file_loader import loader
from engine.sprites import SpritesLib
from engine.sounds import SoundsLib
from engine.texts import TextLib
from engine.animations import Animations

class StageContext(object):

    def __init__(self, context):
        for k,v in context.iteritems():
            setattr(self, k, v)
        self.load_sounds(self.sounds_dir)
        self.load_sheets(self.graphics_dir)
        self.load_graphics(self.graphics_file)
        self.load_music(self.music_dir)
        self.load_fonts(self.font_dir)
        self.load_animations(self.animations_file)

    def add(self, key, value):
        setattr(self, key, value)

    def load_sheets(self, dir):
        self.spriteslib = SpritesLib(self)
        for name, handle, meta in loader(dir):
            try:
                colorkey = meta["colorkeys"][name]
            except KeyError:
                colorkey = None
            self.spriteslib.add_sheet(name, handle, colorkey=colorkey)
        self.add("sprites", self.spriteslib)

    def load_sounds(self):
        self.soundslib = SoundsLib()
        self.soundslib.add_sound("alloyshipthrust", os.path.normpath("assets/sounds/alloyshipthrust.wav"))
        self.soundslib.add_sound("gunshot", os.path.normpath("assets/sounds/gunshot.wav"))
        self.soundslib.add_sound("gunblast", os.path.normpath("assets/sounds/gunblast.wav"))
        self.soundslib.add_sound("explosion", os.path.normpath("assets/sounds/explosion.wav"))
        self.add("sounds", self.soundslib)

    def load_music(self):
        self.soundslib.add_music("intro", os.path.normpath("assets/music/intro.wav"))

    def load_animations(self):
        self.animations = Animations(self)

    def load_fonts(self):
        self.textlib = TextLib(self)
        self.add("text", self.textlib)

class EventQueue(object):

    def __init__(self):
        self.subscriptions = dict()
        self.subscriptions["keyboard"] = dict()

    def subscribe(self, eventsource, eventtype, eventid, callback_handler):
        if eventtype not in self.subscriptions[eventsource]:
            self.subscriptions[eventsource][eventtype] = dict()
        self.subscriptions[eventsource][eventtype][eventid] = callback_handler

    def unsubscribe(self, eventsource, eventtype, eventid):
        if eventsource in self.subscriptions and eventtype in self.subscriptions[eventsource] and eventid in self.subscriptions[eventsource][eventtype]:
            self.subscriptions[eventsource][eventtype][eventid]

    def handle_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            for eventtype in self.subscriptions["keyboard"]:
                if event.type == eventtype:
                    for eventid in self.subscriptions["keyboard"][eventtype]:
                        if event.key == eventid:
                            handler = self.subscriptions["keyboard"][eventtype][eventid]
                            if handler is not None:
                                handler()
        return True
