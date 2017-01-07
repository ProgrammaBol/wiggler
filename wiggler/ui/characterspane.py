import wx


class CharactersPane(wx.ListCtrl):

    def __init__(self, parent, resources, events):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_ICON)
        self.events = events
        self.resources = resources
        self.il = wx.ImageList(30, 30, True)
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.events.subscribe(self, ['projload', 'load_character'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_select)

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'loadchar':
            self.load_character(name=event.data.charname)
        elif event.notice == 'charadded':
            self.add_character(event.data.charname, event.data.chardef)
        elif event.notice == 'add_char_sprite':
            character = self.resources.cast.get_character()
            character.add_sprite(event.data.sprite_name)
        elif event.notice == 'remove_char_sprite':
            character = self.resources.cast.get_character()
            character.remove_sprite(event.data.sprite_name)
        elif event.notice == 'add_sprite_costume':
            character = self.resources.cast.get_character()
            sprite = character.get_sprite_builder()
            sprite.add_costume(event.data.costume_name)
        elif event.notice == 'remove_sprite_costume':
            character = self.resources.cast.get_character()
            sprite = character.get_sprite_builder()
            sprite.add_costume(event.data.costume_name)
        event.Skip()

    def reload(self):
        self.resources.cast.reload()
        self.DeleteAllItems()
        for __, character in self.resources.cast.characters.items():
            self.load_character(character=character)

    def list_select(self, event):
        self.set_active_character(event.m_itemIndex)

    def set_active_character(self, index):
        character = self.resources.cast.set_active_character(index=index)
        self.events.send('actchar', character=character)

    def add_character(self, charname, chardef):
        character = self.resources.cast.add_character(charname, chardef)
        self.load_character(character=character)

    def load_character(self, name='', character=None):
        if character is None:
            character = self.resources.cast.get_character(name=name)
        sprite_builder = character.get_sprite_builder(index=0)
        costume = sprite_builder.costumes.costumes[
            sprite_builder.costumes.costumes_list[0]]
        width, height, raw_image = costume.get_raw_image()
        bitmap = wx.BitmapFromBufferRGBA(width, height, raw_image)
        image = wx.ImageFromBitmap(bitmap)
        image_scaled = image.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        self.il.Add(sprite_bitmap)
        index = self.InsertImageStringItem(0, character.name, 0)
        self.resources.cast.set_index(character.name, index)
