import wx

from wiggler.core.events import Events
from wiggler.core.project import Project
from wiggler.core.resources import Resources
from wiggler.ui.root import RootWindow


class Wiggler(wx.App):

    def __init__(self, filename=None):
        wx.App.__init__(self, filename)

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
