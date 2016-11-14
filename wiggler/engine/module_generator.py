import imp
import sys
# import traceback


# TODO: implement traceback lineno reporting
class ModuleGenerator(object):

    def __init__(self, name, class_code):
        self.name = name
        self.class_code = class_code

    def generate(self):
        # try:
        compile(self.class_code, "test.py", "exec")
        self.module = imp.new_module(self.name)
        exec(self.class_code) in self.module.__dict__
        sys.modules[self.name] = self.module
        return sys.modules[self.name]
        # except:
        #    exc_type, exc_value, exc_traceback = sys.exc_info()
        #    print exc_value.lineno
        # finally:
        #    try:
        #        del exc_traceback
        #    except:
        #        pass
