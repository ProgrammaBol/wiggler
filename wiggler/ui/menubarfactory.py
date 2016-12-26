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

# wx.ITEM_SEPARATOR
# self.fileMenu.Append(
#     ID_NEW_FILE,
#     "&New file\tCTRL+N",
#     "Creates a XYZ document"
# )


class MenuBarFactory(object):

    def __init__(self, parent, menu_schema):
        """Create a menu bar facade to simplify toolbar creation

           Arguments:
               parent - a wx.Frame object containing the menu bar
        """
        self.parent = parent
        self.bar = wx.MenuBar()
        for menu in menu_schema:
            current = wx.Menu()
            for item in menu["items"]:
                if len(item) == 0:
                    current.AppendSeparator()
                else:
                    menuitem = self.create_menu_item(
                        current,
                        item.get("title"),
                        item.get("id"),
                        item.get("description"),
                    )
                    if item.get("handler") is not None:
                        self.parent.Bind(wx.EVT_MENU, item["handler"], menuitem)
            self.bar.Append(current, menu["title"])

    def menubar(self):
        return self.bar

    def create_menu_item(self, menu, title, item_id=wx.ID_ANY, status="..."):
        """Creates a menu item, append it to a menu and return it,
           ready to be binded to an event handler.

           Arguments:
           menu        - Parent menu
           title       - Text to display on the menu

           Keyword arguments:
           id          - id to assign to menu (usually wx.ID_ANY)
           status      - Text to display on the status bar

           Returns:
           menuitem
        """
        if status is None:
            status = "..."
        if item_id is None:
            item_id = wx.ID_ANY
        item = menu.Append(item_id, title, status)
        return item
