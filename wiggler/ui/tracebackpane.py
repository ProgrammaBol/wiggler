import traceback
import wx
import wx.lib.agw.aui as aui


class TracebackPane(aui.AuiNotebook):

    def __init__(self, parent, resources, events):
        self.resources = resources
        self.events = events
        super(TracebackPane, self).__init__(parent, -1,
                                            style=aui.AUI_NB_CLOSE_ON_ALL_TABS)

        self.Show()
        self.events.subscribe(self, ['projload', 'traceback'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)

    def notice_handler(self, event):
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'traceback':
            self.add_message(event.data.exc_type, event.data.exc_value,
                             event.data.tb)
        event.Skip()

    def reload(self):
        self.DeletePage(0)

    def add_message(self, exc_type, exc_value, tb):
        tb_lines = traceback.format_exception(exc_type, exc_value, tb)
        message = "".join(tb_lines)
        text = wx.TextCtrl(self, -1, message,
                           style=wx.NO_BORDER | wx.TE_MULTILINE)
        self.AddPage(text, "traceback")
