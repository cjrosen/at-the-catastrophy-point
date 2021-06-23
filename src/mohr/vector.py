import numpy as np
import math

class Vec2:

    def __init__(self):
        self.x = 0
        self.y = 0

    def __init__(self, x, y):
        self.x = x
        self.y = y

    def __getitem__(self, key): 
        if key == 0:
            return self.x
        if key == 1:
            return self.y
    
    def __iter__(self):
        self.__iter_n = 0
        return self

    def __next__(self):
        if self.__iter_n < 2:
            self.__iter_n += 1
            return self[self.__iter_n-1]
        else:
            raise StopIteration

    def __add__(self, other):
        return Vec2(self.x + other.x, self.y + other.y)

    def __sub__(self, other):
        return Vec2(self.x - other.x, self.y - other.y)

    def __mul__(self, other):
        if isinstance(other, Vec2):
            return self.x * other.x + self.y * other.y
        return Vec2(self.x * other, self.y * other)

    def rotateDegrees(self, degrees):
        return self.rotateRadians(degrees * math.pi / 180.0)
    
    def rotateRadians(self, radians):
        return Vec2(
            math.cos(radians) * self.x - math.sin(radians) * self.y,
            math.sin(radians) * self.x + math.cos(radians) * self.y,
        )
    
    def angleDegrees(self, v):
        return self.angleRadians(v) * 180 / math.pi

    def angleRadians(self, v):
        return math.acos( (self.x * v.x + self.y * v.y) / ( self.length() * v.length() ) )

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y)

    def norm(self):
        l = self.length()
        return Vec2(self.x / l, self.y / l)

    def dot(self, v):
        return self.x * v.x + self.y * v.y

    def npCol(self):
        return np.array([[self.x], [self.y]])

    def npRow(self):
        return np.array([self.x, self.y])

    def __str__(self):
        return f"[{self.x:.2f}, {self.y:.2f}]"

    def __repr__(self):
        return f"[{self.x:.2f}, {self.y:.2f}]"


class Vec3:

    def __init__(self):
        self.x = 0
        self.y = 0
        self.z = 0

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def __getitem__(self, key): 
        if key == 0:
            return self.x
        if key == 1:
            return self.y
        if key == 2:
            return self.z

    def __iter__(self):
        self.__iter_n = 0
        return self

    def __next__(self):
        if self.__iter_n < 3:
            self.__iter_n += 1
            return self[self.__iter_n-1]
        else:
            raise StopIteration

    def __add__(self, other):
        return Vec3(self.x + other.x, self.y + other.y, self.z + other.z)

    def __sub__(self, other):
        return Vec3(self.x - other.x, self.y - other.y, self.z - other.z)

    def __mul__(self, other):
        if isinstance(other, Vec3):
            return self.x * other.x + self.y * other.y + self.z * other.z
        if isinstance(other, Vec2):
            print("Can't multiply Vec2 with Vec3")
            return None
        return Vec3(self.x * other, self.y * other, self.z * other)

    def length(self):
        return math.sqrt(self.x * self.x + self.y * self.y + self.z * self.z)

    def norm(self):
        l = self.length()
        return Vec3(self.x / l, self.y / l, self.z / l)

    def npCol(self):
        return np.array([[self.x], [self.y], [self.z]])

    def npRow(self):
        return np.array([self.x, self.y, self.z])

    def __str__(self):
        return f"[{self.x:.2f}, {self.y:.2f}, {self.z:.2f}]"

    def __repr__(self):
        return f"[{self.x:.2f}, {self.y:.2f}, {self.z:.2f}]"


class Matrix:

    def __init__(self, nparray):
        self.mat = nparray
        self.rows = self.mat.shape[0]
        self.cols = self.mat.shape[1] if len(self.mat.shape) > 1 else 1

    @classmethod
    def zeros(cls, rows, cols):
        return cls(np.zeros((rows, cols)))

    def getValue(self, x, y):
        return self.mat[y, x]

    def getMatrix(self):
        return self.mat

#     def get_row(self, row):
#         return Matrix(self.m, 1, [self.values[self.m*row+i] for i in range(self.m)])

    def getColumn(self, col):
        return Matrix(self.mat[:, col])

    def asVector(self):
        if (self.rows == 1 and self.cols == 2) or (self.rows == 2 and self.cols == 1):
            mat = self.mat.reshape((1, 2))
            return Vec2(mat[0, 0], mat[0, 1])
        if (self.rows == 1 and self.cols == 3) or (self.rows == 3 and self.cols == 1):
            mat = self.mat.reshape((1, 3))
            return Vec3(mat[0, 0], mat[0, 1], mat[0, 2])
        return None

#     def set(self, x, y, value):
#         if x < 0 or x >= self.m or y < 0 or y >= self.n:
#             return None
#         self.values[self.m*y + x] = value
#
    def transpose(self):
        return Matrix(self.mat.transpose())

    def __mul__(self, other):
        if isinstance(other, Vec2) and self.cols == 2:
            return Matrix(self.mat.dot(other.npCol()))

        if isinstance(other, Vec3) and self.cols == 3:
            return Matrix(self.mat.dot(other.npCol()))

        if isinstance(other, Matrix):
            return Matrix(self.mat.dot(other.mat))

        return Matrix(self.mat.dot(other))

    def __str__(self):
        return f"{self.mat}"


