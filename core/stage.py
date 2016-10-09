import os
import pygame
import sys
import wx

from engine.datastructures import EventQueue, StageContext
from engine.stagecontroller import StageController

tilemap = dict()

class Stage(wx.StaticBox):
    def __init__(self, parent, id, title = 'SDL window', **options):
        wx.StaticBox.__init__(*(self, parent, id, title), **options)
        self.parent = parent

        self._initialized = 0
        self._resized = 0
        self._surface = None
        self.__needsDrawing = 1
        #hwnd = self.parent.GetHandle()
        self.size = self.GetSizeTuple()

        wx.EVT_SIZE(self, self.OnSize)
        wx.EVT_IDLE(self, self.OnIdle)
        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_PAINT, self.OnPaint)
        self.Bind(wx.EVT_TIMER, self.Update, self.timer)

        self.max_fps = 60.0
        self.timespacing = 1000.0 / self.max_fps
        self.timer.Start(self.timespacing, False)
        self.default_backcolor = (255, 255, 255)


    def OnIdle(self, ev):
        if not self._initialized or self._resized:
            if not self._initialized:
                # get the handle
                hwnd = self.GetHandle()

                os.environ['SDL_WINDOWID'] = str(hwnd)
                if sys.platform == 'win32':
                    os.environ['SDL_VIDEODRIVER'] = 'windib'
                pygame.init()
                self.screen = pygame.display.set_mode(self.size)
                main_event_queue = EventQueue()
                context_data = { "clock": self.timer,
                                "resolution": self.size,
                                "screen": self.screen,
                                }
                self.stage_context = StageContext(context_data)
                self.stage_controller = StageController(main_event_queue, self.stage_context)
                self._initialized = 1
        else:
            self._resized = 0

        x,y = self.GetSizeTuple()
        self._surface = pygame.display.set_mode((x,y))

        self._surface.fill((0,0,0))
        if self.__needsDrawing:
            self.draw()

    def OnPaint(self, ev):
        self.Redraw()

    def OnSize(self, ev):
        self.size = self.GetSizeTuple()

    def Kill(self, event):
        # Make sure Pygame can't be asked to redraw /before/ quitting by unbinding all methods which
        # call the Redraw() method
        # (Otherwise wx seems to call Draw between quitting Pygame and destroying the frame)
        self.Unbind(event = wx.EVT_PAINT, handler = self.OnPaint)
        self.Unbind(event = wx.EVT_TIMER, handler = self.Update, source = self.timer)
        pygame.quit()

    def set_background(self):
        filename = os.path.normpath("assets/images/stars.jpg")
        image = pygame.image.load(filename)
        background_image = image.subsurface((0,0), (self.size[0], self.size[1])).copy()
        background_image.convert()
        background_image.set_alpha(127)

    def draw(self):
        pygame.draw.circle(self._surface, (250,0,0), (100,100), 50)
        pygame.display.flip()
        #raise NotImplementedError('please define a .draw() method!')

    def Update(self):
        #loop = main_event_queue.handle_events()
        #background_change, background, screen_elements = game_controller.update()
        self.Redraw()

    def Redraw(self):
        self.screen.fill((0,0,0))
        #screen.fill(default_backcolor)
        #screen.blit(background_image, (0,0))
        #screen_elements.draw(screen)
        pygame.display.flip()
        #clock.tick(max_fps)
