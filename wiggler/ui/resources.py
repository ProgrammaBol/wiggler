import wx

import wiggler.ui.dialogs as dialogs


class ResourceManager(wx.Control):

    def __init__(self, parent, resources, events):
        wx.Control.__init__(self, parent)
        self.parent = parent
        self.events = events
        self.resources = resources
        self.events.subscribe(self, ['add_costume', 'del_costume',
                                     'add_character', 'del_character',
                                     'add_sheet', 'del_sheet',
                                     'add_image', 'del_image',
                                     'add_sprite', 'del_sprite',
                                     'add_animation', 'del_animation',
                                     'change_background'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)

    def notice_handler(self, event):
        if event.notice == 'change_background':
            self.change_background()
        elif event.notice == 'add_costume':
            self.add_costume()
        elif event.notice == 'del_costume':
            self.del_costume()
        elif event.notice == 'add_sheet':
            self.add_sheet()
        elif event.notice == 'del_sheet':
            self.del_sheet()
        elif event.notice == 'add_image':
            pass
        elif event.notice == 'del_image':
            pass
        elif event.notice == 'add_character':
            self.add_character()
        elif event.notice == 'del_character':
            self.del_character()
        elif event.notice == 'add_animation':
            pass
        elif event.notice == 'del_animation':
            pass
        elif event.notice == 'add_sprite':
            self.add_sprite()
        elif event.notice == 'del_sprite':
            self.del_sprite()
        event.Skip()

    def change_background(self):
        dlg = dialogs.ChangeBackgroundDialog(self.parent)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            back_type = dlg.back_type.GetValue()
            back_spec = dlg.back_spec.GetValue()
            self.resources.change_default_background(back_type, back_spec)
        dlg.Destroy()

    def add_sheet(self):
        # definition_fields = Factory_sheet.definition_fields
        # dialog with definition fields, source file with browse button
        # resource with same name , overwrite ?
        filename = dialogs.open_sheet(self.parent)
        if filename is not None:
            dia = dialogs.AddSheetDialog(None, -1, "Insert sheet details",
                                         self.resources)
            result = dia.ShowModal()
            if result == wx.ID_OK:
                self.settings = dia.GetSettings()
                try:
                    self.resources.add_resource(
                        'sheets', self.settings['name'],
                        {'colorkey': self.settings['colorkey'],
                         'abs_path': filename})
                except ValueError as e:
                    wx.MessageBox(str(e), "Error",
                                  wx.OK | wx.ICON_INFORMATION)
            dia.Destroy()
        return True

    def del_sheet(self):
        # LISTCTR with very large icons ?
        # use resources.find_deps
        # print self.resources.find_deps('sheets', 'master')
        # name = 'testsheet'
        # self.resources.remove_resource('sheets', name)
        # and everything associated to IT!!!
        dia = dialogs.DelSheetDialog(None, -1, "Delete sheet",
                                     self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('sheets',
                                              self.settings['sheet']):
                for elem in x:
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception as e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('sheets',
                                               self.settings['sheet'])
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_costume(self):
        # dialog with definitions and a area selection on the sheet
        dia = dialogs.AddCostumeDialog(None, -1, "Add a new costume",
                                       self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            # print self.settings['name'], self.settings['rect'], \
            #    self.settings['sheet']
            try:
                self.resources.add_resource(
                    'costumes', self.settings['name'],
                    {'name': self.settings['name'],
                     'sheet': self.settings['sheet'],
                     'rect': self.settings['rect']})
            except ValueError as e:
                wx.MessageBox(str(e), "Error",
                              wx.OK | wx.ICON_INFORMATION)
        dia.Destroy()
        return True

    def del_costume(self):
        # LISTCTRL with large icons
        dia = dialogs.DelCostumeDialog(None, -1, "Delete costume",
                                       self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('costumes',
                                              self.settings['costume']):
                for elem in x:
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception as e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('costumes',
                                               self.settings['costume'])
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_sprite(self):
        # dialog with definition, select from existing costumes,
        # animations, sounds...
        # or add empty
        dia = dialogs.AddSpriteDialog(None, -1, "Add a new sprite",
                                      self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            try:
                self.resources.add_resource('sprites', self.settings['name'],
                                            {'name': self.settings['name'],
                                             'base_class': self.settings
                                             ['base_class'],
                                             'costumes': self.settings
                                             ['costumes'],
                                             'animations': [],
                                             'sounds': [],
                                             'self_sufficiency': 0,
                                             'user_code': {'__init__': ''}})
            except ValueError as e:
                wx.MessageBox(str(e), "Error",
                              wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def del_sprite(self):
        # LISTCTRK with name + sprite definition
        dia = dialogs.DelSpriteDialog(None, -1, "Delete a sprite",
                                      self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('sprites',
                                              self.settings['sprite']):
                for elem in x:
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception as e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('sprites',
                                               self.settings['sprite'])
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_character(self):
        # dialog with definition, select from existing sprites or add empty
        dia = dialogs.AddCharacterDialog(None, -1, "Add a new character",
                                         self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            try:
                self.resources.add_resource('characters',
                                            self.settings['name'],
                                            {'sprites': []})
            except ValueError as e:
                wx.MessageBox(str(e), "Error",
                              wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def del_character(self):
        # LISTCTRK with name + sprite definition
        dia = dialogs.DelCharacterDialog(None, -1, "Delete character",
                                         self.resources)
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('characters',
                                              self.settings['character']):
                for elem in x:
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception as e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('characters',
                                               self.settings['character'])
            except Exception as e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_animation(self):
        # dialog similar to add_costume but for every frame
        pass

    def del_animation(self):
        # listctrl with animated gifs ?
        pass
