import wx

from wiggler.ui.editor import TextEditor


class CodePane(wx.Notebook):

    def __init__(self, parent, resources, events):
        wx.Notebook.__init__(self, parent)
        self._buffers = {}
        self.events = events
        self.resources = resources
        self.active_sprite = None
        self.events.subscribe(
            self, ['reload', 'actsprite', 'preplay', 'projload', 'traceback',
                   'selfsuff_change'])
        self.Bind(self.events.EVT_NOTICE, self.notice_handler)

    def notice_handler(self, event):
        if event.notice == 'reload':
            self.reload()
        if event.notice == 'projload':
            self.reload()
        elif event.notice == 'selfsuff_change':
            self.save_active_buffers()
            self.set_sprite_code_buffers(self.active_sprite)
        elif event.notice == 'actsprite':
            self.save_active_buffers()
            self.set_sprite_code_buffers(event.data.sprite_builder)
        elif event.notice == 'preplay':
            self.save_active_buffers()
        elif event.notice == 'traceback':
            if event.data.code_handler is not None:
                self.handle_traceback(event.data.code_handler)
        event.Skip()

    def set(self, buffer_name, text, readonly=False):
        if buffer_name not in self._buffers:
            editor = TextEditor(self, wx.ID_ANY, readonly=readonly)
            self._buffers[buffer_name] = editor
            self.AddPage(editor, buffer_name)
        editor = self._buffers[buffer_name]
        editor.set_buffer(text)

    def clear(self, buffer_name=None):
        if buffer_name is not None:
            editors = [self._buffers[buffer_name]]
        else:
            editors = self._buffers.values()
        for ed in editors:
            ed.Clear()

    def set_sprite_code_buffers(self, sprite_builder):
        self.active_sprite = sprite_builder
        self.reload()
        buffers = \
            self.resources.selfsuff.get_buffers_list('sprite')
        # TODO: add the possibilty to show all user_code, with
        # the ones outside of selfsuff set as read-only
        for buffer_name in buffers:
            try:
                buffer_text = sprite_builder.user_code[buffer_name]
            except KeyError:
                # FIXME: find a better place to fill a
                # missing user_code section
                buffer_text = sprite_builder.user_code[buffer_name] = ''
            self.set(buffer_name, buffer_text)
        text = sprite_builder.code_handler.generated_code
        self.set("generated_code", text, readonly=True)
        # TODO(panda), get a list of sprite attributes
        # for index, attrib in enumerate(dir(MovingSprite)):
        #    self.basket_functions.InsertStringItem(index, attrib)
        # self.basket_functions.DeleteAllItems()

    def handle_traceback(self, code_handler):
        traceback_line = code_handler.traceback_line
        errored_section = code_handler.errored_section
        errored_line = code_handler.errored_section_line
        self._buffers["generated_code"].mark_error(traceback_line)
        self._buffers[errored_section].mark_error(errored_line)

    def save_active_buffers(self):
        new_user_code = {}
        sprite_builder = self.active_sprite
        if sprite_builder is None:
            return
        for buffer_name, buffer_editor in self._buffers.items():
            if buffer_name != "generated_code":
                new_user_code[buffer_name] = buffer_editor.GetText()
        sprite_builder.update_user_code(new_user_code)
        self.set("generated_code", sprite_builder.code_handler.generated_code)
        if sprite_builder.code_handler.compile_error:
            self.handle_traceback(sprite_builder.code_handler)
        else:
            for editor in self._buffers.values():
                editor.clear_errors()

    def reload(self):
        self.DeleteAllPages()
        self._buffers = {}
