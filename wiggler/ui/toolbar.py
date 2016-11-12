import wx


class ToolBar(object):

    def __init__(self, resources, parent):
        self.resources = resources
        self.width = 30
        self.height = 30
        self.parent = parent
        self.tools = parent.CreateToolBar()
        self.add_button('play', 'Play', self.parent.play)
        self.add_button('stop', 'Stop', self.stop)
        self.add_button('incss', 'incss', self.incss)
        self.add_button('decss', 'decss', self.decss)
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

    def stop(self, event):
        pass

    # Self sufficiency is per-character attribute
    def decss(self, event):
        pass
        # self.selfsufficiency -= 1
        # self.statusbar.SetStatusText(
        #    "Self-Sufficiency Level: %d" % self.selfsufficiency)

    def incss(self, event):
        pass
        # self.selfsufficiency += 1
        # self.statusbar.SetStatusText(
        #    "Self-Sufficiency Level: %d" % self.selfsufficiency)
