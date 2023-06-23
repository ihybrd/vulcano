import app.utils.cgmath as cgmath
import pyrr
import numpy as np

class BaseCamera(object):

    def __init__(self):
        self.angle_of_view = 60
        self.__pos = None
        self.__view = None

    def pos(self):
        return self.__pos

    def view(self):
        return self.__view


class Camera(BaseCamera):

    MOVE = 0
    ZOOM = 1
    ZOOM_WHL = 2

    def __init__(self):
        super(Camera, self).__init__()

        self.V = cgmath.Vector4(0, 0, -10, 1)
        self.T = cgmath.Matrix4x4()
        self.V.to_matrix().multiply(self.T).print_matrix()

        self.rx = 0
        self.ry = 0
        self.z = 0

        self.look_x = 0.
        self.look_y = 0.
        self.look_z = 0.

        self.dist_factor = 1

        self.__pos = self.V.to_list()
        self.__view = None

        self.__dx, self.__dy, self.__dist = 0, 0, 1
        self.__last = None

    def look_at(self, x, y, z):
        self.look_x = x
        self.look_y = y
        self.look_z = z

    def __rot_cam(self, dx, dy):
        self.ry += dx
        if -90 <= self.rx + dy <= 90:
            self.rx -= dy
        elif self.rx + dy > 90:
            self.rx = 85
        elif self.rx + dy < -90:
            self.rx = -85

    def __zoom_cam(self, dx):
        if self.dist_factor - dx / 100.0 <= 0.1:
            self.dist_factor = 0.1
        else:
            self.dist_factor -= dx / 100.0

    def pos(self):
        return self.__pos

    def view(self):
        return self.__view

    def update(self, dx, dy, zoom):
        # calculate ry, rx rotation value
        self.__rot_cam(dx, dy)

        if dx != 0: self.__dx = dx
        if dy != 0: self.__dy = dy

        # calculate zoom in/out
        self.__zoom_cam(zoom)

        rx = -self.rx
        ry = -self.ry

        # matrix for camera rotating around Y axis
        T_p = self.T.transform(
            0, 0, 0,
            0, ry,0,
            1, 1, 1
        )
        # matrix for camera rotating up-down around X axis [-90, 90]
        T_c = self.T.transform(
            0, 0, 0,
            rx,0, 0,
            1, 1, 1
        )

        # get final matrix
        T = T_c.multiply(T_p)
        x, y, z, w = self.V.to_matrix().multiply(T).to_list()
        x *= self.dist_factor
        y *= self.dist_factor
        z *= self.dist_factor

        position = np.array([x, y, z], dtype=np.float32)
        target = np.array([self.look_x, self.look_y, self.look_z],dtype=np.float32)
        up = np.array([0, 1, 0], dtype=np.float32)
        view = pyrr.matrix44.create_look_at(position, target, up, dtype=np.float32)

        self.__pos = [x, y, z]
        self.__view = view


class CameraWasd(BaseCamera):

    def __init__(self):
        super(CameraWasd, self).__init__()

        self.look_dir = cgmath.Vector4(0, 0, 1, 1)
        # self.tar_pos = [0,0,1,1]
        self.V = cgmath.Vector4(0, 0, 0, 1)
        self.T = cgmath.Matrix4x4()

        self.rx = 0
        self.ry = 0
        self.z = 0

        self.look_x = 1.
        self.look_y = 1.
        self.look_z = 1.

        self.__pos = self.V.to_list()
        self.__view = None

        self.__dx, self.__dy, self.__dist = 0, 0, 1

        self.move_x = 0
        self.move_y = 0
        self.move_z = 0

    def __rot_cam(self, dx, dy, speed=1.):
        self.ry += dx*speed
        if -90 <= self.rx + dy <= 90:
            self.rx -= dy*speed
        elif self.rx + dy > 90:
            self.rx = 85
        elif self.rx + dy < -90:
            self.rx = -85

    def pos(self):
        return self.__pos

    def set_pos(self, pos):
        self.__pos = pos

    def set_rot(self, rx, ry):
        self.rx = rx
        self.ry = ry

    def view(self):
        return self.__view

    def update(self, move_x, move_y, move_z, rot_x, rot_y):
        self.move_x = move_x
        self.move_y = move_y
        self.move_z = move_z

        self.__rot_cam(rot_x, rot_y)

        rx = -self.rx
        ry = -self.ry

        # print rx, ry
        # matrix for camera rotating around Y axis
        T_p = self.T.transform(
            0, 0, 0,
            0, ry,0,
            1, 1, 1
        )
        # matrix for camera rotating up-down around X axis [-90, 90]
        T_c = self.T.transform(
            0, 0, 0,
            rx,0, 0,
            1, 1, 1
        )

        T_pos = self.T.transform(
            self.__pos[0], self.__pos[1], self.__pos[2],
            0, 0, 0,
            1, 1, 1
        )

        # get final matrix
        T = T_c.multiply(T_p.multiply(T_pos))

        # get current position
        x, y, z, w = self.V.to_matrix().multiply(T).to_list()
        # get look target position
        tar_x, tar_y, tar_z, _ = self.look_dir.to_matrix().multiply(T).to_list()

        # get vector from target(x) to v_pos(o), x is where camera is pointing.
        # while y is up.
        #
        # y
        # |  z
        # | /
        # .o ___ x
        #
        vecx = tar_x - x
        vecy = tar_y - y
        vecz = tar_z - z
        lookdir = cgmath.Vector4(vecx, vecy, vecz, 0)

        # get vector of side direction movement (o-z), x is where camera is
        # pointing while y is up.
        #
        # y
        # |  z
        # | /
        # .o ___ x
        #
        lookdir90 = lookdir.cross(cgmath.Vector4(0, 1, 0, 0))

        # offset calculation
        offset_x = lookdir.x * self.move_x + lookdir90.x * self.move_z
        offset_y = self.move_y + lookdir.y * self.move_x
        offset_z = lookdir.z * self.move_x + lookdir90.z * self.move_z

        # view position with offset
        vp = [
            x + offset_x,
            y + offset_y,
            z + offset_z
        ]

        # look target position with offset
        tp = [
            tar_x + offset_x,
            tar_y + offset_y,
            tar_z + offset_z
        ]

        position = np.array([vp[0], vp[1], vp[2]], dtype=np.float32)
        target = np.array([tp[0], tp[1], tp[2]], dtype=np.float32)
        up = np.array([0, 1, 0], dtype=np.float32)
        view = pyrr.matrix44.create_look_at(position, target, up, dtype=np.float32)

        self.__pos = vp
        self.__view = view

