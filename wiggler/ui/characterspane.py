import wx

import wiggler.ui.dialogs as dialogs


class CharactersPane(wx.ListCtrl):

    def __init__(self, parent, resources, events):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_ICON)
        self.events = events
        self.resources = resources
        self.il = wx.ImageList(30, 30, True)
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.events.subscribe(self, ['projload', 'load_character',
                                     'add_sprite_costume',
                                     'del_sprite_costume',
                                     'add_char_sprite',
                                     'del_char_sprite',
                                     'add_char_proj',
                                     'del_char_proj'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_select)

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'loadchar':
            self.load_character(name=event.data.charname)
        elif event.notice == 'charadded':
            self.new_character(event.data.charname, event.data.chardef)
        elif event.notice == 'add_char_sprite':
            self.add_char_sprite()
        elif event.notice == 'del_char_sprite':
            self.del_char_sprite()
        elif event.notice == 'add_sprite_costume':
            self.add_sprite_costume()
        elif event.notice == 'del_sprite_costume':
            self.del_sprite_costume()
        elif event.notice == 'add_char_proj':
            self.add_character()
        elif event.notice == 'del_char_proj':
            self.del_character()
        event.Skip()

    def add_sprite_costume(self):
        dia = dialogs.AddCostumeToSpriteDialog(None, -1,
                                               "Add costume to sprite",
                                               self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            character = self.resources.cast.get_character()
            sprite = character.get_sprite_builder()
            sprite.add_costume(self.settings['costume'])

        dia.Destroy()

    def del_sprite_costume(self):
        character = self.resources.cast.get_character()
        sprite = character.get_sprite_builder()
        sprite_name = sprite.name
        dia = dialogs.DelCostumeFromSpriteDialog(None, -1,
                                                 "Remove costume from sprite",
                                                 self.resources, sprite_name)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            sprite.del_costume(self.settings['costume'])

        dia.Destroy()

    def add_char_sprite(self):
        dia = dialogs.AddSpriteToCharDialog(None, -1,
                                            "Add sprite to character",
                                            self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            base_name = self.settings.get('base', None)
            if base_name is None:
                definition = {
                    'name': self.settings['sprite'],
                    'base_class': 'MovingSprite',
                    'animations': {},
                    'costumes': {},
                    'sounds': {},
                    'user_code': {},
                }
                self.resources.add_resource('sprites', self.settings['sprite'],
                                            definition)
            else:
                self.resources.clone_resource('sprite', base_name,
                                              self.settings['sprite'])
            character = self.resources.cast.get_character()
            character.add_sprite(self.settings['sprite'])

        dia.Destroy()

    def del_char_sprite(self):
        character = self.resources.cast.get_character()
        char_name = character.name
        dia = dialogs.DelSpriteFromCharDialog(None, -1,
                                              "Delete sprite from character",
                                              self.resources, char_name)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            character.remove_sprite(self.settings['sprite'])

        dia.Destroy()

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

    def add_character(self):
        dia = dialogs.AddCharToProjDialog(None, -1,
                                          "Add character to project",
                                          self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            base_name = self.settings.get('base', None)
            char_name = self.settings['character']
            if base_name is None:
                chardef = {
                    'sprites': {}
                }
                self.resources.add_resource('character',
                                            self.settings['character'],
                                            chardef)
            else:
                chardef = self.resources.clone_resource('characters',
                                                        base_name,
                                                        char_name)
            character = self.resources.cast.add_character(char_name, chardef)
            self.load_character(character=character)

        dia.Destroy()

    def del_character(self):
        character = self.resources.cast.get_character()
        char_name = character.name
        dia = dialogs.DelCharFromProjDialog(None, -1,
                                            "Delete character from project",
                                            self.resources, char_name)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            index = self.resources.cast.get_index(self.settings['character'])
            self.DeleteItem(index)
            self.resources.cas.del_character(self.settings['character'])

        dia.Destroy()

    def load_character(self, name='', character=None):
        if character is None:
            character = self.resources.cast.get_character(name=name)
        sprite_builder = character.get_sprite_builder(index=0)
        costume = sprite_builder.costumes.costumes[
            sprite_builder.costumes.costumes_list[0]]
        self.events.send('spriteloaded', costume=costume)
        width, height, raw_image = costume.get_raw_image()
        bitmap = wx.BitmapFromBufferRGBA(width, height, raw_image)
        image = wx.ImageFromBitmap(bitmap)
        image_scaled = image.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        self.il.Add(sprite_bitmap)
        index = self.GetItemCount()
        index = self.InsertImageStringItem(index, character.name, 0)
        self.resources.cast.set_index(character.name, index)
