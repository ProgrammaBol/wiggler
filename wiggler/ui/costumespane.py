import wx


class CostumesPane(wx.ListCtrl):

    def __init__(self, parent, resources, events):
        wx.ListCtrl.__init__(self, parent, size=(100, 400), style=wx.LC_ICON)
        self.events = events
        self.resources = resources
        self.il = wx.ImageList(30, 30, True)
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.events.subscribe(self, ['projload', 'spriteloaded'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.list_select)

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'spriteloaded':
            self.reload()
            self.load_costume(event.data.costume)
        event.Skip()

    def reload(self):
        self.DeleteAllItems()

    def list_select(self, event):
        self.set_active_costume(event.m_itemIndex)

    def set_active_costume(self, index):
        self.events.send('active_costume_set', index=index)

    def load_costume(self, costume):
        width, height, raw_image = costume.get_raw_image()
        bitmap = wx.BitmapFromBufferRGBA(width, height, raw_image)
        image = wx.ImageFromBitmap(bitmap)
        image_scaled = image.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        self.il.Add(sprite_bitmap)
        self.InsertImageStringItem(0, costume.name, 0)
