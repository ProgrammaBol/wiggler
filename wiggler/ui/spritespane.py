import wx


class SpritesPane(wx.ListCtrl):

    def __init__(self, parent, resources, events):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_ICON)
        self.events = events
        self.resources = resources
        self.il = wx.ImageList(30, 30, True)
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.events.subscribe(self, ['reload', 'actchar'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_select)

    def reload(self):
        pass

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'actchar':
            self.set_active_sprite(event.data.character)
        event.Skip()

    def list_select(self, event):
        self.set_active_sprite(event.m_itemIndex)

    def set_active_sprite(self, character):
        character.set_active_sprite(0)
        # self.SetItem(character.active_sprite)
        sprite_builder = character.get_sprite_builder(
            index=character.active_sprite)
        self.events.send('actsprite', sprite_builder=sprite_builder)
