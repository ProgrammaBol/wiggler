import wx
from wiggler.core.resources import Resources


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

    def __init__(self, *args, **kwargs):
        for sheetname in self.resources.sheets.keys():
            Sheet = self.resources.load_resource('sheets', sheetname)
            self.AddItem(Sheet)


class ResourceDialog(wx.Dialog):

    def __init__(self, parent, id, title):
        wx.Dialog.__init__(self, parent, id, title, size=(300, 380))
        self.settings = {}

        wx.StaticText(self, -1, 'Select source sheet file:', (5, 5))
        self.lc = wx.ListCtrl(self, -1, pos=(5, 25), size=(284, 150),
                              style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.resources = Resources()
        self.lc.InsertColumn(0, 'Sheet file')
        self.lc.SetColumnWidth(0, 267)
        for sheetname in self.resources.sheets.keys():
            num_items = self.lc.GetItemCount()
            self.lc.InsertStringItem(num_items, sheetname)

        wx.StaticText(self, -1, 'Insert costume name:', (20, 190))
        self.name = wx.TextCtrl(self, -1, '', (160, 187))

        wx.StaticBox(self, -1, 'Define costume RECT', (5, 227), size=(284, 90))
        wx.StaticText(self, -1, 'Origin point:', (15, 253))
        wx.StaticText(self, -1, 'X:', (136, 253))
        self.originx = wx.SpinCtrl(self, -1, '0', (150, 250), (55, -1), min=0,
                                   max=4000)
        wx.StaticText(self, -1, 'Y:', (216, 253))
        self.originy = wx.SpinCtrl(self, -1, '0', (230, 250), (55, -1), min=0,
                                   max=4000)

        wx.StaticText(self, -1, 'Side size:', (15, 283))
        wx.StaticText(self, -1, 'X:', (136, 283))
        self.sidex = wx.SpinCtrl(self, -1, '0', (150, 280), (55, -1), min=0,
                                 max=4000)
        wx.StaticText(self, -1, 'Y:', (216, 283))
        self.sidey = wx.SpinCtrl(self, -1, '0', (230, 280), (55, -1), min=0,
                                 max=4000)

        self.button_ok = wx.Button(self, 1, 'Ok', (170, 320), (60, -1))
        self.button_cancel = wx.Button(self, 2, 'Cancel', (230, 320), (60, -1))
        self.button_ok.Bind(wx.EVT_BUTTON, self.onOk)
        self.button_cancel.Bind(wx.EVT_BUTTON, self.onCancel)

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
            self.settings['sheet'] = out2['abs_path'].rpartition('\\')[2]
            self.EndModal(wx.ID_OK)

    def GetSettings(self):
        return self.settings
