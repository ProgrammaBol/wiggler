import wx


class CharactersPane(wx.ListCtrl):

    def __init__(self, parent, resources):
        wx.ListCtrl.__init__(self, parent, style=wx.LC_ICON)
        self.parent = parent
        self.resources = resources
        self.Bind(wx.EVT_LIST_ITEM_SELECTED, self.parent.onCharSelected)
        self.il = wx.ImageList(30, 30, True)
        self.AssignImageList(self.il, wx.IMAGE_LIST_NORMAL)
        self.current_character = None

    def load_character(self, character):
        sprite_builder = character.sprite_builders[character.spritedef_list[0]]
        costume = sprite_builder.costumes.costumes[
            sprite_builder.costumes.costumes_list[0]]
        width, height, raw_image = costume.get_raw_image()
        bitmap = wx.BitmapFromBufferRGBA(width, height, raw_image)
        image = wx.ImageFromBitmap(bitmap)
        image_scaled = image.Scale(30, 30, wx.IMAGE_QUALITY_HIGH)
        sprite_bitmap = wx.BitmapFromImage(image_scaled)
        self.il.Add(sprite_bitmap)
        index = self.InsertImageItem(0, 0)
        return index
