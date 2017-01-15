import wx
import os


def unsaved_warning(parent):
    if wx.MessageBox("Current content has not been saved! Proceed?",
                     "Please confirm",
                     wx.ICON_QUESTION | wx.YES_NO, parent) == wx.NO:
        return False
    return True


def open_project(parent):
    open_file = wx.FileDialog(parent, "Open wiggler project", "", "",
                              "wig files (*.wig)|*.wig",
                              wx.FD_OPEN | wx.FD_FILE_MUST_EXIST)
    if open_file.ShowModal() == wx.ID_CANCEL:
        return None
    return open_file.GetPath()


def save_project(parent):
    save_file = wx.FileDialog(parent, "Save wiggler project", "", "",
                              "wig files (*.wig)|*.wig",
                              wx.FD_SAVE | wx.FD_OVERWRITE_PROMPT)
    if save_file.ShowModal() == wx.ID_CANCEL:
        return None
    return save_file.GetPath()


def open_sheet(parent):
    options = wx.FD_OPEN | wx.FD_FILE_MUST_EXIST | wx.FD_PREVIEW
    open_file = wx.FileDialog(parent, "Select sheet file", "", "",
                              "", options)
    if open_file.ShowModal() == wx.ID_CANCEL:
        return None
    return open_file.GetPath()