def test():
    print("Vec2")
    v1 = Vec2(1, 1)
    v2 = Vec2(2, -2)
    v3 = v1 + v2
    print(f"{v1} + {v2} = {v3}")
    v3 = v1 - v2
    print(f"{v1} - {v2} = {v3}")
    v3 = v1 * v2
    print(f"{v1} * {v2} = {v3}")
    v3 = v1 * 0.5
    print(f"{v1} * {0.5} = {v3}")

    print("\nVec3")
    v1 = Vec3(1, 1, 1)
    v2 = Vec3(2, -2, -1)
    v3 = v1 + v2
    print(f"{v1} + {v2} = {v3}")
    v3 = v1 - v2
    print(f"{v1} - {v2} = {v3}")
    v3 = v1 * v2
    print(f"{v1} * {v2} = {v3}")
    v3 = v1 * 0.5
    print(f"{v1} * {0.5} = {v3}")

    # print("\nMatrix")
    # m1 = Matrix.zeros(2, 3)
    # m2 = Matrix(2, 2, [1,2,3,4])
    # m3 = Matrix.from_column_vectors([Vec2(1,2),Vec2(3,4),Vec2(5,6)])
    # print(m1)
    # print(m2)
    # print(m3)
    # print(m3.transpose())
    #
    # v1 = Vec3(2,2,0)
    # m4 = m2 * 0.5
    # print(f"{m2} * {0.5} = \n{m4}")
    # m4 = m3 * v1
    # print(f"{m3} * {v1} = \n{m4}")
    # m5 = m3.get_row(0)
    # print(f"Row 0 of m3 is:\n{m5}")
    # print(f"That makes a vector: {m5.as_vector()}")
    # m5 = m3.get_column(0)
    # print(f"Col 0 of m3 is:\n{m5}")
    # print(f"That makes a vector: {m5.as_vector()}")

    print("\nMatrix")
    m1 = Matrix.zeros(2, 3)
    m2 = Matrix(np.array([[1, 2],
                   [3, 4]]))
    m3 = Matrix(np.array([[1, 3, 5],
                   [2, 4, 6]]))
    print(m1)
    print(m2)
    print(m3)
    print(m3.transpose())

    m4 = m2 * 0.5
    print(f"{m2} * {0.5} = \n{m4}")
    v1 = Vec3(2, 2, 0)
    m4 = m3 * v1
    print(f"{m3} * {v1} = \n{m4}")
    v1 = Vec2(2, 2)
    m4 = m3.transpose() * v1
    print(f"{m3.transpose()} * {v1} = \n{m4}")
    print(f"That makes a vector: {m4.asVector()}")


if __name__ == "__main__":
    print("Test vector.py")
    test()




# class Matrix:
#
#     def __init__(self, m, n, values):
#         self.m = m
#         self.n = n
#         self.values = values
#
#     @classmethod
#     def from_column_vectors(cls, column_vectors):
#         t = type(column_vectors[0])
#         for v in column_vectors:
#             if type(v) is not t:
#                 return None
#         if not (t is Vec3 or t is Vec2):
#             return None
#         m = len(column_vectors)
#         values = []
#         n = 2
#         for v in column_vectors:
#             values.append(v.x)
#         for v in column_vectors:
#             values.append(v.y)
#         if t is Vec3:
#             n = 3
#             for v in column_vectors:
#                 values.append(v.z)
#         return cls(m, n, values)
#
#     @classmethod
#     def zeros(cls, m, n):
#         return cls(m, n, [0] * m * n)
#
#     def get_value(self, x, y):
#         if x < 0 or x >= self.m or y < 0 or y >= self.n:
#             return None
#         return self.values[self.m*y + x]
#
#     def get_row(self, row):
#         return Matrix(self.m, 1, [self.values[self.m*row+i] for i in range(self.m)])
#
#     def get_column(self, col):
#         return Matrix(1, self.n, [self.values[self.m*i+col] for i in range(self.n)])
#
#     def as_vector(self):
#         if (self.n == 1 and self.m == 2) or (self.m == 1 and self.n == 2):
#             return Vec2(self.values[0], self.values[1])
#         if (self.n == 1 and self.m == 3) or (self.m == 1 and self.n == 3):
#             return Vec3(self.values[0], self.values[1], self.values[2])
#         return None
#
#     def set(self, x, y, value):
#         if x < 0 or x >= self.m or y < 0 or y >= self.n:
#             return None
#         self.values[self.m*y + x] = value
#
#     def transpose(self):
#         m = self.n
#         n = self.m
#         values = [0] * m * n
#         for x in range(m):
#             for y in range(n):
#                 values[m*y+x] = self.values[self.m*x+y]
#         return Matrix(m, n, values)
#
#     def __mul__(self, other):
#         if isinstance(other, float):
#             return Matrix(self.m, self.n, [v * other for v in self.values])
#         values = []
#
#         if isinstance(other, Vec2) and self.m == 2:
#             for row in range(self.n):
#                 row = Vec2(self.get_value(0, row), self.get_value(1, row))
#                 values.append(row * other)
#             return Matrix(1, len(values), values) if len(values) > 0 else None
#
#         if isinstance(other, Vec3) and self.m == 3:
#             for row in range(self.n):
#                 vr = Vec3(self.get_value(0, row), self.get_value(1, row), self.get_value(2, row))
#                 values.append(vr * other)
#             return Matrix(1, len(values), values) if len(values) > 0 else None
#
#         # if isinstance(other, Matrix) and self.m == other.n:
#         #     result = Matrix.zeros(other.m, self.n)
#         #     for right_col_index in range(other.m):
#         #         for left_row_index in range(self.n):
#         #             left_row = self.get_row(left_row_index)
#         #             right_col = other.get_column(right_col_index)
#
#     def __str__(self):
#         #output = f"Matrix, {self.m} x {self.n} (m x n)\n[ "
#         output = f"(m{self.m}x{self.n})\n[ "
#         for row in range(self.n):
#             for col in range(self.m):
#                 output += f"{self.get_value(col, row):8.2f}, "
#             output += "\n  " if row < self.n - 1 else "]"
#         return output