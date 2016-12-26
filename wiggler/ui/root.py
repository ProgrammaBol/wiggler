import wx
import wx.py
import sys
import gettext

from wiggler.core.project import Project
from wiggler.core.events import Events
from wiggler.ui.stagepane import StagePane
from wiggler.ui.toolbar import ToolBar
from wiggler.ui.menubarfactory import MenuBarFactory
from wiggler.ui.characterspane import CharactersPane
from wiggler.ui.code_pane import CodePane
from wiggler.ui.spritespane import SpritesPane

kwargs = {}
if sys.version_info[0] > 3:
    # In Python 2, ensure that the _() that gets installed into built-ins
    # always returns unicodes.  This matches the default behavior under
    # Python 3, although that keyword argument is not present in the
    # Python 3 API.
    kwargs['unicode'] = True
gettext.install("wiggler", **kwargs)


class RootWindow(wx.Frame):

    def __init__(self, resources):
        # super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self, None, -1, "Menu")
        self.events = Events()
        self.resources = resources
        self.SetMinSize((100, 100))
        self.stage_resolution = self.resources.conf['stage_resolution']
        self.stage_pane = StagePane(
            self, wx.ID_ANY, self.resources, self.events,
            size=self.stage_resolution)

        # self.setup_menu()
        self.create_menu_bar()
        self.toolbar = ToolBar(self.resources, self)

        self.code_pane = CodePane(self, self.resources, self.events)
        self.characters_pane = CharactersPane(
            self, self.resources, self.events)
        self.sprites_pane = SpritesPane(self, self.resources, self.events)
        self.project = Project(self.resources, self.events)
        self.setup_shell()
        self.setup_basket_classes()
        self.setup_basket_members()

        self.statusbar = self.CreateStatusBar(2)
        # self.statusbar.SetStatusWidths([1,-1])
        # self.tab.AddPage(wx.StaticText(self.tab, -1, "Costumes"), "Costumes")
        self.statusbar.SetStatusText("Self-Sufficiency Level: 0")

        self.widget_placement()
        self.Layout()

    def create_menu_bar(self):
        menu_schema = [{"title": _("&File"),
            "items": [
                {"title": _("&New project"),
                 "description": _("Create a new project"),
                 "id": wx.ID_NEW,
                 "handler": self.on_new_project},
                {"title": _("&Load project"),
                 "description": _("Load a project from disk"),
                 "id": wx.ID_OPEN,
                 "handler": self.on_open_project},
                {"title": _("&Save project"),
                 "description": _("Save a project to disk"),
                 "id": wx.ID_SAVE,
                 "handler": self.on_save_project},
                {"title": _("&Duplicate project"),
                 "description": _("Save a project to disk changing its name"),
                 "id": wx.ID_SAVEAS,
                 "handler": self.on_saveas_project},
                {},
                {"title": _("&Examples"),
                 "description": _("Load one of the example projects"),
                 #"id": wx.ID_SAVEAS,
                 "handler": self.test_load},
                {},
                {"title": _("E&xit"),
                 "description": _("Close Wiggler"),
                 "id": wx.ID_EXIT,
                 "handler": self.exit}
            ]},
            {"title": _("&Modify"),
                 "items": [
                    {"title": _("&Undo"),
                     "description": _("Undo the last action"),
                     "id": wx.ID_UNDO,
                    #"handler": self.on_undo
                    },
                    {"title": _("&Redo"),
                     "description": _("Redo the last action"),
                     "id": wx.ID_REDO,
                    #"handler": self.on_redo
                    },
                    {},
                    {"title": _("&Copy"),
                     "description": _("Copy selected text to the clipboard"),
                     "id": wx.ID_COPY,
                     # "handler": self.on_copy
                    },
                    {"title": _("&Cut"),
                     "description": _("Move selected text to the clipboard"),
                     "id": wx.ID_CUT,
                     #"handler": self.on_cut
                    },
                    {"title": _("&Paste"),
                     "description": _("Paste text from the clipboard"),
                     "id": wx.ID_PASTE,
                     # "handler": self.on_paste
                    },
                    {},
                    {"title": _("Pr&eferences"),
                     "description": _("Open the preference dialog"),
                     #"id": wx.ID_ANY,
                     # "handler": self.on_paste
                    }
                    ]
            },
            {"title": _("&Appearance"),
                "items": [
                    {}
                ]
            }
        ]
        bf = MenuBarFactory(self, menu_schema)
        self.SetMenuBar(bf.menubar())

    def widget_placement(self):
        sizer = wx.GridBagSizer()
        sizer.Add(self.stage_pane, (0, 0))
        sizer.Add(self.basket_classes, (0, 1), span=(1, 1))
        sizer.Add(self.basket_functions, (1, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.code_pane, (0, 2), span=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.characters_pane, (1, 0), flag=wx.EXPAND)
        sizer.Add(self.shell, (2, 0), span=(1, 3), flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def setup_basket_members(self):
        self.basket_functions = wx.ListCtrl(
            self, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT)
        self.basket_functions.InsertColumn(0, "Available attributes")

    def setup_basket_classes(self):
        self.basket_classes = wx.ListCtrl(
            self, wx.ID_ANY, size=(200, 400), style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0, "Available Classes")
        self.basket_classes.InsertStringItem(0, "MovingSprite")
        self.basket_classes.InsertStringItem(1, "StaticSprite")

    def setup_shell(self):
        self.shell = wx.py.shell.Shell(parent=self)
        self.shell.Show()

    def setup_menu(self):
        menu_exit_id = wx.NewId()
        menu_testload_id = wx.NewId()
        file_menu = wx.Menu()
        file_menu.Append(menu_exit_id, "Exit", "Exit")
        file_menu.Append(menu_testload_id, "Test Load", "Test Load")
        wx.EVT_MENU(self, menu_exit_id, self.exit)
        wx.EVT_MENU(self, menu_testload_id, self.test_load)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "&File")
        self.SetMenuBar(menu_bar)

    def exit(self, event):
        self.Close(True)

    def test_load(self, event):
        self.project.load(
            filename="tests/fixtures/test_project.wig")

    def load(self, event):
        # FIXME get filenam from event
        filename = None
        self.project.load(filename)

    def play(self, event):
        # TODO move to project
        self.project.play()

# EVT handlers

    def on_new_project(self, event):
        pass

    def on_open_project(self, event):
        pass

    def on_save_project(self, event):
        pass

    def on_saveas_project(self, event):
        pass
