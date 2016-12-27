import wx


class Data(object):
    pass


class ProjectEvent(wx.PyCommandEvent):

    def __init__(self, evtType, notice, **data):
        wx.PyCommandEvent.__init__(self, evtType)
        self.notice = notice
        self.data = Data()
        for key, value in data.items():
            setattr(self.data, key, value)


class Events(object):

    def __init__(self):
        self.EVT_TYPE_NOTICE = wx.NewEventType()
        self.EVT_NOTICE = wx.PyEventBinder(self.EVT_TYPE_NOTICE, 1)
        self.subscribers = {}

    def send(self, notice, **data):
        event = ProjectEvent(self.EVT_TYPE_NOTICE, notice, **data)
        try:
            for window in self.subscribers[notice]:
                wx.PostEvent(window.GetEventHandler(), event)
        except KeyError:
            pass

    def subscribe(self, window, commands):
        for command in commands:
            if command not in self.subscribers.keys():
                self.subscribers[command] = []
            self.subscribers[command].append(window)
