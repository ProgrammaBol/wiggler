import imp
import jinja2
import re
import sys
import traceback

class SpriteElement(object):

    def __init__(self, name):
        self.name = name
        self.raw_code = ''

    def create_module(self):
        split_raw_code = self.complete_code()
        indented_code = '\n'.join(map(lambda s: re.sub("^"," "*8,s), split_raw_code))
        env = jinja2.Environment(loader=jinja2.FileSystemLoader("core/templates"))
        template = env.get_template("element.j2")
        self.element_code = template.render(class_name="example", indented_code=indented_code)
        print self.element_code
        #try:
        tree = compile(self.element_code, "test.py", "exec")
        self.module = imp.new_module(self.name)
        exec self.element_code in self.module.__dict__
        sys.modules[self.name] = self.module
        #except:
        #    exc_type, exc_value, exc_traceback = sys.exc_info()
        #    print exc_value.lineno
        #finally:
        #    try:
        #        del exc_traceback
        #    except:
        #        pass

    def find_next_line(self, index, split_raw_code):
        if index is None:
            return None, None
        while index < len(split_raw_code) - 1:
            index = index + 1
            line = split_raw_code[index]
            if line != '':
                return index, line
        return None, None


    def complete_code(self):

        split_raw_code = self.raw_code.splitlines()
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
        return split_raw_code

