
class OverlayDict(object):

    '''
    OverlayDict operates on two dictionaries: base and overlay
    once the overlay switch is set to True, the base switch becomes
    immutable, and the overlay dict take precedence on all operations
    '''

    def __init__(self, *args):
        self.overlay = {}
        self.base = {}
        # base: only base is visible, base is mutable
        # overlay: only overlay is visible, overlay is mutable
        # both: overlay over base is visible, base is immutable
        self.switch = "base"

    def set_overlay(self, overlay):
        self.overlay = overlay

    def reset_overlay(self):
        self.overlay = {}

    def is_overlay(self, key):
        if key in self.overlay:
            return True
        return False

    def __nonzero__(self):
        if self.switch == "both" or self.switch == "overlay":
            return bool(self.overlay)
        else:
            return bool(self.base)

    def __repr__(self):
        d = {}
        for k, v in self.items():
            d[k] = v
        return str(d)

    def __getitem__(self, key):
        if self.switch == "both":
            try:
                value = self.overlay[key]
            except KeyError:
                value = self.base[key]
        elif self.switch == "base":
            value = self.base[key]
        elif self.switch == "overlay":
            value = self.overlay[key]

        return value

    def keys(self):
        keys = set(self.base.keys()).union(set(self.overlay.keys()))
        return list(keys)

    def items(self):
        keys = set(self.keys()).union(set(self.overlay.keys()))
        for key in list(keys):
            yield key, self.__getitem__(key)

    def __setitem__(self, key, value):
        if self.switch == "both" or self.switch == "overlay":
            self.overlay[key] = value
        elif self.switch == "base":
            self.base[key] = value

    def __delitem__(self, key):
        if self.switch == "both" or self.switch == "overlay":
            dict.__delitem__(self.overlay, key)
        elif self.switch == "base":
            dict.__delitem__(self.base, key)

    def update(self, other=None, **kwargs):
        if self.switch == "both" or self.switch == "overlay":
            self.overlay.update(other)
        elif self.switch == "base":
            self.base.update(other)
