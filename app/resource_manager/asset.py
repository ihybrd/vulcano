import numpy as np
import assimp_py
import app.utils.objimporter as objimporter

class Asset:
    def __init__(self):
        self.obj = "bunny" # bunny or cube
        self.use_mesh = True

    def load_mesh_OBJimporter(self):
        obj = objimporter.OBJImporter()
        v, i = obj.load("../sample_data/{0}.obj".format(self.obj))
        return np.array(v, dtype = np.float32), i

    def load_mesh_assimp(self):
        process_flags = (assimp_py.Process_Triangulate | assimp_py.Process_CalcTangentSpace)
        scene = assimp_py.ImportFile("../sample_data/{0}.obj".format(self.obj), process_flags)
        m = scene.meshes[0]

        vertices = []
        for id, verts in enumerate(m.vertices):
            vertices += list(verts)+[1,1,1]+list(m.normals[id])+list(m.tangents[id])+[0,0] # vert, color, uv
        indices = []
        for i in m.indices:
            indices += list(i)

        return np.array(vertices, dtype=np.float32), indices

    def load_triangle(self):
        vertices = np.array(
           [
                0.0, -0.1, 0, 0.0, 1.0, 0.0,  0,0,1,0,0,0,  0.5, 0.0,  # 0
                0.1, 0.1, 0, 0.0, 1.0, 0.0,   0,0,1,0,0,0,  1.0, 1.0,  # 1
                -0.1, 0.1, 0, 0.0, 1.0, 0.0,  0,0,1,0,0,0,  0.0, 1.0   # 2
           ], dtype=np.float32
        )
        indices = [0, 1, 2]
        return vertices, indices

    def load_square(self):
        vertices = np.array(
           [
                -0.1, 0.1, 0, 1.0, 0.0, 0.0,   0,0,1,0,0,0,    0.0, 1.0,  # 0
                -0.1, -0.1, 0, 1.0, 0.0, 0.0,  0,0,1,0,0,0,    0.0, 0.0,  # 1
                0.1, -0.1, 0, 1.0, 0.0, 0.0,   0,0,1,0,0,0,    1.0, 0.0,  # 2
                0.1, 0.1, 0, 1.0, 0.0, 0.0,    0,0,1,0,0,0,    1.0, 1.0,  # 3
           ], dtype=np.float32
        )
        indices = [
            0, 1, 2,
            2, 3, 0
        ]
        return vertices, indices

    def load_star(self):
        if self.use_mesh:
            return self.load_mesh_assimp()
            # return self.load_mesh_OBJimporter()
        else:
            vertices = np.array(
                (
                    -0.1, -0.05, 0, 1.0, 1.0, 1.0, 0.0, 0.25,  # 0
                    -0.04, -0.05, 0, 1.0, 1.0, 1.0, 0.3, 0.25,  # 1
                    -0.06, 0.0, 0, 1.0, 1.0, 1.0, 0.2, 0.5,  # 2
                    0.0, -0.1,0, 1.0, 1.0, 1.0, 0.5, 0.0,  # 3
                    0.04, -0.05,0, 1.0, 1.0, 1.0, 0.7, 0.25,  # 4
                    0.1, -0.05,0, 1.0, 1.0, 1.0, 1.0, 0.25,  # 5
                    0.06, 0.0,0, 1.0, 1.0, 1.0, 0.8, 0.5,  # 6
                    0.08, 0.1,0, 1.0, 1.0, 1.0, 0.9, 1.0,  # 7
                    0.0, 0.02,0, 1.0, 1.0, 1.0, 0.5, 0.6,  # 8
                    -0.08, 0.1,0, 1.0, 1.0, 1.0, 0.1, 1.0  # 9
                ), dtype=np.float32
            )
            indices = [
                0, 1, 2,
                1, 3, 4,
                2, 1, 4,
                4, 5, 6,
                2, 4, 6,
                6, 7, 8,
                2, 6, 8,
                2, 8, 9
            ]
            return vertices, indices