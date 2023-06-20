class MouseHandler(object):

    # buttons = {
    #     0: "left button",
    #     2: "mid button",
    #     1: "right button"
    # }
    #
    # stat = {
    #     1: "pressed",
    #     0: "released"
    # }

    def __init__(self):
        self.pos_x, self.pos_y = 0, 0
        self.last_x, self.last_y = -1, -1
        self.dx, self.dy = 0, 0

        self.stat = 0  # release by default
        self.button = 0

        self.dy_whl = 0

    def mouse_pressed(self, win, button_id, press_stat, xx):
        self.button = button_id
        self.stat = press_stat

        if press_stat == 0:  # released
            self.last_x, self.last_y = -1, -1
            # self.dx, self.dy = 0, 0

            # print "%s, %s" % (button_id, press_stat)

    def mouse_move(self, win, x, y):
        # DEBUG
        # print "move:", x, y, "from: ", self.last_x, self.last_y
        # print self.stat
        if self.stat == 0:
            return

        if self.last_x == -1 or self.last_y == -1:
            self.last_x, self.last_y = x, y

        self.dx = x - self.last_x
        self.dy = y - self.last_y

        self.last_x, self.last_y = x, y

    def mouse_wheel(self, win, x, y):
        self.dy_whl = y

    def update(self):
        # de-acc for mouse delta value after mouse releasing
        if abs(self.dx) > 0.05:
            self.dx /= 1.1
        else:
            self.dx = 0

        if abs(self.dy) > 0.05:
            self.dy /= 1.1
        else:
            self.dy = 0

        if abs(self.dy_whl) > 0.1:
            self.dy_whl /= 1.1
        else:
            self.dy_whl = 0
