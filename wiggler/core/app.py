import wx
import wx.stc
import wx.py
from ui import RootWindow


class Slither(wx.App):

    def OnInit(self):
        frame = RootWindow()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


def main():
    app = Slither()
    app.MainLoop()
