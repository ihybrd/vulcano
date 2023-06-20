"""
Author: Hu Yongbin
create date: Jul 8, 2018
description: cgmath is a math module for computer graphic usage
"""

import math


class MatrixError(Exception):
    pass


class VectorError(Exception):
    pass


class Vector(object):

    def __init__(self, *components):
        self.__components = components
        self.__component_count = len(self.__components)

    def get_component_count(self):
        """return number of vector components."""
        return self.__component_count

    def to_list(self):
        """return vector components in array"""
        return self.__components

    def __mul__(self, other):
        return Vector(*[a * other for a in self.__components])

    def __div__(self, other):
        return Vector(*[a / other for a in self.__components])

    def __add__(self, other):
        return self.__add_sub(other, 1)

    def __sub__(self, other):
        return self.__add_sub(other, -1)

    def __add_sub(self, other, op):
        if other.get_component_count() != self.get_component_count():
            raise VectorError("Number of vector component isn't name")
        args = [y + x * op for x, y in zip(other.to_list(), self.__components)]
        return Vector(*args)

    def magnitude(self):
        return pow(sum([pow(i, 2) for i in self.__components]), 0.5)

    def normalized(self):
        """
                          v
        normalized(v) =  ---
                         |v|
        """
        magnitude = self.magnitude()
        return Vector(*[i / magnitude for i in self.__components])

    def dot(self, vec):
        if not isinstance(vec, Vector):
            raise VectorError("dot needs to work with another vector")
        return round(sum([x * y for x, y in zip(vec.to_list(), self.__components)]), 4)

    def to_matrix(self, row_major = True):
        if not row_major:
            r, c = len(self.__components), 1
        else:
            c, r = len(self.__components), 1

        return Matrix(r, c, self.__components)

    def get_angle_with(self, vec):
        """vec needs to be 2 or 3"""
        return math.degrees(math.acos(self.dot(vec.normalized())))


