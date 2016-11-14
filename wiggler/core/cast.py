class Cast(object):

    def __init__(self, resources):
        self.resources = resources
        self.characters = {}
        self.indexes = {}
        for name, definition in self.resources.characters.items():
            self.characters[name] = definition

    def add_character(self, name, definition):
        character = self.resources.new_resource('characters', name, definition)
        self.characters[name] = character
        return character

    def set_index(self, name, index):
        self.indexes[index] = self.characters[name]

    def get_character(self, name=None, index=None):
        if name is not None:
            return self.characters[name]
        if index is not None:
            return self.indexes[index]
