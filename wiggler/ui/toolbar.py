import wx


class ToolBar(object):

    def __init__(self, resources, parent, events):
        self.resources = resources
        self.width = 30
        self.height = 30
        self.events = events
        self.parent = parent
        self.tools = parent.CreateToolBar()
        self.add_button('play', 'Play', self.play)
        self.add_button('stop', 'Stop', self.stop)
        self.add_button('incss', 'incss', self.incss)
        self.add_button('decss', 'decss', self.decss)
        self.add_button('costume', 'Add costume to sprite',
                        self.add_costume_sprite)
        self.add_button('nocostume', 'Remove costume from sprite',
                        self.del_costume_sprite)
        self.add_button('sprite', 'Add sprite to character',
                        self.add_sprite_character)
        self.add_button('nosprite', 'Remove sprite from character',
                        self.del_sprite_character)
        self.add_button('character', 'Add character to project',
                        self.add_character_project)
        self.add_button('nocharacter', 'Remove character from project',
                        self.del_character_project)
        self.tools.Realize()

    def add_button(self, bitmap_name, label_text, action_callable):
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
        UIimage = self.resources.load_ui_images(bitmap_name)
        image = UIimage.get_image(scale=(self.width, self.height))
        tool = self.tools.AddLabelTool(wx.ID_ANY, label_text, image)
        self.parent.Bind(wx.EVT_TOOL, action_callable, tool)

    def play(self, event):
        self.events.send('preplay')
        self.events.send('play')

    def stop(self, event):
        self.events.send('stop')

    def decss(self, event):
        self.resources.selfsuff.decrease_level()
        self.events.send('selfsuff_change')

    def incss(self, event):
        self.resources.selfsuff.increase_level()
        self.events.send('selfsuff_change')

    def add_costume_sprite(self, event):
        self.events.send('add_sprite_costume')

    def del_costume_sprite(self, event):
        self.events.send('del_sprite_costume')

    def add_sprite_character(self, event):
        self.events.send('add_char_sprite')

    def del_sprite_character(self, event):
        self.events.send('del_char_sprite')

    def add_character_project(self, event):
        self.events.send('add_char_proj')

    def del_character_project(self, event):
        self.events.send('del_char_proj')
