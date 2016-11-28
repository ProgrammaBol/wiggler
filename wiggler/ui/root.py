import wx
import wx.py

from wiggler.ui.editor import TextEditor
from wiggler.ui.stagepane import StagePane
from wiggler.ui.toolbar import ToolBar
from wiggler.ui.characterspane import CharactersPane


class RootWindow(wx.Frame):

    def __init__(self, resources):
        # super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self, None, -1, "Menu")
        self.resources = resources
        self.current_character = None
        self.SetMinSize((100, 100))
        self.stage_resolution = self.resources.conf['stage_resolution']
        self.stage_pane = StagePane(
            self, wx.ID_ANY, self.resources, size=self.stage_resolution)

        self.setup_menu()
        self.toolbar = ToolBar(self.resources, self)

        self.setup_object_area()
        self.characters_pane = CharactersPane(self, self.resources)
        self.setup_shell()
        self.setup_basket_classes()
        self.setup_basket_members()

        self.statusbar = self.CreateStatusBar(2)
        # self.statusbar.SetStatusWidths([1,-1])
        self.statusbar.SetStatusText("Self-Sufficiency Level: 0")
        self.current_character = None
        self.current_sprite = None

        self.widget_placement()
        self.Layout()

    def widget_placement(self):
        sizer = wx.GridBagSizer()
        sizer.Add(self.stage_pane, (0, 0))
        sizer.Add(self.basket_classes, (0, 1), span=(1, 1))
        sizer.Add(self.basket_functions, (1, 1), span=(1, 1), flag=wx.EXPAND)
        sizer.Add(self.tab, (0, 2), span=(2, 1), flag=wx.EXPAND)
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

    def setup_object_area(self):
        self.tab = wx.Notebook(self, -1)
        self.editor = TextEditor(self.tab, wx.ID_ANY)
        self.generated_code = TextEditor(self.tab, wx.ID_ANY)
        self.tab.AddPage(self.editor, "Code")
        self.tab.AddPage(wx.StaticText(self.tab, -1, "Costumes"), "Costumes")
        self.tab.AddPage(self.generated_code, "Generated Code")

    def setup_menu(self):
        menu_exit_id = wx.NewId()
        menu_testload_id = wx.NewId()
        file_menu = wx.Menu()
        file_menu.Append(menu_exit_id, "Exit", "Exit")
        file_menu.Append(menu_testload_id, "Test Load", "Test Load")
        wx.EVT_MENU(self, menu_exit_id, self.exit)
        wx.EVT_MENU(self, menu_testload_id, self.test_load)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

    def exit(self, event):
        self.Close(True)

    def test_load(self, event):
        project_def = {
            'characters': {
                'player1': {
                    'sprites': ['ship'],
                }
            },
            'background': {
                'solid': (0, 0, 0),
            }
        }
        self.load(project_def)

    def load(self, project_def):
        char_def = project_def['characters']['player1']
        character = self.resources.cast.add_character('player1', char_def)
        index = self.characters_pane.load_character(character)
        self.resources.cast.set_index('player1', index)
        if self.current_character is None:
            self.change_current_character(character)

    def change_current_character(self, character):
        self.current_character = character
        self.change_current_sprite(0)

    def change_current_sprite(self, spriteindex):
        self.save_current_buffers()
        sprite_builder = self.current_character.get_sprite(index=spriteindex)
        # this depends on self sufficiency level
        text_buffers = sprite_builder.sufficiency.get_buffers_list()
        # for buffer_name in text_buffers:
        #     open an editor tab for each buffer
        #     set buffers to user_code[buffer_name]
        self.editor.set_buffer(sprite_builder.user_code[text_buffers[0]])
        self.current_sprite = sprite_builder
        self.generated_code.set_readonly_buffer(
            self.current_sprite.generated_code)
        # for index, attrib in enumerate(dir(MovingSprite)):
        #    self.basket_functions.InsertStringItem(index, attrib)
        # self.basket_functions.DeleteAllItems()

    def save_current_buffers(self):
        if self.current_sprite is not None:
            text_buffers = self.current_sprite.sufficiency.get_buffers_list()
            self.current_sprite.user_code[
                text_buffers[0]] = self.editor.GetText()

    def play(self, event):
        self.save_current_buffers()
        self.stage_pane.play()
        self.generated_code.set_readonly_buffer(
            self.current_sprite.generated_code)

    def onCharSelected(self, event):
        character = self.resources.cast.get_character(index=event.m_itemIndex)
        self.change_current_character(character)

    def onSpriteSelected(self, event):
        self.change_current_sprite(event.m_itemIndex)
