import wx
import wx.py

import wiggler.ui.dialogs as dialogs

from wiggler.ui.characterspane import CharactersPane
from wiggler.ui.costumespane import CostumesPane
from wiggler.ui.code_pane import CodePane
from wiggler.ui.menubar import MenuBar
from wiggler.ui.resources import ResourceManager
from wiggler.ui.spritespane import SpritesPane
from wiggler.ui.stagepane import StagePane
from wiggler.ui.toolbar import ToolBar
from wiggler.ui.tracebackpane import TracebackPane


class RootWindow(wx.Frame):

    def __init__(self, resources, events, project):
        wx.Frame.__init__(self, None, -1, "Menu")
        self.events = events
        self.project = project
        self.resources = resources
        self.resourcemanager = ResourceManager(self, self.resources,
                                               self.events)
        self.SetMinSize((100, 100))
        self.stage_resolution = self.resources.conf['stage_resolution']
        self.stage_pane = StagePane(
            self, wx.ID_ANY, self.resources, self.events,
            size=self.stage_resolution)

        self.menubar = MenuBar(self.events)
        self.Bind(wx.EVT_MENU, self.menubar.notice_dispatcher)
        self.toolbar = ToolBar(self.resources, self, self.events)

        self.code_pane = CodePane(self, self.resources, self.events)
        self.characters_pane = CharactersPane(
            self, self.resources, self.events)
        self.costumes_pane = CostumesPane(
            self, self.resources, self.events)
        self.sprites_pane = SpritesPane(self, self.resources, self.events)
        self.traceback = TracebackPane(self, self.resources, self.events)
        self.setup_basket_classes()
        self.setup_basket_members()

        self.statusbar = self.CreateStatusBar(2)
        self.statusbar.SetStatusText("Self-Sufficiency Level: 0")
        self.SetMenuBar(self.menubar)

        self.widget_placement()
        self.Layout()

        self.events.subscribe(self, ['projnew', 'projopen', 'projsave',
                                     'projsaveas', 'testload', 'exit',
                                     'modified', 'addcostume'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)

    def notice_handler(self, event):
        if event.notice == 'projnew':
            self.new_project()
        elif event.notice == 'projopen':
            self.open_project()
        elif event.notice == 'projsave':
            self.save_project()
        elif event.notice == 'projsaveas':
            self.save_project_as()
        elif event.notice == 'testload':
            self.project.load("tests/fixtures/test_project.wig")
        elif event.notice == 'modified':
            self.project.needs_save = True
        elif event.notice == 'exit':
            self.close()
        elif event.notice == 'addcostume':
            self.add_costume(event)
        event.Skip()

    def widget_placement(self):
        sizer = wx.GridBagSizer(hgap=1, vgap=1)
        sizer.Add(self.stage_pane, (0, 0))
        sizer.Add(self.basket_classes, (0, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.basket_functions, (1, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.costumes_pane, (0, 2), span=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.code_pane, (0, 3), span=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.characters_pane, (1, 0), flag=wx.EXPAND)
        sizer.Add(self.traceback, (2, 0), span=(1, 4), flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(3)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def setup_basket_members(self):
        self.basket_functions = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_REPORT)
        self.basket_functions.InsertColumn(0, "Available attributes",
                                           width=wx.LIST_AUTOSIZE_USEHEADER)

    def setup_basket_classes(self):
        self.basket_classes = wx.ListCtrl(
            self, wx.ID_ANY, style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0, "Available Classes",
                                         width=wx.LIST_AUTOSIZE_USEHEADER)
        self.basket_classes.InsertStringItem(0, "MovingSprite")
        self.basket_classes.InsertStringItem(1, "StaticSprite")

    def load(self, event):
        # FIXME get filenam from event
        filename = None
        self.project.load(filename)

    def close(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        self.resources.cleanup()
        self.Close(True)

    def open_project(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        filename = dialogs.open_project(self)
        if filename is not None:
            self.project.load(filename)

    def save_project(self):
        if self.project.abspath is None:
            self.save_project_as()
        else:
            self.project.save(self.project.abspath)

    def save_project_as(self):
        filename = dialogs.save_project(self)
        if filename is not None:
            self.project.save(filename)

    def new_project(self):
        # if self.project.needs_save:
        if True:
            proceed = dialogs.unsaved_warning(self)
            if not proceed:
                return
        self.project.new()

    def add_costume(self, event):
        self.toolbar.add_costume(event)
