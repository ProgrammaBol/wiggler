import wx


class UIimage(object):

    def __init__(self, resources, name, definition, **params):
        self.name = name
        bitmap = wx.Bitmap(definition['abs_path'])
        self.image = wx.ImageFromBitmap(bitmap)

    def get_image(self, scale=None):
        image = self.image
        if scale is not None:
            width, height = scale
            image = self.image.Scale(width, height, wx.IMAGE_QUALITY_HIGH)
        bitmap = wx.BitmapFromImage(image)
        return bitmap
