import glfw

class CommandLine:

    def __init__(self):
        self.cmd_mode = 0

        self.input = ""
        self.output = ""
        self.command_list = []

        self.cursor_pos = 0
        self.cmd_ptr_pos = 0

    def execute(self, cmd):
        print(cmd)

    def pressed(self, key, char):
        if key in [glfw.KEY_TAB, glfw.KEY_GRAVE_ACCENT]:
            return

        if key == glfw.KEY_ENTER:
            if self.input:
                self.execute(self.input)
                self.command_list.append(self.input)
                self.cmd_ptr_pos += 1
                self.input = ""
        elif key == glfw.KEY_LEFT:
            if self.cursor_pos > 0:
                self.cursor_pos -= 1
        elif key == glfw.KEY_RIGHT:
            if self.cursor_pos < len(self.input):
                self.cursor_pos += 1
        elif key == glfw.KEY_UP:
            if self.cmd_ptr_pos > 0:
                self.cmd_ptr_pos -= 1
                self.input = self.command_list[self.cmd_ptr_pos]
        elif key == glfw.KEY_DOWN:
            if self.cmd_ptr_pos < len(self.command_list)-1:
                self.cmd_ptr_pos += 1
                self.input = self.command_list[self.cmd_ptr_pos]
        elif key == glfw.KEY_BACKSPACE:
            if len(self.input) >= 0:
                in1 = self.input[:self.cursor_pos]
                in2 = self.input[self.cursor_pos:] if self.cursor_pos < len(self.input) else ""
                if len(in1) > 0:
                    in1 = in1[:-1]
                    self.input = in1 + in2
                    self.cursor_pos -= 1
        elif key == glfw.KEY_ESCAPE:
            self.input = ""
        else:
            if len(self.input) >= 0:
                in1 = self.input[:self.cursor_pos]
                in2 = self.input[self.cursor_pos:] if self.cursor_pos < len(self.input) else ""
                self.input = in1 + char + in2
                self.cursor_pos += 1
