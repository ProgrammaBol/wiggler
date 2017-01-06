import wx
import os
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

        boxglobal = wx.BoxSizer(wx.VERTICAL)

        boxup = wx.BoxSizer(wx.VERTICAL)
        self.lc = wx.ListCtrl(self, -1, style=wx.LC_REPORT |
                              wx.LC_SINGLE_SEL)
        self.resources = Resources()
        self.lc.InsertColumn(0, 'Sheet file', width=wx.LIST_AUTOSIZE_USEHEADER)
        for sheetname in self.resources.sheets.keys():
            num_items = self.lc.GetItemCount()
            self.lc.InsertStringItem(num_items, sheetname)
        boxup.Add(wx.StaticText(self, 0, 'Select source sheet file:'), 0,
                  wx.ALL, 5)
        boxup.Add(self.lc, 0, wx.ALL, 5)

        boxdown = wx.BoxSizer(wx.VERTICAL)

        boxdown1 = wx.BoxSizer(wx.HORIZONTAL)
        boxdown1.Add(wx.StaticText(self, 0, 'Insert costume name:'), 0,
                     wx.ALL, 5)
        self.name = wx.TextCtrl(self, 0, '')
        boxdown1.Add(self.name, -1, wx.ALL, 5)

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
