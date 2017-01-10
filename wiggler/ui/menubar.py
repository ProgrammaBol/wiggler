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
import gettext
import wx

from collections import OrderedDict

gettext.install("wiggler")

ID_CHANGE_BACKGROUND = wx.NewId()
ID_ADD_COSTUME = wx.NewId()
ID_DEL_COSTUME = wx.NewId()
ID_ADD_SHEET = wx.NewId()
ID_DEL_SHEET = wx.NewId()
ID_ADD_CHARACTER = wx.NewId()
ID_DEL_CHARACTER = wx.NewId()
ID_ADD_ANIMATION = wx.NewId()
ID_DEL_ANIMATION = wx.NewId()
ID_ADD_SPRITE = wx.NewId()
ID_DEL_SPRITE = wx.NewId()
ID_ADD_IMAGE = wx.NewId()
ID_DEL_IMAGE = wx.NewId()
ID_ADD_SOUND = wx.NewId()
ID_DEL_SOUND = wx.NewId()
ID_ADD_MUSIC = wx.NewId()
ID_DEL_MUSIC = wx.NewId()
ID_ADD_TEXT = wx.NewId()
ID_DEL_TEXT = wx.NewId()


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
            ID_ADD_COSTUME: ('Add costume',
                             'Add a new costume to project library',
                             'add_costume'),
            ID_DEL_COSTUME: ('Remove costume',
                             'Remove costume from project library',
                             'del_costume'),
            ID_ADD_SHEET: ('Add sprite sheet',
                           'Add a new sheet to project library',
                           'add_sheet'),
            ID_DEL_SHEET: ('Remove sprite sheet',
                           'Remove sheet from project library',
                           'del_sheet'),
            ID_ADD_CHARACTER: ('Add character',
                               'Add a new character to project library',
                               'add_character'),
            ID_DEL_CHARACTER: ('Remove character',
                               'Remove character from project library',
                               'del_character'),
            ID_ADD_ANIMATION: ('Add animation',
                               'Add a new animation to project library',
                               'add_animation'),
            ID_DEL_ANIMATION: ('Remove animation',
                               'Remove animation from project library',
                               'del_animation'),
            ID_ADD_SPRITE: ('Add sprite',
                            'Add a new sprite to project library',
                            'add_sprite'),
            ID_DEL_SPRITE: ('Remove sprite',
                            'Remove sprite from project library',
                            'del_sprite'),
            ID_ADD_IMAGE: ('Add image',
                           'Add a new image to project library',
                           'add_image'),
            ID_DEL_IMAGE: ('Remove image',
                           'Remove image from project library',
                           'del_image'),
            ID_ADD_SOUND: ('Add sound',
                           'Add a new sound to project library',
                           'add_sound'),
            ID_DEL_SOUND: ('Remove sound',
                           'Remove sound from project library',
                           'del_sound'),
            ID_ADD_MUSIC: ('Add music',
                           'Add a new music to project library',
                           'add_music'),
            ID_DEL_MUSIC: ('Remove music',
                           'Remove music from project library',
                           'del_music'),
            ID_ADD_TEXT: ('Add text',
                          'Add a new text box to project library',
                          'add_text'),
            ID_DEL_TEXT: ('Remove text',
                          'Remove text box from project library',
                          'del_text'),
            ID_CHANGE_BACKGROUND: ('Change default background',
                                   'Change default background for the project',
                                   'change_background'),
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
        self.menu['&Resources'] = [
            ID_CHANGE_BACKGROUND,
            wx.ID_SEPARATOR,
            ID_ADD_SHEET,
            ID_DEL_SHEET,
            wx.ID_SEPARATOR,
            ID_ADD_COSTUME,
            ID_DEL_COSTUME,
            wx.ID_SEPARATOR,
            ID_ADD_CHARACTER,
            ID_DEL_CHARACTER,
            wx.ID_SEPARATOR,
            ID_ADD_SPRITE,
            ID_DEL_SPRITE,
            wx.ID_SEPARATOR,
            ID_ADD_IMAGE,
            ID_DEL_IMAGE,
            wx.ID_SEPARATOR,
            ID_ADD_ANIMATION,
            ID_DEL_ANIMATION,
            wx.ID_SEPARATOR,
            ID_ADD_SOUND,
            ID_DEL_SOUND,
            wx.ID_SEPARATOR,
            ID_ADD_MUSIC,
            ID_DEL_MUSIC,
            wx.ID_SEPARATOR,
            ID_ADD_TEXT,
            ID_DEL_TEXT,
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
