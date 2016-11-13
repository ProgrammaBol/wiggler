import wx
import wx.py

from wiggler.core.editor import TextEditor
from wiggler.core.spriteelements import SpriteElement
from wiggler.engine.sprites import MovingSprite
from wiggler.core.stage import Stage
from wiggler.core.file_utils import get_resource_filename


class RootWindow(wx.Frame):

    def __init__(self):
        # super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self, None, -1, "Menu")
        self.elements = {}
        self.current_element = None
        self.selfsufficiency = 0
        self.SetMinSize((100, 100))

        self.stage = Stage(self, wx.ID_ANY, size=(400, 400))
        self.setup_menu()
        self.setup_toolbar()

        self.setup_object_area()
        self.setup_sprites_list()
        self.setup_shell()
        self.setup_basket_classes()
        self.setup_basket_members()

        self.statusbar = self.CreateStatusBar(2)
        # self.statusbar.SetStatusWidths([1,-1])
        self.statusbar.SetStatusText("Self-Sufficiency Level: 0")

        self.widget_placement()
        self.Layout()

    def widget_placement(self):
        sizer = wx.GridBagSizer()
        sizer.Add(self.stage, (0, 0))
        sizer.Add(self.basket_classes, (0, 1), span=(1, 1))
        sizer.Add(self.basket_functions, (1, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.tab, (0, 2), span=(2, 1), flag=wx.EXPAND)
        sizer.Add(self.sprites, (1, 0), flag=wx.EXPAND)
        sizer.Add(self.shell, (2, 0), span=(1, 3), flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)

    def setup_basket_members(self):
        self.basket_functions = wx.ListCtrl(
            self, wx.ID_ANY, size=(200, 300), style=wx.LC_REPORT)
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

    def setup_sprites_list(self):
        self.sprites = wx.ListCtrl(self, style=wx.LC_ICON)
        self.sprites.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSpriteSelected)
        self.il = wx.ImageList(30, 30, True)
        self.sprites.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)

        # Fixtures
        spritesheet_bitmap = wx.Bitmap(get_resource_filename('resources/spritesheets/master.png'))
        spritesheet_image = wx.ImageFromBitmap(spritesheet_bitmap)
        subsize = wx.Rect(481, 403, 29, 29)
        image = spritesheet_image.GetSubImage(subsize)
        image_scaled = image.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        self.il.Add(sprite_bitmap)
        index = self.sprites.InsertImageItem(0, 0)
        self.elements[index] = SpriteElement('example')

    def onSpriteSelected(self, event):
        try:
            self.current_element.raw_code = self.editor.GetText()
        except AttributeError:
            pass
        self.current_element = self.elements[event.m_itemIndex]
        self.editor.set_buffer(self.current_element.raw_code)
        self.basket_functions.DeleteAllItems()
        for index, attrib in enumerate(dir(MovingSprite)):
            self.basket_functions.InsertStringItem(index, attrib)
        self.generated_code.SetReadOnly(0)
        self.generated_code.SetText(self.current_element.element_code)
        self.generated_code.SetReadOnly(1)

    def setup_object_area(self):
        self.tab = wx.Notebook(self, -1)
        self.editor = TextEditor(self.tab, wx.ID_ANY)
        self.generated_code = TextEditor(self.tab, wx.ID_ANY)
        self.tab.AddPage(self.editor, "Code")
        self.tab.AddPage(wx.StaticText(self.tab, -1, "Costumes"), "Costumes")
        self.tab.AddPage(self.generated_code, "Generated Code")

    def setup_menu(self):
        menu_exit_id = wx.NewId()
        file_menu = wx.Menu()
        file_menu.Append(menu_exit_id, "Exit", "Exit")
        wx.EVT_MENU(self, menu_exit_id, self.exit)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

    def setup_toolbar(self):
        self.tools = self.CreateToolBar()
        self.add_toolbar_button(
            self.tools, get_resource_filename('resources/images/play.png'), 'Play', self.play)
        self.add_toolbar_button(
            self.tools, get_resource_filename('resources/images/stop.png'), 'Stop', self.stop)
        self.add_toolbar_button(
            self.tools, get_resource_filename('resources/images/incss.png'), 'incss', self.incss)
        self.add_toolbar_button(
            self.tools, get_resource_filename('resources/images/decss.png'), 'decss', self.decss)
        self.tools.Realize()

    def add_toolbar_button(self,
                           toolbar,
                           image_path,
                           label_text,
                           action_callable,
                           width=30,
                           height=30):
        """Creates a button and add it to a toolbar

           Arguments:

           toolbar         -- toolbar to attach the button into
           image_path      -- path of the png image used to decorate the button
           label_text      -- text of the button label
           action_callable -- function or method to call when button is pushed

           Keyword arguments:

           width           -- button width in pixel (default: 30 => 30px)
           height          -- button height in pixel (default: 30 => 30px)

           Returns:
           none
        """
        image = wx.ImageFromBitmap(wx.Bitmap(image_path))
        image = wx.BitmapFromImage(
            image.Scale(width, height, wx.IMAGE_QUALITY_HIGH))
        tool = toolbar.AddLabelTool(wx.ID_ANY, label_text, image)
        self.Bind(wx.EVT_TOOL, action_callable, tool)

    def stop(self, event):
        pass

    def decss(self, event):
        self.selfsufficiency -= 1
        self.statusbar.SetStatusText(
            "Self-Sufficiency Level: %d" % self.selfsufficiency)

    def incss(self, event):
        self.selfsufficiency += 1
        self.statusbar.SetStatusText(
            "Self-Sufficiency Level: %d" % self.selfsufficiency)

    def play(self, event):
        self.current_element.raw_code = self.editor.GetText()
        for index in range(self.sprites.GetItemCount()):
            self.stage.clear()
            spriteelement = self.elements[index]
            spriteelement.create_module()
            self.stage.add_elements(spriteelement)
        self.generated_code.SetReadOnly(0)
        self.generated_code.SetText(self.current_element.element_code)
        self.generated_code.SetReadOnly(1)

    def exit(self, event):
        self.Close(True)
