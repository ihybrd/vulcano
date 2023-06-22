import app.engine.mouse as mouse
import app.engine.keyboard as keyboard
import app.engine.joystick as joystick


class InputStateManager(object):

    def __init__(self):
        self.mouse_handler = mouse.MouseHandler()
        self.joystick_handler = joystick.JoyStickHandler()
        self.keyboard_handler = keyboard.KeyboardHandler()

        self.is_joystick_mode = True

    def update(self):
        self.mouse_handler.update()
        self.joystick_handler.update()

        self.input_stat_switch()

    def input_stat_switch(self):
        if self.joystick_handler.is_presented():
            if not self.is_joystick_mode:
                has_button_pressed = any(self.joystick_handler.stat.buttons)
                has_joystick_moved = any([0 if abs(a)<.1 else a for a in self.joystick_handler.stat.axes[:4]])
                has_trigger_pressed = any([True if a>-1.0 else False for a in self.joystick_handler.stat.axes[4:]])
                self.is_joystick_mode = any([has_button_pressed, has_joystick_moved, has_trigger_pressed])

            else:
                if self.mouse_handler.stat or self.keyboard_handler.keys:
                    self.is_joystick_mode = False

    def load_camera_data(self):
        move_x, move_y, move_z = 0,0,0
        if self.is_joystick_mode:
            L_h, L_v, R_h, R_v, L_tr, R_tr = self.joystick_handler.stat.axes

            # rotate cam
            R_v = 0 if abs(R_v)<0.1 else R_v*1.5
            R_h = 0 if abs(R_h)<0.1 else R_h*1.5
            rot_x, rot_y = R_h*1.5, R_v*1.5

            # move cam
            L_v = 0 if abs(L_v)<0.1 else L_v
            L_h = 0 if abs(L_h)<0.1 else L_h
            L_tr = (L_tr + 1.0) * 0.5
            R_tr = (R_tr + 1.0) * 0.5

            if not L_v:
                move_x = 0
            else:
                move_x += L_v*(-.1)

            if not L_h:
                move_z = 0
            else:
                move_z += L_h*.1

            if not L_tr and not R_tr:
                move_y = 0
            elif L_tr:
                move_y -= L_tr*.1
            elif R_tr:
                move_y += R_tr*.1
        else:
            rot_x, rot_y = self.mouse_handler.dx, self.mouse_handler.dy

            move_speed = 0.05
            if 87 in self.keyboard_handler.keys:
                move_x += move_speed  # w
            if 83 in self.keyboard_handler.keys:
                move_x -= move_speed  # s
            if 65 in self.keyboard_handler.keys:
                move_z -= move_speed  # a
            if 68 in self.keyboard_handler.keys:
                move_z += move_speed  # d
            if 81 in self.keyboard_handler.keys:
                move_y -= move_speed  # q
            if 69 in self.keyboard_handler.keys:
                move_y += move_speed  # e
            if not self.keyboard_handler.keys:
                move_x, move_y, move_z = 0, 0, 0
        return move_x, move_y, move_z, rot_x, rot_y