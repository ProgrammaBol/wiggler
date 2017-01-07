import wx


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
            pass
        elif event.notice == 'del_costume':
            pass
        elif event.notice == 'add_sheet':
            pass
        elif event.notice == 'del_sheet':
            pass
        elif event.notice == 'add_image':
            pass
        elif event.notice == 'del_image':
            pass
        elif event.notice == 'add_character':
            pass
        elif event.notice == 'del_character':
            pass
        elif event.notice == 'add_animation':
            pass
        elif event.notice == 'del_animation':
            pass
        elif event.notice == 'add_sprite':
            pass
        elif event.notice == 'remove_sprite':
            pass
        event.Skip()

    def change_background(self):
        dlg = ChangeBackgroundDialog(self.parent)
        res = dlg.ShowModal()
        if res == wx.ID_OK:
            back_type = dlg.back_type.GetValue()
            back_spec = dlg.back_spec.GetValue()
            self.resources.change_default_background(back_type, back_spec)
        dlg.Destroy()


class ChangeBackgroundDialog(wx.Dialog):

    def __init__(self, parent):
        wx.Dialog.__init__(self, parent, wx.ID_ANY,
                           "background", size=(300, 300))

        boxglobal = wx.BoxSizer(wx.VERTICAL)
        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert background type'), 0,
                     wx.ALL, 5)
        self.back_type = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.back_type, -1, wx.Right, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, 0, 'Insert background specs'), 0,
                     wx.ALL, 5)
        self.back_spec = wx.TextCtrl(self, 0, '')
        boxdown2.Add(self.back_spec, -1, wx.Right, 5)

        boxdown4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown4, 1, wx.EXPAND, 5)

        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onOk(self, e):
        self.EndModal(wx.ID_OK)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)
