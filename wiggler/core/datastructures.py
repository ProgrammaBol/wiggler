
class OverlayDict(dict):

    '''
    OverlayDict operates on two dictionaries: base and overlay
    once the overlay switch is set to True, the base switch becomes
    immutable, and the overlay dict take precedence on all operations
    '''

    def __init__(self, *args):
        dict.__init__(self, *args)
        self.overlay = {}
        # base: only base is visible, base is mutable
        # overlay: only overlay is visible, overlay is mutable
        # both: overlay over base is visible, base is immutable
        self.switch = "base"

    def set_overlay(self, overlay):
        self.overlay = overlay

    def is_overlay(self, key):
        if key in self.overlay:
            return True
        return False

    def __getitem__(self, key):
        if self.switch == "both":
            try:
                value = dict.__getitem__(self.overlay, key)
            except KeyError:
                value = dict.__getitem__(self, key)
        elif self.switch == "base":
            value = dict.__getitem__(self, key)
        elif self.switch == "overlay":
            value = dict.__getitem__(self.overlay, key)

        return value

    def __setitem__(self, key, value):
        if self.switch == "both" or self.switch == "overlay":
            dict.__setitem__(self.overlay, key, value)
        elif self.switch == "base":
            dict.__setitem__(self, key, value)

    def __delitem__(self, key):
        if self.switch == "both" or self.switch == "overlay":
            dict.__delitem__(self.overlay, key)
        elif self.switch == "base":
            dict.__delitem__(self, key)

    def update(self, other=None, **kwargs):
        if self.switch == "both" or self.switch == "overlay":
            dict.update(self.overlay, other, **kwargs)
        elif self.switch == "base":
            dict.update(self, other, **kwargs)
