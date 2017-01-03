import wx


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

    def __init__(self, *args, **kw):
        super(SelectSheet, self).__init__(*args, **kw)

        self.InitUI()
        self.SetSize((250, 200))
        self.SetTitle("Select sheet")

    def InitUI(self):
        pnl = wx.Panel(self)
        vbox = wx.BoxSizer(wx.VERTICAL)

        sb = wx.StaticBox(pnl, label='Sheets')
        sbs = wx.StaticBoxSizer(sb, orient=wx.VERTICAL)
        sbs.Add(wx.ListCtrl())

        # --- resource options ---
        hbox1 = wx.BoxSizer(wx.HORIZONTAL)
        hbox1.Add(wx.RadioButton(pnl, label='name'))
        hbox1.Add(wx.TextCtrl(pnl), flag=wx.LEFT, border=5)
        sbs.Add(hbox1)

        pnl.SetSizer(sbs)

        hbox2 = wx.BoxSizer(wx.HORIZONTAL)
        okButton = wx.Button(self, label='Ok')
        closeButton = wx.Button(self, label='Close')
        hbox2.Add(okButton)
        hbox2.Add(closeButton, flag=wx.LEFT, border=5)

        vbox.Add(pnl, proportion=1,
            flag=wx.ALL|wx.EXPAND, border=5)
        vbox.Add(hbox2,
            flag=wx.ALIGN_CENTER|wx.TOP|wx.BOTTOM, border=10)

        self.SetSizer(vbox)

        okButton.Bind(wx.EVT_BUTTON, self.OnClose)
        closeButton.Bind(wx.EVT_BUTTON, self.OnClose)

    def OnClose(self, e):
        self.Destroy()

    def GetValue():
        retval['name'] = gettextname
        retval['rect'] = getrectvalue

