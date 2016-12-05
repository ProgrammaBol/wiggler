import wx

from wiggler.ui.root import RootWindow
from wiggler.core.resources import Resources


class Wiggler(wx.App):

    def OnInit(self):
        self.resources = Resources()
        self.resources.create_new_project()
        frame = RootWindow(self.resources)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


def main():
    app = Wiggler()
    app.MainLoop()
