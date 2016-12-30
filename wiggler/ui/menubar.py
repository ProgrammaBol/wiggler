""" this class create and populate the menu toolbar
    the actual menus are :
    + &File
      - &New projet    wx.ID_NEW
      - &Load project  wx.ID_OPEN
      - &Save project  wx.ID_SAVE
      - &Save a copy   wx.ID_SAVEAS
      - ---
      - &Examples
      - ---
      - E&xit

    + &Modify
      - &Undo (Ctrl + Z) wx.ID_UNDO
      - &Redo (Ctrl + Y) wx.ID_REDO
      - Copy  (Ctrl + C) wx.ID_COPY
      - Cut   (Ctrl + X) wx.ID_CUT
      - Paste (Ctrl + V) wx.ID_PASTE
      - ---
      - &Preferences

    + &Appearance
      - &Language
      - ---
      - Show &Tool bar (checkbox default on)
      - Show &Menu bar (checkbox default on)
      - Shoe &Status bar (checkout default on)
      - ---
      - Show &Console (checkbox default on)


References:
    https://wiki.wxpython.org/wxPython%20Style%20Guide
    https://wxpython.org/Phoenix/docs/html/wx.Menu.html#wx.Menu
    https://wxpython.org/Phoenix/docs/html/wx.MenuBar.html#wx.MenuBar

"""
import wx
import gettext

from collections import OrderedDict

gettext.install("wiggler")


class MenuBar(wx.MenuBar):

    def __init__(self, events):
        """Create a menu bar facade to simplify toolbar creation

           Arguments:
               parent - a wx.Frame object containing the menu bar
        """
        wx.MenuBar.__init__(self, wx.ID_ANY)
        self.events = events
        self.menu_items = {
            wx.ID_NEW: ("&New project", "Create a new project", "projnew"),
            wx.ID_OPEN: ("&Load project", "Load a project from disk",
                         "projopen"),
            wx.ID_SAVE: ("&Save project", "Save a project to disk",
                         "projsave"),
            wx.ID_SAVEAS: ("&Duplicate project",
                           "Save a project to disk changing its name",
                           'projsaveas'),
            wx.ID_EXECUTE: ("&Examples", "Load one of the example projects",
                            'testload'),
            wx.ID_EXIT: ("E&xit", "Close Wiggler", "exit"),
            wx.ID_UNDO: ("&Undo", "Undo the last action", 'undo'),
            wx.ID_REDO: ("&Redo", "Redo the last action", 'redo'),
            wx.ID_COPY: ("&Copy", "Copy selected text to the clipboard",
                         'copy'),
            wx.ID_CUT: ("&Cut", "Move selected text to the clipboard", 'cut'),
            wx.ID_PASTE: ("&Paste", "Paste text from the clipboard", 'paste'),
            wx.ID_PREFERENCES: ("Pr&eferences", "Open the preference dialog",
                                'preferences'),
            wx.ID_SEPARATOR: (),
        }
        self.menu = OrderedDict()
        self.menu["&File"] = [
            wx.ID_NEW,
            wx.ID_OPEN,
            wx.ID_SAVE,
            wx.ID_SAVEAS,
            wx.ID_SEPARATOR,
            wx.ID_EXECUTE,
            wx.ID_SEPARATOR,
            wx.ID_EXIT,
        ]
        self.menu["&Edit"] = [
            wx.ID_UNDO,
            wx.ID_REDO,
            wx.ID_SEPARATOR,
            wx.ID_COPY,
            wx.ID_CUT,
            wx.ID_PASTE,
            wx.ID_SEPARATOR,
            wx.ID_PREFERENCES,
        ]
        self.menu["&Appearance"] = []

        for name, item_list in self.menu.items():
            current = wx.Menu()
            for menu_id in item_list:
                if menu_id == wx.ID_SEPARATOR:
                    current.AppendSeparator()
                else:
                    title, description, __ = self.menu_items[menu_id]
                    current.Append(menu_id, _(title), _(description))
            self.Append(current, name)

    def notice_dispatcher(self, event):
        menu_id = event.GetId()
        __, __, notice = self.menu_items[menu_id]
        self.events.send(notice)