class Matrix(object):
    def __init__(self, row, column, entries = None):
        """
            row - number of rows
            column - number of columns
            entries - elements

        """
        self.__row = row
        self.__col = column
        if entries is None:
            self.__mtx = [0] * row * column
        else:
            if len(entries) != row * column:
                raise MatrixError("len(entries) != r * c")
            self.__mtx = entries
        self.__is_row_major = True

    def multiply(self, other):
        """ Matrix can multiply with scalar or other matrix

        M * scalar

        | a b c |       | ak bk ck |
        | d e f | * k = | dk ek fk |
        | g h i |       | gk hk ik |

        M1 is a 3x3 matrix, M2 is 3x1 matrix, below is the result of M1*M2

        rule
        M1.col == M2.row, if M1.col != M2.row, they can't be multiplied
        M1 * M2 != M2 * M1

        M1          M2      result

        | a b c |   | x |   | ax + by + cz |
        | d e f | * | y | = | ex + ey + fz |
        | e g i |   | z |   | ex + gy + iz |

        arg:
            other: another matrix object, which should have same number of rows
                with current matrix's column number.
       """
        if isinstance(other, int) or isinstance(other, float):
            return self.__mul_scalar(other)
        elif isinstance(other, Vector) or isinstance(other, Matrix):
            return self.__mul_matrix(other)

    def __mul_scalar(self, other):
        return Matrix(self.__row, self.__col, [i * other for i in self.__mtx])

    def __mul_matrix(self, other):
        if self.__col != other.rows():
            raise MatrixError("col != row")
        new_col = other.columns()
        new_row = self.__row
        mtx = [0] * new_col * new_row
        for i in range(new_row):
            for j in range(new_col):
                vec1 = Vector(*other.get_column(j))
                vec2 = Vector(*self.get_row(i))
                mtx[new_col * i + j] = vec1.dot(vec2)
        return Matrix(new_row, new_col, mtx)

    def is_row_major(self):
        """returns True if the current matrix is row-major"""
        return self.__is_row_major

    def is_column_major(self):
        """returns True if the current matrix is column-major"""
        return not self.__is_row_major

    def set_matrix(self, m):
        """sets matrix with array."""
        self.__mtx = m

    def to_list(self):
        """returns matrix as array."""
        return self.__mtx

    def transpose(self):
        """Transpose matrix is a new matrix with exchanged the row id and col
        id from the current one.

        row-major     col-major

        | 1 2 3 |     | 1 4 7 |
        | 4 5 6 | --> | 2 5 8 |
        | 7 8 9 |     | 3 6 9 |
        """
        m = [0] * self.__row * self.__col
        for i in range(self.__row):
            for j in range(self.__col):
                c = self.get_entry(i, j)
                m[self.__row * j + i] = c
        self.__col, self.__row = self.__row, self.__col
        self.__is_row_major = False
        self.__mtx = m
        # return Matrix(self.__col, self.__row, m)

    def minor(self, i, j):
        """Mintor of a matrix

        M             M(1,2)

        | a b c |     | a b . |
        | d e f | --> | . . . | --> | a b |
        | g h i |     | g h . |     | g h |

        args:
            i - the id of row
            j - the ie of col
            col - the number of columns
            m - the matrix values.

        returns:
            a new minored matrix
        """
        return self.__minor(i, j, self.__col, self.__mtx)

    def __minor(self, i, j, col, m):
        _m = [0] * (col - 1) * (col - 1)
        for _j in range(col):  # column
            for _i in range(col):  # row
                if _j != j and _i != i:
                    J = _j if _j < j else _j - 1
                    I = _i if _i < i else _i - 1
                    self.__set_entry(I, J, m[col * _i + _j], col - 1, _m)
                    # _m[(col - 1) * I + J] = m[col * _i + _j]
        return _m

    def determinant(self):
        """ The determinant of a matrix is an operation that takes a square
        matrix to a number.

        Det of a 2x2 matrix

        det | a b | = ad - bc
            | c d |

        Belows are steps of how to get the determinant of given 3x3 matrix

            | a b c |
        det | d e f |
            | g h i |

              | . . . |       | . . . |       | . . . |
        = a * | . e f | - b * | d . f | + c * | d e . |
              | . h i |       | g . i |       | g h . |

        = a * | e f | - b * | d f | + c * | d e |
              | h i |       | g i |       | g h |

        = a * (ei - fh) - b * (di - fg) + c * (dh - eg)

        For larger size matrix,
        """
        return self.__determinant(self.__mtx)

    def __determinant(self, M):
        size = int(pow(len(M), 0.5))
        if size > 2:
            r = 0
            for c in range(size):
                m = self.__minor(0, c, size, M)
                # DEBUG: Matrix(size-1, size-1, m).print_matrix()
                det = self.__determinant(m)
                minor = 1 if c % 2 == 0 else -1
                r += M[c] * det * minor
            return r
        elif size == 2:
            return M[0] * M[3] - M[1] * M[2]  # check if transpose supported
        elif size == 1:
            return M[0]
        else:
            raise MatrixError("no element in the matrix")

    def adjoint(self):
        """returns adjoint matrix,
        adjoint matrix is a transposed cofactor matrix
        """
        cof = self.cofactor()
        cof.transpose()
        return cof

    def cofactor(self):
        """
        formular of getting cofactor from a matrix

                      (i+j)
        cofactor = -1       x Det(Minor(i, j))

        see self.determinant and self.minor for more details about definition.

        """
        return self.__cofactor(self.__mtx)

    def __cofactor(self, M):
        size = int(pow(len(M), 0.5))
        m = [0] * size * size
        for j in range(size):  # column
            for i in range(size):  # row
                cofactor = pow(-1, i + j) * self.__determinant(self.__minor(i, j, size, M))
                self.__set_entry(i, j, cofactor, size, m)
        return Matrix(self.__row, self.__col, m)

    def inverse(self):
        """

         -1    1
        M   = --- . adj(M)
              |M|

        if |M| == 0, then the matrix doesn't have its inversed.
        """
        return self.adjoint().multiply(1.0 / self.determinant())

    def has_inverse(self):
        """ Matrix is not inverse-able if |M| == 0.
        """
        return False if self.determinant() == 0 else True

    def is_square(self):
        """Returns true if col = row else returns false."""
        return self.__col == self.__row

    def get_identity_matrix(self):
        """returns a new matrix as identity matrix.
        """
        if not self.is_square():
            raise MatrixError("Only sqr matrix returns identity matrix")
        m = [0] * self.__col * self.__row
        for c in range(self.__col):
            self.__set_entry(c, c, 1, self.__col, m)
        return Matrix(self.__row, self.__col, m)

    def identify(self):
        """Sets current matrix as identity matrix (or unit matrix). Identity
        matrix should be a n x n square matrix, and it looks like this:

            | 1 0 0 . 0 |
            | 0 1 0   . |
        I = | 0 0 1   . |
            | .     . . |
            | 0 . . . 1 |
        """
        if not self.is_square():
            raise MatrixError("Only sqr matrix returns identity matrix")
        self.__mtx = [0] * self.__col * self.__row
        for c in range(self.__col):
            self.set_entry(c, c, 1)

    def __get_entry(self, i, j, col, m):
        return m[col * i + j]

    def __set_entry(self, i, j, val, col, m):
        m[col * i + j] = val

    def get_entry(self, i, j):
        """returns Matrix (i, j)"""
        return self.__get_entry(i, j, self.__col, self.__mtx)

    def set_entry(self, i, j, val):
        """sets matrix (i, j) with given value"""
        self.__set_entry(i, j, val, self.__col, self.__mtx)

    def get_row(self, j):
        """returns specific row of the matrix in array"""
        return self.__mtx[j * self.__col: j * self.__col + self.__col]

    def get_column(self, i):
        """"returns specific column of the matrix in array"""
        return [self.__mtx[idx + i] for idx in range(0, len(self.__mtx), self.__col)]

    def columns(self):
        """returns number of columns of the current matrix"""
        return self.__col

    def rows(self):
        """returns number of rows of the current matrix"""
        return self.__row

    def print_matrix(self):
        print ("Rows: %s\nColumns:%s" % (self.__row, self.__col))
        for col in range(0, len(self.__mtx), self.__col):
            r = []
            for c in range(self.__col):
                r.append(self.__mtx[col + c])
            print ("\t".join([str(i) for i in r]))


