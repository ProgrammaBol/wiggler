import imp
import jinja2
import py_compile
import re
import sys
import traceback
import wx
import wx.py



from editor import TextEditor
from stage import Stage
import pyflakes.checker as pyflakes

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
        self.tab.AddPage(wx.StaticText(self.tab, -1, "Costumes"), "Costumes")
        self.sprites = wx.ListCtrl(self)
        self.sprites.InsertImageItem(0,0)
        self.sprites.InsertImageItem(1,0)
        self.sprites.InsertImageItem(2,0)
        #self.tools = wx.ToolBar(self, -1, size = (10, 40))
        self.tools = self.CreateToolBar()
        play_image_bitmap =  wx.Bitmap('resources/images/play.png')
        play_image = wx.ImageFromBitmap(play_image_bitmap)
        play_image_scaled = play_image.Scale(30,30, wx.IMAGE_QUALITY_HIGH)
        play_image = wx.BitmapFromImage(play_image_scaled)
        playtool = self.tools.AddLabelTool(wx.ID_ANY, 'Play', play_image)
        self.Bind(wx.EVT_TOOL, self.play, playtool)
        stop_image_bitmap =  wx.Bitmap('resources/images/stop.png')
        stop_image = wx.ImageFromBitmap(stop_image_bitmap)
        stop_image_scaled = stop_image.Scale(30,30, wx.IMAGE_QUALITY_HIGH)
        stop_image = wx.BitmapFromImage(stop_image_scaled)
        stoptool = self.tools.AddLabelTool(wx.ID_ANY, 'stop', stop_image)
        self.tools.Realize()
        self.shell = wx.py.crust.Crust(parent=self)
        self.shell.Show()
        self.basket_classes = wx.ListCtrl(self, wx.ID_ANY, size = (200,300), style=wx.LC_REPORT)
        self.basket_classes.InsertColumn(0,"Classes")
        self.basket_classes.InsertStringItem(0, "Movement")
        self.basket_classes.InsertStringItem(1, "Stage")
        self.basket_functions = wx.ListCtrl(self, wx.ID_ANY, size = (200,300))
        sizer = wx.GridBagSizer()
        self.stage = Stage(self, wx.ID_ANY, size = (300,300))
        self.box = wx.StaticBox(self, wx.ID_ANY, size = (300,300))
        sizer.Add(self.stage, (0,0))
        sizer.Add(self.basket_classes, (0,1), span=(1,1))
        sizer.Add(self.basket_functions, (1,1), span=(1,1), flag=wx.EXPAND)
        sizer.Add(self.tab, (0,2), span=(2,1), flag=wx.EXPAND)
        sizer.Add(self.sprites, (1,0), flag=wx.EXPAND)
        sizer.Add(self.shell, (2,0), span=(1,3),  flag=wx.EXPAND)
        sizer.Fit(self)
        sizer.AddGrowableCol(2)
        sizer.AddGrowableRow(2)
        self.SetSizer(sizer)
        self.Layout()


    def find_next_line(self, index, split_raw_code):
        if index is None:
            return None, None
        while index < len(split_raw_code) - 1:
            index = index + 1
            line = split_raw_code[index]
            if line != '':
                return index, line
        return None, None


    def play(self, event):
        raw_code = self.editor.GetText()
        split_raw_code = raw_code.splitlines()
        lines = len(split_raw_code)
        print split_raw_code
        index = -1
        loops = [None]
        indent = 0
        index, line = self.find_next_line(index, split_raw_code)
        while line:
            print "line %d"
            print line
            m = re.match("(\s*)(for|while)", line)
            if m:
                print "match found on line %d" % index
                index, line = self.find_next_line(index, split_raw_code)
                m = re.match("(\s*)(.+)", line)
                print "first loop line %d - %s " % (index, line)
                loops.insert(0, len(m.groups()[0]))
                print "loop block indentation %d" % loops[0]
                index, line = self.find_next_line(index, split_raw_code)
            if loops[0]:
                if line:
                    m = re.match("(\s*)(.*)", line)
                    indent = len(m.groups()[0])
                    print "indent %d" % indent
                    next_index = index + 1
                    if indent < loops[0]:
                        print "dedent from %d to %d on line %d" % (loops[0], indent, index)
                        print "injecting yield in line %d" % index
                        # dedent, end code block
                        split_raw_code.insert(index, ' '* loops[0] + "yield")
                        lines += 1
                        loops.pop(0)
                if line is None or index == lines - 1:
                    print "End of file after loop"
                    print "injecting yield in line %d" % (lines -1)
                    # dedent, end code block
                    split_raw_code.insert(lines , ' '* loops[0] + "yield")
                    loops.pop(0)
            index, line = self.find_next_line(index, split_raw_code)

        indented_code = '\n'.join(map(lambda s: re.sub("^"," "*8,s), split_raw_code))
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("core/templates"))
        template = env.get_template("element.j2")
        element_code = template.render(class_name="example", indented_code=indented_code)
        print element_code
        #try:
        tree = compile(element_code, "test.py", "exec")
        with open('/tmp/element.py',"w+") as element_file:
            element_file.write(element_code)
        #except:
        #    exc_type, exc_value, exc_traceback = sys.exc_info()
        #    print exc_value.lineno
        #finally:
        #    try:
        #        del exc_traceback
        #    except:
        #        pass
        self.stage.clear()
        self.stage.add_elements('example')

    def exit(self, event):
        self.Close(True)
