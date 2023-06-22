# triangulate quad
# https://notes.underscorediscovery.com/obj-parser-easy-parse-time-triangulation/
#
# split normal
# http://www.opengl-tutorial.org/intermediate-tutorials/tutorial-9-vbo-indexing/
import app.utils.cgmath as cgmath


class OBJImporter(object):

    def __init__(self):
        self.vertex_poscol_list = []
        self.vertex_norm_list = []
        self.vertex_coord_list = []
        self.vertex_tan_list = []

        self.verts_attr_combine = {}  # {"1/2/3": 9, ...}
        self.indices = []

    def __get_triangle_attr(self, tri):
        for attr_combine in tri:
            # if similar triangle vert not in the vbo
            if attr_combine not in self.verts_attr_combine:
                ind = len(self.indices)
                self.verts_attr_combine[attr_combine] = ind
                self.indices.append(ind)
            else:
                self.indices.append(self.verts_attr_combine[attr_combine])

    def load(self, obj_path):
        # for line in _obj_hard.split("\n"):
        with open(obj_path, 'r') as f:
            c = f.read()

        for line in c.split("\n"):
            # print line
            if line.startswith("v "):  # vertex position vector
                components = line.split(" ", 1)[1].split()
                if len(components) == 3:
                    x, y, z = [round(float(i), 6) for i in components]
                    r, g, b = .0, .0, .0
                elif len(components) == 6:  # with vertex color
                    x, y, z, r, g, b = [round(float(i), 6) for i in components]
                else:
                    x, y, z, r, g, b = [0.0, 0.0, 0.0, 0.0, 0.0 ,0.0]

                self.vertex_poscol_list.append([x, y, z, r, g, b])
            elif line.startswith("vn "):  # vertex normal vector
                x, y, z = [round(float(i), 6) for i in line.split(" ", 1)[1].split()]
                self.vertex_norm_list.append([x, y, z])
            elif line.startswith("vt "):  # vertex normal vector
                u, v = [round(float(i), 6) for i in line.split(" ", 1)[1].split()]
                self.vertex_coord_list.append([u, v])
            elif line.startswith("f "):  # face : v(vert) / vt(tex) / vn(norm)
                verts = line.split(" ", 1)[1].split()

                # TODO: ngon is not considered for now.
                if len(verts) == 3:
                    tri1 = verts
                    for tri in [tri1]:
                        self.__get_triangle_attr(tri)
                elif len(verts) == 4:
                    tri1 = verts[:3]
                    tri2 = [verts[0]]+verts[2:]

                    # IGNORE EXISTING VERTS WITH SAME ATTRS
                    for tri in [tri1, tri2]:
                        self.__get_triangle_attr(tri)

        verts_attr_combine_ivs = {}
        for k in self.verts_attr_combine:
            verts_attr_combine_ivs[self.verts_attr_combine[k]] = k
        # print "ivs", verts_attr_combine_ivs

        __vt = []
        __vn = []
        __uv = []
        __tg = []

        for i in range(0, len(self.indices), 3):

            verts = []
            uvs = []

            for j in [self.indices[i], self.indices[i+1], self.indices[i+2]]:
                _vt, _uv, _vn = verts_attr_combine_ivs[j].split("/")
                __vt.append(self.vertex_poscol_list[int(_vt) - 1])
                __vn.append(self.vertex_norm_list[int(_vn) - 1])
                __uv.append(self.vertex_coord_list[int(_uv) - 1])
                # __col.append(self.vertex_col_list[int(_col) - 1])

                verts.append(self.vertex_poscol_list[int(_vt) - 1])
                uvs.append(self.vertex_coord_list[int(_uv) - 1])

            # print "vertex pos", self.vertex_pos_list[int(_vt) - 1]
            # print "vertex uv", self.vertex_coord_list[int(_uv) - 1]

            # get tangent vector
            vt1, vt2, vt3 = verts
            uv1, uv2, uv3 = uvs

            egde1 = [vt2[0]-vt1[0], vt2[1]-vt1[1], vt2[2]-vt1[2]]
            egde2 = [vt3[0]-vt1[0], vt3[1]-vt1[1], vt3[2]-vt1[2]]
            delta_uv1 = [uv2[0]-uv1[0], uv2[1]-uv1[1]]
            delta_uv2 = [uv3[0]-uv1[0], uv3[1]-uv1[1]]

            # print delta_uv1
            # print delta_uv2
            if (delta_uv1[0] * delta_uv2[1] - delta_uv2[0] * delta_uv1[1]) != 0:
                f = 1.0 / (delta_uv1[0] * delta_uv2[1] - delta_uv2[0] * delta_uv1[1])
                tangent_x = f * (delta_uv2[1] * egde1[0] - delta_uv1[1] * egde2[0])
                tangent_y = f * (delta_uv2[1] * egde1[1] - delta_uv1[1] * egde2[1])
                tangent_z = f * (delta_uv2[1] * egde1[2] - delta_uv1[1] * egde2[2])
            else: # fix divided by 0 issue
                tangent_x, tangent_y, tangent_z = 0., 1., 0.
            vec3_tan = cgmath.Vector(tangent_x, tangent_y, tangent_z)
            tangent = list(vec3_tan.normalized().to_list())

            # append three times for three vertex
            __tg.append(tangent)
            __tg.append(tangent)
            __tg.append(tangent)

        r = []
        # for f in full_attr_list:
        for i in range(len(__vt)):

            # the order of adding vertex info here is very important,
            # msh.set_attrib(attrib_id..) must be same with the order below

            # notes: __vt contains position and color
            # r += __vt[i] + __vn[i] + __tg[i] + __uv[i]
            r += __vt[i] + __uv[i]

        return r, self.indices