class Vector4(Vector):
    """
    Homogeneous coordinate vector.
    """

    def __init__(self, x, y, z, w):
        super(Vector4, self).__init__(*[x, y, z, w])
        self.x = x
        self.y = y
        self.z = z
        self.w = w

    def cross(self, vec4):
        """
        A x B = Ay*Bz - Az*By, Az*Bx - Ax*Bz, Ax*By - Ay*Bx
        """
        x = self.y * vec4.z - self.z * vec4.y
        y = self.z * vec4.x - self.x * vec4.z
        z = self.x * vec4.y - self.y * vec4.x
        return Vector4(x, y, z, 0)

    def is_point(self):
        return True if self.w == 1 else False

    def is_vector(self):
        return True if self.w == 0 else False


class Matrix4x4(Matrix):
    """
    Homogeneous coordinate matrix.
    """

    def __init__(self, m = None):
        super(Matrix4x4, self).__init__(4, 4, m)

    def I(self):
        m = [1,0,0,0,
             0,1,0,0,
             0,0,1,0,
             0,0,0,1]

        return Matrix4x4(m)

    def T(self, tx, ty, tz):

        # row-major
        m = [1, 0, 0, 0,
             0, 1, 0, 0,
             0, 0, 1, 0,
             tx,ty,tz,1]

        M = Matrix4x4(m)
        if self.is_column_major():
            M.transpose()
        return M

    def S(self, sx, sy, sz):

        m = [sx,0, 0, 0,
             0, sy,0, 0,
             0, 0, sz,0,
             0, 0, 0, 1]

        return Matrix4x4(m)

    def __get_cos_sin(self, a):
        c = math.cos(math.radians(a))
        s = math.sin(math.radians(a))
        return c, s

    def R_x(self, a):
        c, s = self.__get_cos_sin(a)

        m = [1, 0, 0, 0,
             0, c, s, 0,
             0,-s, c, 0,
             0, 0, 0, 1]

        M = Matrix4x4(m)
        if self.is_column_major():
            M.transpose()
        return M

    def R_y(self, a):
        c, s = self.__get_cos_sin(a)

        m = [c, 0,-s, 0,
             0, 1, 0, 0,
             s, 0, c, 0,
             0, 0, 0, 1]

        M = Matrix4x4(m)
        if self.is_column_major():
            M.transpose()
        return M

    def R_z(self, a):
        c, s = self.__get_cos_sin(a)

        m = [c, s, 0, 0,
             -s,c, 0, 0,
             0, 0, 1, 0,
             0, 0, 0, 1]

        M = Matrix4x4(m)
        if self.is_column_major():
            M.transpose()
        return M

    # TODO: correct the order of the multiplication between matrixes.
    # the result of the R mul still needs to be validated.
    def R(self, rx, ry, rz):
        # eura
        x = self.R_x(rx)
        y = self.R_y(ry)
        z = self.R_z(rz)
        return y.multiply(x.multiply(z))

    def transform(self, tx, ty, tz, rx, ry, rz, sx, sy, sz):
        """ transform order of matrix multiplication.

        1) scale
        2) rotate
        3) translate
        """
        s = self.S(sx, sy, sz)
        r = self.R(rx, ry, rz)
        t = self.T(tx, ty, tz)
        return s.multiply(r).multiply(t)

