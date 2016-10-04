import wx
import wx.stc
import keyword
import pygame
import os

import os
import sys


class wxSDLWindow(wx.Frame):
    def __init__(self, parent, id, title = 'SDL window', **options):
        wx.Frame.__init__(*(self, parent, id, title), **options)
        self.parent = parent

        self._initialized = 0
        self._resized = 0
        self._surface = None
        self.__needsDrawing = 1

        wx.EVT_IDLE(self, self.OnIdle)

    def OnIdle(self, ev):
        if not self._initialized or self._resized:
            if not self._initialized:
                # get the handle
                hwnd = self.parent.GetHandle()

                os.environ['SDL_WINDOWID'] = str(hwnd)
                if sys.platform == 'win32':
                    os.environ['SDL_VIDEODRIVER'] = 'windib'
                pygame.init()
                wx.EVT_SIZE(self, self.OnSize)
                self._initialized = 1
        else:
            self._resized = 0

        x,y = self.GetSizeTuple()
        self._surface = pygame.display.set_mode((x,y))

        self._surface.fill((0,0,0))
        if self.__needsDrawing:
            self.draw()

    def OnPaint(self, ev):
        self.__needsDrawing = 1

    def OnSize(self, ev):
        self._resized = 1
        ev.Skip()

    def draw(self):
        pygame.draw.circle(self._surface, (250,0,0), (100,100), 50)
        pygame.display.flip()
        #raise NotImplementedError('please define a .draw() method!')

    def getSurface(self):
        return self._surface


