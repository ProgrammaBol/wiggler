import wx

from wiggler.ui.root import RootWindow
from wiggler.core.resources import Resources
from wiggler.core.events import Events
from wiggler.core.project import Project


class Wiggler(wx.App):

    def __init__(self, redirect=True, filename=None):
        wx.App.__init__(self, redirect, filename)

    def OnInit(self):
        self.resources = Resources()
        self.events = Events()
        self.project = Project(self.resources, self.events)
        frame = RootWindow(self.resources, self.events, self.project)
        frame.Show(True)
        self.SetTopWindow(frame)
        return True


def main():
    app = Wiggler()
    app.MainLoop()
