import glfw


class JoyStickHandler(object):

    BUTTON_A = 0
    BUTTON_B = 1
    BUTTON_X = 2
    BUTTON_Y = 3
    BUTTON_LB = 4
    BUTTON_RB = 5
    BUTTON_OPT = 6
    BUTTON_MENU = 7
    BUTTON_L_STICK = 9
    BUTTON_R_STICK = 10
    BUTTON_UP = 11
    BUTTON_RIGHT = 12
    BUTTON_DOWN = 13
    BUTTON_LEFT = 14

    def __init__(self):
        self.stat = None
        self.button_stat = None
        self.cb_pressed = None

    def update(self):
        if glfw.joystick_present(glfw.JOYSTICK_1):
            self.stat = glfw.get_gamepad_state(glfw.JOYSTICK_1)

            if self.button_stat != self.stat.buttons:
                self.button_stat = self.stat.buttons

                if self.button_stat.count(1) == 1:
                    # check if only one button pressed
                    button_id = self.button_stat.index(1)  # get button id

                    if self.cb_pressed is not None:
                        self.cb_pressed(button_id)
        else:
            self.stat = None
            self.button_stat = None

    def is_presented(self):
        return glfw.joystick_present(glfw.JOYSTICK_1)
