import wx

import wiggler.ui.dialogs as dialogs


class ToolBar(object):

    def __init__(self, resources, parent, events):
        self.resources = resources
        self.width = 30
        self.height = 30
        self.events = events
        self.parent = parent
        self.tools = parent.CreateToolBar()
        self.add_button('play', 'Play', self.play)
        self.add_button('stop', 'Stop', self.stop)
        self.add_button('incss', 'incss', self.incss)
        self.add_button('decss', 'decss', self.decss)
        self.add_button('incss', 'add sheet', self.add_sheet)
        self.add_button('decss', 'del sheet', self.del_sheet)
        self.add_button('incss', 'add costume', self.add_costume)
        self.add_button('decss', 'add costume', self.del_costume)
        self.add_button('incss', 'add sprite', self.decss)
        self.add_button('incss', 'add character', self.decss)
        self.tools.Realize()

    def add_button(self, bitmap_name, label_text, action_callable):
        """Creates a button and add it to a toolbar

           Arguments:

           toolbar         -- toolbar to attach the button into
           image_path      -- path of the png image used to decorate the button
           label_text      -- text of the button label
           action_callable -- function or method to call when button is pushed

           Keyword arguments:

           width           -- button width in pixel (default: 30 => 30px)
           height          -- button height in pixel (default: 30 => 30px)

           Returns:
           none
        """
        UIimage = self.resources.load_ui_images(bitmap_name)
        image = UIimage.get_image(scale=(self.width, self.height))
        tool = self.tools.AddLabelTool(wx.ID_ANY, label_text, image)
        self.parent.Bind(wx.EVT_TOOL, action_callable, tool)

    def add_sheet(self, event):
        # definition_fields = Factory_sheet.definition_fields
        # dialog with definition fields, source file with browse button
        # resource with same name , overwrite ?
        definition = {'name': 'testsheet',
                      'colorkey': "0,0,0",
                      'modified': True}
        filename = dialogs.open_sheet(self.parent)
        if filename is not None:
            self.resources.add_resource('sheets', definition['name'],
                                        definition, source_file=filename)

        dlg = MyDialog()
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            print dlg.comboBox1.GetValue()
        dlg.Destroy()

    def del_sheet(self, event):
        # LISTCTR with very large icons ?
        # use resources.find_deps
        # print self.resources.find_deps('sheets', 'master')
        # name = 'testsheet'
        # self.resources.remove_resource('sheets', name)
        # and everything associated to IT!!!
        dia = dialogs.DelSheetDialog(None, -1, "Delete sheet")
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('sheets',
                                              self.settings['sheet']):
                for elem in x:
                    print elem[0], elem[1]
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception, e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('sheets',
                                               self.settings['sheet'])
            except Exception, e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_costume(self, event):
        # dialog with definitions and a area selection on the sheet
        dia = dialogs.AddResourceDialog(None, -1, "Add costume")
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            # print self.settings['name'], self.settings['rect'], \
            #    self.settings['sheet']
            try:
                out = self.resources.add_resource(
                    'costumes', self.settings['name'],
                    {'name': self.settings['name'],
                     'sheet': self.settings['sheet'],
                     'rect': self.settings['rect']})
            except ValueError, e:
                wx.MessageBox(str(e), "Error",
                              wx.OK | wx.ICON_INFORMATION)
        dia.Destroy()
        return True

    def del_costume(self, event):
        # LISTCTRL with large icons
        dia = dialogs.DelCostumeDialog(None, -1, "Delete costume")
        result = dia.ShowModal()
        if result == wx.ID_OK:
            self.settings = dia.GetSettings()
            for x in self.resources.find_deps('costumes',
                                              self.settings['costume']):
                for elem in x:
                    try:
                        self.resources.remove_resource(elem[0], elem[1])
                    except Exception, e:
                        wx.MessageBox(str(e), "Error", wx.OK |
                                      wx.ICON_INFORMATION)

            try:
                self.resources.remove_resource('costumes',
                                               self.settings['costume'])
            except Exception, e:
                wx.MessageBox(str(e), "Error", wx.OK | wx.ICON_INFORMATION)

        dia.Destroy()
        return True

    def add_sprite(self, event):
        # dialog with definition, select from existing costumes,
        # animations, sounds...
        # or add empty
        pass

    def del_sprite(self, event):
        # LISTCTRK with name + sprite definition
        pass

    def add_character(self, event):
        # dialog with definition, select from existing sprites or add empty
        pass

    def del_character(self, event):
        # LISTCTRK with name + sprite definition
        pass

    def add_animation(self, event):
        # dialog similar to add_costume but for every frame
        pass

    def del_animation(self, event):
        # listctrl with animated gifs ?
        pass

    def play(self, event):
        self.events.send('preplay')
        self.events.send('play')

    def stop(self, event):
        self.events.send('stop')

    # Self sufficiency is per-character attribute
    def decss(self, event):
        pass
        # self.selfsufficiency -= 1
        # self.statusbar.SetStatusText(
        #    "Self-Sufficiency Level: %d" % self.selfsufficiency)

    def incss(self, event):
        pass
        # self.selfsufficiency += 1
        # self.statusbar.SetStatusText(
        #    "Self-Sufficiency Level: %d" % self.selfsufficiency)
