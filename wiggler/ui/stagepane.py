import os
import pygame
import sys
import wx

from wiggler.engine.stage import Stage

tilemap = dict()


class StagePane(wx.StaticBox):

    def __init__(self, parent, id, resources, **options):
        wx.StaticBox.__init__(*(self, parent, id, 'SDL window'), **options)
        self.parent = parent
        self.resources = resources
        self.stage = Stage(self.resources)

        self._initialized = 0
        self._resized = 0
        self._surface = None
        self.__needsDrawing = 1
        self.size = self.GetSizeTuple()

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_IDLE(self, self.OnIdle)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.max_fps = 25.0
        self.timespacing = 1000.0 / self.max_fps
        self.timer.Start(self.timespacing, False)
        self.default_backcolor = (255, 255, 255)

    def OnIdle(self, ev):
        if not self._initialized or self._resized:
            if not self._initialized:
                hwnd = self.GetHandle()
                os.environ['SDL_WINDOWID'] = str(hwnd)
                if sys.platform == 'win32':
                    os.environ['SDL_VIDEODRIVER'] = 'windib'
                self.stage.start()
                self._initialized = 1
        else:
            self._resized = 0

    def clear(self):
        pass

    def OnPaint(self, ev):
        self.Redraw()

    def OnSize(self, ev):
        self.size = self.GetSizeTuple()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting
        # by unbinding all methods which call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame
        # and destroying the frame)
        self.Unbind(event=wx.EVT_PAINT, handler=self.OnPaint)
        self.Unbind(event=wx.EVT_TIMER, handler=self.Update, source=self.timer)
        pygame.quit()

    def Update(self, event):
        # loop = main_event_queue.handle_events()
        self.Redraw()

    def Redraw(self):
        if not self.stage.screen:
            return
        self.stage.update()

    def play(self):
        self.stage.populate()
