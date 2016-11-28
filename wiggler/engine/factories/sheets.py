'''
animations
defs
{
    'name': "name"
    'total_duration': msec,
    'equal_time': (true, false), #DEFAULT true
    'sequence': [
        ("sheet_name", (rect), duration),
        ("sheet_name", (rect), duration),
        ("sheet_name", (rect), duration),
        ...
    ],
    'sound': { # OPTIONAL
        "name": sound name,
        'loop': true, false, # DEFAULT false
    }
}

'''
import copy
import pygame

from wiggler.engine.exceptions import ResourceError


class Sheet(object):

    def __init__(self, resources, name, definition):
        self.name = name
        filename = definition['abs_path']
        surface_raw = pygame.image.load(filename)
        self.surface = surface_raw.convert()
        try:
            colorkey = tuple(map(int, definition['colorkey'].split(',')))
            self.surface.set_colorkey(colorkey)
        except KeyError:
            pass

    def get_surface(self):
        return self.surface

    def get_area(self, rect):
        return self.surface.subsurface(rect).copy()


class Costume(object):

    def __init__(self, resources, name, definition):
        self.name = name
        sheet = resources.load_sheet_by_filename(definition['sheet'])
        rect = tuple(map(int, definition['rect'].split(',')))
        self.surface = sheet.get_area(rect)
        self.rect = self.surface.get_rect()

    def get_image(self):
        return self.surface

    def get_raw_image(self):
        width = self.rect.width
        height = self.rect.height
        raw_image = pygame.image.tostring(self.surface, "RGBA")
        return width, height, raw_image

    def get(self, rotate=None):
        if rotate is not None:
            rotated_image = pygame.transform.rotate(
                self.surface,
                -rotate
            )
            return rotated_image, rotated_image.get_rect()
        else:
            return self.surface, self.rect


class Animation(object):

    def __init__(self, resources, name, definition):
        self.name = name
        self.sound = None
        try:
            self.sound = resources.load_sound(definition['sound'])
        except KeyError:
            pass
        except ResourceError:
            pass
        self.validate(definition)
        equal_time = definition.get('equal_time', True)
        self.frames = []
        self.durations = []
        self.total_duration = definition.get('total_duration', 0)
        self.set_sequence(definition['sequence'], equal_time)
        self.playback_position = 0
        self.clock = resources.clock
        self.nextframe_countdown = 0
        self.sound_played = False
        self.count = 0

    def validate(self, definition):
        pass

    def set_sequence(self, sequence, equal_time):
        # TYPE can be costumes or blitover
        for frame_full_def in sequence:
            if equal_time:
                sheet_name, rect = frame_full_def
                frame_duration = self.total_duration / len(sequence)
            else:
                sheet_name, rect, frame_duration = frame_full_def
                self.total_duration += frame_duration
            frame_def = (sheet_name, rect)
            self.frames.append(frame_def)
            self.durations.append(frame_duration)

    def frame_generator(self):
        remaining_frames = copy.copy(self.frames)
        remaining_durations = copy.copy(self.durations)
        remaining_time = self.total_duration
        if self.sound is not None:
            self.sound.single_play(self.sound)
        # first frame
        frame = remaining_frames.pop()
        duration = remaining_durations.pop()
        nextframe_countdown = duration
        yield frame
        while remaining_time > 0:
            time_msec = self.clock.get_time()
            nextframe_countdown -= time_msec
            remaining_time -= time_msec
            if nextframe_countdown <= 0:
                try:
                    frame = remaining_frames.pop()
                    duration = remaining_durations.pop()
                    nextframe_countdown = duration
                except IndexError:
                    pass
            yield frame
