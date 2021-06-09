import math
import numpy as np
from vector import Vec3, Matrix


'''
Rotation of cube
'''


def rotation(f):
    r = math.pi/180
    x = 83 * math.sin((f - 98) * r) + 7 * math.sin((3 * f + 114) * r)
    y = 30 * math.sin((2 * f + 16) * r)
    z = 83 * math.sin((f - 8) * r) + 7 * math.sin((3 * f + 156) * r) + (518 - f)

    return Vec3(x, y, z)


class Cube(object):

    def __init__(self):
        self.__corners = Matrix(np.array([[ 1,  1,  1],
                                          [ 1, -1,  1],
                                          [-1, -1,  1],
                                          [-1,  1,  1],

                                          [ 1,  1, -1],
                                          [ 1, -1, -1],
                                          [-1, -1, -1],
                                          [-1,  1, -1]]).transpose())

    def get_corner(self, i):
        return self.__corners.get_column(i).as_vector()

    def euler_rotation_matrix(self, angles: Vec3):
        # https://adipandas.github.io/posts/2020/02/euler-rotation/
        r1p = Matrix(np.array([
            [ math.cos(angles.z), math.sin(angles.z), 0],
            [-math.sin(angles.z), math.cos(angles.z), 0],
            [                  0,                  0, 1]
        ]))
        r1pp = Matrix(np.array([
            [math.cos(angles.y), 0, -math.sin(angles.y)],
            [                 0, 1,                   0],
            [math.sin(angles.y), 0,  math.cos(angles.y)]
        ]))
        r2 = Matrix(np.array([
            [1,                   0,                  0],
            [0,  math.cos(angles.x), math.sin(angles.x)],
            [0, -math.sin(angles.x), math.cos(angles.x)]
        ]))
        return r2 * r1pp * r1p

    def rotated_corners(self, euler_angles):
        return self.__corners


'''
Combination of lines in cube
'''


def segment_for_frame(f):
    s = math.floor((f - 482) / 30.0) - 1
    if s < 0.0 or s > 124.0:
        return -1
    return round(s)


def bit_sum(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    i = ((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
    return i


def pattern_for_segment(s):
    c = 0
    for bits in range(1, 6):
        for i in range(64):
            if bit_sum(i) == bits:
                c += 1
                if c == s:
                    return i
    for bits in range(1, 6):
        for i in range(64):
            if bit_sum(i) == bits:
                c += 1
                if c == s:
                    return (i << 6) | int(math.pow(2, 6) - 1)


def bits_to_list(i):
    return [int(b) for b in '{:012b}'.format(i)]


def pattern(f):
    p = [0] * 12
    s = pattern_for_segment(f)

    return s


def test():
    frame = 512
    r = rotation(f=frame)
    print(r)
    cube = Cube()
    rot = cube.euler_rotation_matrix(r)
    print("Rotation matrix: ")
    print(rot)
    c = cube.get_corner(1)
    print("Frist corner pre rotation:")
    print(c, type(c))
    print("Frist corner rotated:")
    print((rot * c).as_vector())
    # for s in range(1, 4):  # 125
    #     ascii_pattern = ''.join(["\u25A1" if b == 1 else "\u25A0" for b in bits_to_list(pattern_for_segment(s))])
    #     print(f"{s:03}: {ascii_pattern}")



if __name__ == "__main__":
    print("Test cubes.py")
    test()
