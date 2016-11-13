import wx
import wx.stc
import wx.py

from wiggler.core.ui import RootWindow

class Wiggler(wx.App):

    def OnInit(self):
        frame = RootWindow()
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


def main():
    app = Wiggler()
    app.MainLoop()
