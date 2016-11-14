import re


class CodeGenerator(object):

    def __init__(self, template, user_code):
        self.template = template
        self.sections = {}
        for section, code in user_code.items():
            self.sections[section] = self.deloopify(code)
        self.generated = self.generate_class_code()

    def generate_class_code(self):
        return self.template.render(self.sections)

    def find_next_line(self, index, code_lines):
        if index is None:
            return None, None
        while index < len(code_lines) - 1:
            index = index + 1
            line = code_lines[index]
            if line != '':
                return index, line
        return None, None

    def deloopify(self, code):
        '''
        Inject a yield at the end of every loop
        '''
        code_lines = code.splitlines()
        lines = len(code_lines)
        index = -1
        loops = [None]
        indent = 0
        index, line = self.find_next_line(index, code_lines)
        while line:
            m = re.match("(\s*)(for|while)", line)
            if m:
                # print "match found on line %d" % index
                index, line = self.find_next_line(index, code_lines)
                m = re.match("(\s*)(.+)", line)
                # print "first loop line %d - %s " % (index, line)
                loops.insert(0, len(m.groups()[0]))
                # print "loop block indentation %d" % loops[0]
                index, line = self.find_next_line(index, code_lines)
            if loops[0]:
                if line:
                    m = re.match("(\s*)(.*)", line)
                    indent = len(m.groups()[0])
                    # print "indent %d" % indent
                    if indent < loops[0]:
                        # template = "dedent from %d to %d on line %d"
                        # print template % (loops[0], indent, index)
                        # print "injecting yield in line %d" % index
                        # dedent, end code block
                        code_lines.insert(index, ' ' * loops[0] + "yield")
                        lines += 1
                        loops.pop(0)
                if line is None or index == lines - 1:
                    # print "End of file after loop"
                    # print "injecting yield in line %d" % (lines -1)
                    # dedent, end code block
                    code_lines.insert(lines, ' ' * loops[0] + "yield")
                    loops.pop(0)
            index, line = self.find_next_line(index, code_lines)
        return '\n'.join(code_lines)
