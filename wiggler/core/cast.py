class Cast(object):

    def __init__(self, resources):
        self.resources = resources
        self.characters = {}
        self.indexes = {}
        self.active_character = 0
        self.reload()

    def add_character(self, name, definition):
        character = self.resources.add_resource('characters', name, definition)
        self.characters[name] = character
        return character

    def del_character(self, name):
        del self.characters[name]
        index = self.get_index(name)
        del self.indexes[index]

    def set_index(self, name, index):
        self.indexes[index] = self.characters[name]

    def get_index(self, name):
        for index, character in self.indexes.items():
            if character == self.characters[name]:
                return index

        return None

    def reload(self):
        self.characters = {}
        self.active_character = 0
        self.indexes = {}
        for name in self.resources.characters.keys():
            self.characters[name] = self.resources.load_resource(
                'characters', name)

    def set_active_character(self, name=None, index=None):
        if name is not None:
            for index in self.indexes:
                if self.indexes[index] == self.characters[name]:
                    break
        if index is not None:
            self.active_character = index
        return self.indexes[index]

    def get_character(self, name=None, index=None):
        if name is None and index is None:
            index = self.active_character
        if name is not None:
            return self.characters[name]
        if index is not None:
            try:
                return self.indexes[index]
            except KeyError:
                return None
