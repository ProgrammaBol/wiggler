
class SoundsSet(object):

    def __init__(self, resources, names=[]):
        self.resources = resources
        self.sounds = {}
        if names:
            for sound_name in names:
                self.add(sound_name)

    def add(self, sound_name):
        sound = self.resources.load_sound(sound_name)
        self.sounds[sound_name] = sound

    def play(self, sound_name, loop=False):
        sound = self.sounds[sound_name]
        if loop:
            sound.loop_play()
        else:
            sound.single_play()


class AnimationsSet(object):

    def __init__(self, resources, animation_names=[]):
        self.resources = resources
        self.animations = {}
        for animation_name in self.animations:
            self.add(animation_name)

    def add(self, animation_name):
        animation = self.resources.load_animation(animation_name)
        self.animations[animation_name] = animation

    def play(self, animation_name):
        animation = self.animations[animation_name]
        frame = animation.frame_generator()
        try:
            next(frame)
            return True
        except StopIteration:
            return False


class CostumesSet(object):

    def __init__(self, resources, costume_names=[]):
        self.resources = resources
        self.active = None
        self.costumes = {}
        self.costumes_list = []
        self.count = 0
        for costume_name in costume_names:
            self.add(costume_name)

        try:
            self.active = self.costumes[self.costumes_list[0]]
        except IndexError:
            pass

    def add(self, costume_name, position=None, make_active=False):
        costume = self.resources.load_resource('costumes', costume_name)
        self.costumes[costume_name] = costume
        if position is not None:
            self.costumes_list.insert(position, costume_name)
        else:
            self.costumes_list.append(costume_name)
        if make_active:
            self.set_active(costume_name)

    def remove(self, costume_name):
        self.costumes_list.remove(costume_name)
        if self.active == costume_name:
            self.active = None

    def set_active(self, costume_name):
        self.active = self.costumes[costume_name]
        return self.active.get()

    def get_active(self, rotate=0):
        return self.active.get(rotate=rotate)