class TextEditor(wx.stc.StyledTextCtrl):

    def __init__(self, parent, ID):
        super(TextEditor, self).__init__(parent, ID, wx.DefaultPosition, wx.DefaultSize, wx.BORDER_NONE)
        #super(TextEditor, self).__init__(parent, ID, (100,100), (200,200), wx.BORDER_NONE)
        self.SetEdgeMode(wx.stc.STC_EDGE_BACKGROUND)
        self.SetEdgeColumn(78)
        self.Bind(wx.stc.EVT_STC_MARGINCLICK, self.OnMarginClick)
        self.SetUpEditor()

    def SetValue(self, value):
        #if wx.USE_UNICODE:
        #    value = value.decode('utf_8')
        self.SetReadOnly(0)
        self.SetText(value)
        self.EmptyUndoBuffer()
        self.SetSavePoint()
        self.SetReadOnly(1)

    def Clear(self):
        self.SetReadOnly(0)
        self.ClearAll()
        self.SetReadOnly(1)

    def SetUpEditor(self):
        self.SetLexer(wx.stc.STC_LEX_PYTHON)
        self.SetKeyWords(0, " ".join(keyword.kwlist))
        # Enable folding
        self.SetProperty("fold", "1" )
        # Highlight tab/space mixing (shouldn't be any)
        self.SetProperty("tab.timmy.whinge.level", "1")
        # Set left and right margins
        self.SetMargins(2,2)
        # Set up the numbers in the margin for margin #1
        self.SetMarginType(1, wx.stc.STC_MARGIN_NUMBER)
        # Reasonable value for, say, 4-5 digits using a mono font (40 pix)
        self.SetMarginWidth(1, 40)
        # Indentation and tab stuff
        self.SetIndent(4)                   # Proscribed indent size for wx
        self.SetIndentationGuides(True) # Show indent guides
        self.SetBackSpaceUnIndents(True)
                # Backspace unindents rather than delete 1 space
        self.SetTabIndents(True)            # Tab key indents
        self.SetTabWidth(4)                 # Proscribed tab size for wx
        self.SetUseTabs(False)              # Use spaces rather than tabs, or
                                            # TabTimmy will complain!
        # White space
        self.SetViewWhiteSpace(False)   # Don't view white space
        # EOL: Since we are loading/saving ourselves, and the
        # strings will always have \n's in them, set the STC to
        # edit them that way.
        self.SetEOLMode(wx.stc.STC_EOL_LF)
        self.SetViewEOL(False)
        # No right-edge mode indicator
        self.SetEdgeMode(wx.stc.STC_EDGE_NONE)
        # Setup a margin to hold fold markers
        self.SetMarginType(2, wx.stc.STC_MARGIN_SYMBOL)
        self.SetMarginMask(2, wx.stc.STC_MASK_FOLDERS)
        self.SetMarginSensitive(2, True)
        self.SetMarginWidth(2, 12)
        # and now set up the fold markers
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEREND,
                wx.stc.STC_MARK_BOXPLUSCONNECTED,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPENMID,
                wx.stc.STC_MARK_BOXMINUSCONNECTED, "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERMIDTAIL,
                wx.stc.STC_MARK_TCORNER,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERTAIL,
                wx.stc.STC_MARK_LCORNER,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDERSUB,
                wx.stc.STC_MARK_VLINE,    "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDER,
                wx.stc.STC_MARK_BOXPLUS,  "white", "black")
        self.MarkerDefine(wx.stc.STC_MARKNUM_FOLDEROPEN,
                wx.stc.STC_MARK_BOXMINUS, "white", "black")
        # Global default style
        if wx.Platform == '__WXMSW__':
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                           'fore:#000000,back:#FFFFFF,face:Courier New,size:9')
        else:
            self.StyleSetSpec(wx.stc.STC_STYLE_DEFAULT,
                           'fore:#000000,back:#FFFFFF,face:Courier,size:12')
        # Clear styles and revert to default.
        self.StyleClearAll()
        # Following style specs only indicate differences from default.
        # The rest remains unchanged.
        self.StyleSetSpec(wx.stc.STC_STYLE_LINENUMBER,
                                                'fore:#000000,back:#99A9C2')
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACELIGHT,
                                                'fore:#00009D,back:#FFFF00')
        self.StyleSetSpec(wx.stc.STC_STYLE_BRACEBAD,
                                                'fore:#00009D,back:#FF0000')
        self.StyleSetSpec(wx.stc.STC_STYLE_INDENTGUIDE, "fore:#CDCDCD")
        self.StyleSetSpec(wx.stc.STC_P_DEFAULT, 'fore:#000000')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTLINE,
                                               'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_COMMENTBLOCK,
                                               'fore:#008000,back:#F0FFF0')
        self.StyleSetSpec(wx.stc.STC_P_NUMBER, 'fore:#008080')
        self.StyleSetSpec(wx.stc.STC_P_STRING, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_CHARACTER, 'fore:#800080')
        self.StyleSetSpec(wx.stc.STC_P_WORD, 'fore:#000080,bold')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLE, 'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(wx.stc.STC_P_TRIPLEDOUBLE,
                                               'fore:#800080,back:#FFFFEA')
        self.StyleSetSpec(wx.stc.STC_P_CLASSNAME, 'fore:#0000FF,bold')
        self.StyleSetSpec(wx.stc.STC_P_DEFNAME, 'fore:#008080,bold')
        self.StyleSetSpec(wx.stc.STC_P_OPERATOR, 'fore:#800000,bold')
        self.StyleSetSpec(wx.stc.STC_P_IDENTIFIER, 'fore:#000000')
        self.SetCaretForeground("BLUE")
        self.SetSelBackground(True,
                      wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHT))
        self.SetSelForeground(True,
                      wx.SystemSettings_GetColour(wx.SYS_COLOUR_HIGHLIGHTTEXT))

    def OnMarginClick(self, evt):
        # fold and unfold as needed
        if evt.GetMargin() == 2:
            if evt.GetShift() and evt.GetControl():
                self.FoldAll()
            else:
                lineClicked = self.LineFromPosition(evt.GetPosition())

                if self.GetFoldLevel(lineClicked) & \
                        wx.stc.STC_FOLDLEVELHEADERFLAG:
                    if evt.GetShift():
                        self.SetFoldExpanded(lineClicked, True)
                        self.Expand(lineClicked, True, True, 1)
                    elif evt.GetControl():
                        if self.GetFoldExpanded(lineClicked):
                            self.SetFoldExpanded(lineClicked, False)
                            self.Expand(lineClicked, False, True, 0)
                        else:
                            self.SetFoldExpanded(lineClicked, True)
                            self.Expand(lineClicked, True, True, 100)
                    else:
                        self.ToggleFold(lineClicked)

    def FoldAll(self):
        lineCount = self.GetLineCount()
        expanding = True
        # find out if we are folding or unfolding
        for lineNum in range(lineCount):
            if self.GetFoldLevel(lineNum) & wx.stc.STC_FOLDLEVELHEADERFLAG:
                expanding = not self.GetFoldExpanded(lineNum)
                break
        lineNum = 0
        while lineNum < lineCount:
            level = self.GetFoldLevel(lineNum)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG and \
                    (level & wx.stc.STC_FOLDLEVELNUMBERMASK) == \
                         wx.stc.STC_FOLDLEVELBASE:
                if expanding:
                    self.SetFoldExpanded(lineNum, True)
                    lineNum = self.Expand(lineNum, True)
                    lineNum = lineNum - 1
                else:
                    lastChild = self.GetLastChild(lineNum, -1)
                    self.SetFoldExpanded(lineNum, False)
                    if lastChild > lineNum:
                        self.HideLines(lineNum+1, lastChild)
            lineNum = lineNum + 1

    def Expand(self, line, doExpand, force=False, visLevels=0, level=-1):
        lastChild = self.GetLastChild(line, level)
        line = line + 1

        while line <= lastChild:
            if force:
                if visLevels > 0:
                    self.ShowLines(line, line)
                else:
                    self.HideLines(line, line)
            else:
                if doExpand:
                    self.ShowLines(line, line)
            if level == -1:
                level = self.GetFoldLevel(line)
            if level & wx.stc.STC_FOLDLEVELHEADERFLAG:
                if force:
                    if visLevels > 1:
                        self.SetFoldExpanded(line, True)
                    else:
                        self.SetFoldExpanded(line, False)
                    line = self.Expand(line, doExpand, force, visLevels-1)
                else:
                    if doExpand and self.GetFoldExpanded(line):
                        line = self.Expand(line, True, force, visLevels-1)
                    else:
                        line = self.Expand(line, False, force, visLevels-1)
            else:
                line = line + 1
        return line


