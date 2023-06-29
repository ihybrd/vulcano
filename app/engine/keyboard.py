import glfw


class KeyboardHandler(object):
    shift_key_char = {
        # glfw.KEY_GRAVE_ACCENT:"~",  # this key used for WASD entry
        glfw.KEY_1: "!",
        glfw.KEY_2: "@",
        glfw.KEY_3: "#",
        glfw.KEY_4: "$",
        glfw.KEY_5: "%",
        glfw.KEY_6: "^",
        glfw.KEY_7: "&",
        glfw.KEY_8: "*",
        glfw.KEY_9: "(",
        glfw.KEY_0: ")",
        glfw.KEY_MINUS: "_",
        glfw.KEY_EQUAL: "+",
        glfw.KEY_LEFT_BRACKET: "{",
        glfw.KEY_RIGHT_BRACKET: "}",
        glfw.KEY_BACKSLASH: "|",
        glfw.KEY_SEMICOLON: ":",
        glfw.KEY_APOSTROPHE: '"',
        glfw.KEY_COMMA: "<",
        glfw.KEY_PERIOD: ">",
        glfw.KEY_SLASH: "?"
    }

    def __init__(self):
        # self.cam_mode = 0
        # self.cmd_mode = 0
        for cap_chr in "ABCDEFGHIJKLMNOPQRSTUVWXYZ":
            KeyboardHandler.shift_key_char[glfw.__dict__['KEY_'+cap_chr]] = cap_chr

        # stat
        self.pressed = False
        self.pressing = False
        self.released = True

        # collection of keys being used simultaneously
        # eg: s/d in wasd pressing together
        self.char = None
        self.key = None
        self.keys = []

    def set_key(self, win, *args):
        """this function will be linked to glutKeyboardFunc"""
        key, scancode, action, mode = args

        self.pressed = True if action == 1 else False
        self.pressing = True if action == 2 else False
        self.released = True if action == 0 else False

        self.key = key
        key_name = glfw.get_key_name(key, scancode)

        if self.pressed and key_name is not None:
            if mode == glfw.MOD_SHIFT:
                self.char = KeyboardHandler.shift_key_char[key]
            else:
                self.char = str(glfw.get_key_name(key, scancode))

        if self.pressed:
            self.keys.append(key)
        elif self.released:
            self.keys.remove(key)

