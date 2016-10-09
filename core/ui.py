import wx
import wx.py

from editor import TextEditor
from stage import Stage

class RootWindow(wx.Frame):

    def __init__(self):
        #super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self,None, -1, "Menu")
        menu_exit_id = wx.NewId()
        self.SetMinSize((100,100))

        file_menu = wx.Menu()
        file_menu.Append(menu_exit_id, "Exit", "Exit")

        wx.EVT_MENU(self, menu_exit_id, self.exit)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        self.tab = wx.Notebook(self, -1)
        self.editor = TextEditor(self.tab, wx.ID_ANY)
        self.tab.AddPage(self.editor, "Codice")
        self.tab.AddPage(wx.StaticText(self.tab, -1, "ciccio"), "Costumi")
        self.sprites = wx.ListCtrl(self)
        self.sprites.InsertImageItem(0,0)
        self.sprites.InsertImageItem(1,0)
        self.sprites.InsertImageItem(2,0)
        self.tools = wx.ToolBar(self, -1, size = (10, 40))
        self.shell = wx.py.crust.Crust(parent=self)
        self.shell.Show()
        self.basket_classes = wx.ListCtrl(self, wx.ID_ANY, size = (200,300), style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0,"Classes")
        self.basket_classes.InsertStringItem(0, "Movement")
        self.basket_classes.InsertStringItem(1, "Stage")
        self.basket_functions = wx.ListCtrl(self, wx.ID_ANY, size = (200,300))
        sizer = wx.GridBagSizer()
        self.stage = Stage(self, wx.ID_ANY, size = (300,300))
        self.box = wx.StaticBox(self, wx.ID_ANY, size = (300,300))
        sizer.Add(self.tools, (0,1), span=(1,3),flag=wx.EXPAND)
        sizer.Add(self.stage, (1,0))
        sizer.Add(self.basket_classes, (1,1), span=(1,1))
        sizer.Add(self.basket_functions, (2,1), span=(1,1), flag=wx.EXPAND)
        sizer.Add(self.tab, (1,2), span=(2,1), flag=wx.EXPAND)
        sizer.Add(self.sprites, (2,0), flag=wx.EXPAND)
        sizer.Add(self.shell, (3,0), span=(1,3),  flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)
        self.Layout()

    def exit(self, event):
        self.Close(True)
