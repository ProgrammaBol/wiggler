import wx
import wx.py

from editor import TextEditor
from spriteelements import SpriteElement
from stage import Stage

class RootWindow(wx.Frame):

    def __init__(self):
        #super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self,None, -1, "Menu")
        self.elements = {}
        self.current_element = None
        self.SetMinSize((100,100))

        self.stage = Stage(self, wx.ID_ANY, size = (300,300))
        self.setup_menu()
        self.setup_toolbar()

        self.setup_object_area()
        self.setup_sprites_list()
        self.setup_shell()
        self.setup_basket_classes()
        self.setup_basket_members()

        self.widget_placement()
        self.Layout()

    def widget_placement(self):
        sizer = wx.GridBagSizer()
        sizer.Add(self.stage, (0,0))
        sizer.Add(self.basket_classes, (0,1), span=(1,1))
        sizer.Add(self.basket_functions, (1,1), span=(1,1), flag=wx.EXPAND)
        sizer.Add(self.tab, (0,2), span=(2,1), flag=wx.EXPAND)
        sizer.Add(self.sprites, (1,0), flag=wx.EXPAND)
        sizer.Add(self.shell, (2,0), span=(1,3),  flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)


    def setup_basket_members(self):
        self.basket_functions = wx.ListCtrl(self, wx.ID_ANY, size = (200,300))

    def setup_basket_classes(self):
        self.basket_classes = wx.ListCtrl(self, wx.ID_ANY, size = (200,300), style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0,"Classes")
        self.basket_classes.InsertStringItem(0, "Movement")
        self.basket_classes.InsertStringItem(1, "Stage")

    def setup_shell(self):
        self.shell = wx.py.crust.Crust(parent=self)
        self.shell.Show()

    def setup_sprites_list(self):
        self.sprites = wx.ListCtrl(self, style = wx.LC_ICON)
        self.sprites.Bind(wx.EVT_LIST_ITEM_SELECTED, self.onSpriteSelected)
        self.il = wx.ImageList(30,30, True)
        img_list=self.sprites.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)

        # Fixtures
        spritesheet_bitmap =  wx.Bitmap('resources/spritesheets/master.png')
        spritesheet_image = wx.ImageFromBitmap(spritesheet_bitmap)
        subsize = wx.Rect(481,403, 29,29)
        image = spritesheet_image.GetSubImage(subsize)
        image_scaled = image.Scale(30,30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        t = self.il.Add(sprite_bitmap)
        index = self.sprites.InsertImageItem(0,0)
        self.elements[index] = SpriteElement('example')
        print t

    def onSpriteSelected(self, event):
        try:
            self.current_element.raw_code = self.editor.GetText()
        except AttributeError:
            pass
        self.current_element = self.elements[event.m_itemIndex]
        self.editor.set_buffer(self.current_element.raw_code)

    def setup_object_area(self):
        self.tab = wx.Notebook(self, -1)
        self.editor = TextEditor(self.tab, wx.ID_ANY)
        self.tab.AddPage(self.editor, "Codice")
        self.tab.AddPage(wx.StaticText(self.tab, -1, "Costumes"), "Costumes")

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
        play_image_bitmap =  wx.Bitmap('resources/images/play.png')
        play_image = wx.ImageFromBitmap(play_image_bitmap)
        play_image_scaled = play_image.Scale(30,30, wx.IMAGE_QUALITY_HIGH)
        play_image = wx.BitmapFromImage(play_image_scaled)
        playtool = self.tools.AddLabelTool(wx.ID_ANY, 'Play', play_image)
        self.Bind(wx.EVT_TOOL, self.play, playtool)
        stop_image_bitmap =  wx.Bitmap('resources/images/stop.png')
        stop_image = wx.ImageFromBitmap(stop_image_bitmap)
        stop_image_scaled = stop_image.Scale(30,30, wx.IMAGE_QUALITY_HIGH)
        stop_image = wx.BitmapFromImage(stop_image_scaled)
        stoptool = self.tools.AddLabelTool(wx.ID_ANY, 'stop', stop_image)
        self.tools.Realize()

    def play(self, event):
        self.current_element.raw_code = self.editor.GetText()
        for index in range(self.sprites.GetItemCount()):
            self.stage.clear()
            spriteelement = self.elements[index]
            spriteelement.create_module()
            self.stage.add_elements(spriteelement)

    def exit(self, event):
        self.Close(True)
