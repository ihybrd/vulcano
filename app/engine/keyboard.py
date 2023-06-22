import glfw


class KeyboardHandler(object):

    def __init__(self):
        self.mode = 0

        # stat
        self.pressed = False
        self.pressing = False
        self.released = True

        # collection of keys being used simultaneously
        # eg: s/d in wasd pressing together
        self.keys = []

    def key_pressed(self, win, *args):
        """this function will be linked to glutKeyboardFunc"""
        key, scancode, action, mode = args

        self.pressed = True if action == 1 else False
        self.pressing = True if action == 2 else False
        self.released = True if action == 0 else False

        # use 'TAB' key to switch between wasd mode and command mode.
        if key == glfw.KEY_TAB:
            if self.pressed:
                self.mode = 0 if self.mode else 1
        else:
            # detecting if keys are being pressed at the same time.
            if self.pressed:
                self.keys.append(key)
            elif self.released:
                self.keys.remove(key)