class SelectSheet(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sheet file', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sheets.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectCostume(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Costume name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.costumes.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectSpriteCostume(wx.ListCtrl):

    def __init__(self, parent, id, resources, sprite_name, single_sel=False):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Costume name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sprites[sprite_name]['costumes']:
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectSprite(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sprite name', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sprites.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectCharacter(wx.ListCtrl):

    def __init__(self, parent, id, resources, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Character name',
                          width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.characters.keys():
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class SelectCharacterSprite(wx.ListCtrl):

    def __init__(self, parent, id, resources, char_name, single_sel=True):
        if single_sel is True:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT |
                                 wx.LC_SINGLE_SEL)
        else:
            wx.ListCtrl.__init__(self, parent, id, style=wx.LC_REPORT)

        self.resources = resources
        self.InsertColumn(0, 'Sprite name',
                          width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.characters[char_name]['sprites']:
            num_items = self.GetItemCount()
            self.InsertStringItem(num_items, sheetname)


class AddSheetDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(270, 180))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Define sheet name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        box2.Add(wx.StaticText(self, -1, 'Set colorkey:'), 0,
                 wx.ALL | wx.ALIGN_BOTTOM, 5)

        box3 = wx.GridSizer(1, 6, 0, 0)
        box3.Add(wx.StaticText(self, -1, 'R:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.rvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.rvalue, 0, 0, 5)
        box3.Add(wx.StaticText(self, -1, 'G:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.gvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.gvalue, 0, 0, 5)
        box3.Add(wx.StaticText(self, -1, 'B:'), 0,
                 wx.ALL | wx.ALIGN_RIGHT, 5)
        self.bvalue = wx.SpinCtrl(self, -1, '0', size=wx.Size(48, -1),
                                  min=0, max=255)
        box3.Add(self.bvalue, 0, 0, 5)

        box4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        box4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        box4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(box1, 1, wx.EXPAND, 5)
        boxglobal.Add(box2, 1, wx.EXPAND, 5)
        boxglobal.Add(box3, 1, wx.EXPAND | wx.ALL, 5)
        boxglobal.Add(box4, 1, wx.EXPAND, 5)

        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['colorkey'] = str(self.rvalue.GetValue()) + \
            ',' + str(self.gvalue.GetValue()) + \
            ',' + str(self.bvalue.GetValue())
        if self.settings['name'] == '':
            wx.MessageBox("Insert a name", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelSheetDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSheet(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a sheet to remove:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a sheet", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sheet'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddCostumeDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 380))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)

        self.lc = SelectSheet(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select source sheet file:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 0, wx.ALL, 5)

        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert costume name:'), 0,
                     wx.ALL, 5)
        self.name = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.name, -1, wx.RIGHT, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, -1, 'Define costume RECT:'), 0,
                     wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown3 = wx.GridSizer(2, 5, 0, 0)
        boxdown3.Add(wx.StaticText(self, -1, 'Origin point:'), 0, wx.ALL, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'X:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.originx = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                   min=0, max=4000)
        boxdown3.Add(self.originx, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Y:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.originy = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                   min=0, max=4000)
        boxdown3.Add(self.originy, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Side size:'), 0, wx.ALL, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'X:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.sidex = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                 min=0, max=4000)
        boxdown3.Add(self.sidex, 0, 0, 5)
        boxdown3.Add(wx.StaticText(self, -1, 'Y:'), 0,
                     wx.ALL | wx.ALIGN_RIGHT, 5)
        self.sidey = wx.SpinCtrl(self, -1, '0', size=wx.Size(55, -1),
                                 min=0, max=4000)
        boxdown3.Add(self.sidey, 0, 0, 5)

        boxdown4 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown4.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown4.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown3, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown4, 1, wx.EXPAND, 5)

        boxglobal.Add(boxup, 1, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['rect'] = str(self.originx.GetValue()) + \
            ', ' + str(self.originy.GetValue()) + \
            ', ' + str(self.sidex.GetValue()) + \
            ', ' + str(self.sidey.GetValue())
        sel = self.lc.GetNextSelected(-1)
        if self.settings['name'] == '' or \
                self.settings['rect'] == '0, 0, 0, 0' or \
                sel == -1:
            wx.MessageBox("Values must not be null", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.sheets[out]
            self.settings['sheet'] = os.path.basename(out2['abs_path'])
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddCostumeToSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCostume(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a costume to add to sprite:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelCostumeFromSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, sprite_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSpriteCostume(self, -1, self.resources, sprite_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a costume to remove from sprite:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelCostumeDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCostume(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a costume to remove:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a costume", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            out2 = self.resources.costumes[out]
            self.settings['costume'] = out2['name']
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 330))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)

        self.lc = SelectCostume(self, -1, self.resources, False)
        boxup.Add(wx.StaticText(self, 0, 'Select costumes:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 0, wx.ALL, 5)

        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert sprite name:'), 0,
                     wx.ALL, 5)
        self.name = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.name, -1, wx.RIGHT, 5)

        boxdown2 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown2.Add(wx.StaticText(self, 0, 'Insert base class name:'), 0,
                     wx.ALL, 5)
        self.classname = wx.TextCtrl(self, 0, '')
        boxdown2.Add(self.classname, -1, wx.RIGHT, 5)

        boxdown3 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown3.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown3.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxdown.Add(boxdown1, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown2, 1, wx.EXPAND, 5)
        boxdown.Add(boxdown3, 1, wx.EXPAND, 5)

        boxglobal.Add(boxup, 1, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        self.settings['base_class'] = self.classname.GetValue()
        sel = self.lc.GetNextSelected(-1)
        if self.settings['name'] == '' or \
                self.settings['base_class'] == '' or \
                sel == -1:
            wx.MessageBox("Values must not be null", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = []
            out.append(self.lc.GetItemText(sel, 0))
            for i in range(0, self.lc.GetSelectedItemCount() - 1):
                sel = self.lc.GetNextSelected(sel)
                out.append(self.lc.GetItemText(sel, 0))
            self.settings['costumes'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddCharToProjDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacter(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a character to copy from:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Specify character name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(box1, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            pass
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['base'] = out
            self.EndModal(wx.ID_OK)
        self.settings['character'] = self.name.GetValue()

    def GetSettings(self):
        return self.settings


class DelCharFromProjDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, char_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacterSprite(self, -1, self.resources, char_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a chracter to remove from project:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a character", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['character'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddSpriteToCharDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSprite(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a sprite to copy from:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Specify sprite name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(box1, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            pass
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['base'] = out
            self.EndModal(wx.ID_OK)
        self.settings['sprite'] = self.name.GetValue()

    def GetSettings(self):
        return self.settings


class DelSpriteFromCharDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources, char_name):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacterSprite(self, -1, self.resources, char_name)
        boxup.Add(wx.StaticText(self, 0,
                                'Select a sprite to remove from character:'),
                  0, wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a sprite", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sprite'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelSpriteDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectSprite(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a sprite to remove:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a sprite", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['sprite'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class AddCharacterDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 100))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        box1 = wx.BoxSizer(wx.HORIZONTAL)
        box1.Add(wx.StaticText(self, 0, 'Define character name:'), 0,
                 wx.ALL | wx.ALIGN_CENTER, 5)
        self.name = wx.TextCtrl(self, 0, '')
        box1.Add(self.name, -1, wx.RIGHT | wx.ALIGN_CENTER, 5)

        box2 = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        box2.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        box2.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(box1, 1, wx.EXPAND, 5)
        boxglobal.Add(box2, 1, wx.EXPAND, 5)

        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        self.settings['name'] = self.name.GetValue()
        if self.settings['name'] == '':
            wx.MessageBox("Insert a name", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


class DelCharacterDialog(wx.Dialog):

    def __init__(self, parent, id, title, resources):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 300))
        self.settings = {}
        self.resources = resources

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = SelectCharacter(self, -1, self.resources)
        boxup.Add(wx.StaticText(self, 0, 'Select a character to remove:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 1, wx.ALL | wx.EXPAND, 5)

        boxdown = wx.BoxSizer(wx.HORIZONTAL)
        self.button_ok = wx.Button(self, 1, 'Ok')
        self.button_cancel = wx.Button(self, 2, 'Cancel')
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)
        boxdown.Add(self.button_ok, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)
        boxdown.Add(self.button_cancel, -1, wx.ALL | wx.ALIGN_BOTTOM, 5)

        boxglobal.Add(boxup, 5, wx.EXPAND, 5)
        boxglobal.Add(boxdown, 1, wx.EXPAND, 5)
        self.SetSizer(boxglobal)

    def onCancel(self, e):
        self.EndModal(wx.ID_CANCEL)

    def onOk(self, e):
        sel = self.lc.GetNextSelected(-1)
        if sel == -1:
            wx.MessageBox("Select a character", "Error",
                          wx.OK | wx.ICON_INFORMATION)
        else:
            out = self.lc.GetItemText(sel, 0)
            self.settings['character'] = out
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings


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
