import imp
import re
import sys
import traceback


START = 0
END = 1


class CodeSection(object):

    def __init__(self, code, offsets, deloopify=True):
        self.yield_inserted_lines = []
        self.original_code = code
        self.mangled_code = code
        self.offsets = offsets
        self.deloopify = deloopify
        if self.deloopify:
            self.deloopify()
        self.mangled_size = len(self.mangled_code.splitlines())
        self.offsets = (
            self.offsets[START], self.offsets[START] + self.mangled_size)

    def change_start_offset(self, increment):
        def incr(offset):
            return offset + increment
        self.yield_inserted_lines = map(incr, self.yield_inserted_lines)
        self.offsets = tuple(map(incr, self.offsets))

    def get_original_line(self, line):
        nyields = 0
        for yield_line in self.yield_inserted_lines:
            if line > yield_line:
                nyields += 1
        original_line = line - nyields - self.offsets[START] + 1
        return original_line

    @staticmethod
    def find_next_line(index, code_lines):
        if index is None:
            return None, None
        while index < len(code_lines) - 1:
            index = index + 1
            line = code_lines[index]
            if line != '':
                return index, line
        return None, None

    def deloopify(self):
        '''Inject a yield at the end of every loop

        '''
        code_lines = self.original_code.splitlines()
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
                        self.yield_inserted_lines.append(
                            index + self.offsets[START])
                        lines += 1
                        loops.pop(0)
                if line is None or index == lines - 1:
                    # print "End of file after loop"
                    # print "injecting yield in line %d" % (lines -1)
                    # dedent, end code block
                    code_lines.insert(lines, ' ' * loops[0] + "yield")
                    self.yield_inserted_lines.append(
                        lines + self.offsets[START])
                    loops.pop(0)
            index, line = self.find_next_line(index, code_lines)
        self.mangled_code = '\n'.join(code_lines)


class CodeHandler(object):

    def __init__(self, resources, element, module_name, user_code,
                 module_filename):
        self.module_name = module_name
        self.element = element
        self.resources = resources
        self.module_filename = module_filename
        self.generated_code = ''
        self.sections = {}
        self.user_code = user_code
        self.compile_error = False
        self.template = None
        self.set_template()
        self.module = None
        self.traceback_message = None
        self.traceback_line = None
        self.errored_section = None
        self.errored_line = None

        self.generate()

    def set_template(self):
        self.template = self.resources.selfsuff.get_template(self.element)

    def update_user_code(self, user_code):
        self.user_code = user_code
        self.generate()

    def find_section_line(self, line):
        for name, section in self.sections.items():
            if line >= section.offsets[START] and line <= section.offsets[END]:
                self.errored_section = name
                self.errored_section_line = section.get_original_line(line)
                break

    def handle_exception(self, exc_type, exc_value, exc_traceback, exc=None):
        if exc is not None:
            self.traceback_line = exc.lineno
        else:
            c_prev = exc_traceback
            c_cur = exc_traceback
            while c_cur is not None:
                c_prev = c_cur
                c_cur = c_cur.tb_next
            self.traceback_line = c_prev.tb_lineno
        self.traceback_message = traceback.format_exc()
        self.compile_error = True
        self.find_section_line(self.traceback_line)

    def generate(self):
        self.traceback_message = None
        self.traceback_line = None
        self.errored_section = None
        self.errored_line = None
        self.compile_error = False
        mangled_user_code = {}

        sections = self.resources.selfsuff.get_buffers_list(self.element)
        for section_name, options in sections.items():
            try:
                code = self.user_code[section_name]
            except KeyError:
                # Section does not exist in code
                continue
            try:
                offsets = (self.template.section_offset[section_name],)
            except KeyError:
                # section does not exist in template
                continue
            deloopify = options.get('deloopify', True)
            self.sections[section_name] = CodeSection(code, offsets,
                                                      deloopify=deloopify)
            mangled_user_code[section_name] = \
                self.sections[section_name].mangled_code
        # adjust offsets for all the successive sections
        for section in self.sections.values():
            start_offset = section.offsets[START]
            section_size = section.mangled_size
            for section in self.sections.values():
                if section.offsets[END] > start_offset:
                    # -1 because the jinjia token is replaced and doesn't count
                    section.change_start_offset(section_size - 1)

        self.generated_code = self.template.render(mangled_user_code)
        with open(self.module_filename, "w") as module_file:
            module_file.write(self.generated_code)

        try:
            self.module = imp.load_source(self.module_name,
                                          self.module_filename)
        except Exception as exc:
            self.module = None
            exc_type, exc_value, exc_traceback = sys.exc_info()
            if exc_type == SyntaxError:
                self.handle_exception(exc_type, exc_value, exc_traceback,
                                      exc=exc)
            sys.excepthook(exc_type, exc_value, exc_traceback)

        finally:
            try:
                del exc_traceback
            except Exception:
                pass

        if not self.compile_error:
            sys.modules[self.module_name] = self.module