class RootWindow(wx.Frame):

    def __init__(self):
        #super(wx.Frame, self).__init__(None, -1, "Menu")
        wx.Frame.__init__(self,None, -1, "Menu")
        menu_exit_id = wx.NewId()
        self.SetMinSize((100,100))

        file_menu = wx.Menu()
        file_menu.Append(menu_exit_id, "Exit", "Exit")

        wx.EVT_MENU(self, menu_exit_id, self.exit)
        menu_bar = wx.MenuBar()
        menu_bar.Append(file_menu, "File")
        self.SetMenuBar(menu_bar)

        self.tab = wx.Notebook(self, -1)
        self.editor = TextEditor(self.tab, wx.ID_ANY)
        self.tab.AddPage(self.editor, "Codice")
        self.tab.AddPage(wx.StaticText(self.tab, -1, "ciccio"), "Costumi")
        self.editor2 = TextEditor(self, wx.ID_ANY)
        sizer = wx.GridBagSizer()
        self.stage = wxSDLWindow(self, wx.ID_ANY, size = (300,300))
        self.box = wx.StaticBox(self, wx.ID_ANY, size = (300,300))
        sizer.Add(self.box, (0,0))
        sizer.Add(self.tab, (0,1), span=(2,1), flag=wx.EXPAND)
        sizer.Add(self.editor2, (1,0), flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(1)
        sizer.AddGrowableRow(1)
        self.SetSizer(sizer)
        self.Layout()

    def exit(self, event):
        self.Close(True)


class Slither(wx.App):

    def OnInit(self):
        frame = RootWindow()
        frame.Show(True)
        #self.SetTopWindow(frame)
        return True

app = Slither()
app.MainLoop()
