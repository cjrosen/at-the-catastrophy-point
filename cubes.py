import math
import numpy as np
from vector import Vec3, Matrix


class MohrCube(object):

    def __init__(self):
        self.__corners_base = Matrix(np.array([
            [-1, -1, -1],
            [-1, -1,  1],
            [-1,  1, -1],
            [-1,  1,  1],

            [ 1, -1, -1],
            [ 1, -1,  1],
            [ 1,  1, -1],
            [ 1,  1,  1]]).transpose())
        self.__corners_current = self.__corners_base
        self.frame = -1
        self.segment = -1

        # self.__line_mappings = [
        #     [0, 1], [1, 2], [2, 3], [3, 0],
        #     [4, 5], [5, 6], [6, 7], [7, 4],
        #     [0, 4], [1, 5], [2, 6], [3, 7],
        # ]
        self.__line_mappings = [
            [7, 3], [6, 7], [6, 2], [2, 3],
            [3, 1], [1, 5], [4, 5], [0, 4],
            [0, 1], [5, 7], [4, 6], [2, 0],
        ]
        # self.__line_reordering = [
        #     0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11
        # ]
        self.__line_reordering = [
            2, 1, 0, 3, 11, 7, 6, 5, 8, 10, 9, 4
        ]

    def set_frame(self, frame):
        self.frame = frame
        self.segment = self.__segment_for_frame(frame)
        angles = self.__angles_at_frame(frame)
        rot = self.__euler_rotation_matrix(angles)
        print(f"Rotation matrix: {rot}")
        print(f"Corners (base): {self.__corners_base}")
        self.__corners_current = Matrix(rot.dot(self.__corners_base.get_matrix()))
        print(f"Corners (rotated): {self.__corners_current}")

    '''
    Rotation of cube
    '''

    def __angles_at_frame(self, f):
        r = math.pi/180
        x = 83 * math.sin((f - 98) * r) - 7 * math.sin((3 * f + 66) * r) - 90
        y = 30 * math.sin((2 * f - 16) * r)
        z = 83 * math.sin((f - 8) * r) + 7 * math.sin((3 * f + 156) * r) - (f - 518)

        return Vec3(x, y, z)

    def get_corner(self, i):
        return self.__corners_current.get_column(i).as_vector()

    def get_line(self, i):
        line = self.__line_mappings[self.__line_reordering[i]]
        return self.__corners_current.get_column(line[0]).as_vector(), self.__corners_current.get_column(line[1]).as_vector()

    def __euler_rotation_matrix(self, angles: Vec3):
        print(f"Angles to rotate by: {angles}")
        angles = angles * (math.pi / 180.0)
        # https://adipandas.github.io/posts/2020/02/euler-rotation/
        # https://www.meccanismocomplesso.org/en/3d-rotations-and-euler-angles-in-python/
        rx = np.array([
            [1,                   0,                  0],
            [0,  math.cos(angles.x), -math.sin(angles.x)],
            [0,  math.sin(angles.x),  math.cos(angles.x)]
        ])
        print(f"Rx: {rx}")
        ry = np.array([
            [ math.cos(angles.y), 0,  math.sin(angles.y)],
            [                 0, 1,                   0],
            [-math.sin(angles.y), 0,  math.cos(angles.y)]
        ])
        print(f"Ry: {ry}")
        rz = np.array([
            [ math.cos(angles.z), -math.sin(angles.z), 0],
            [ math.sin(angles.z),  math.cos(angles.z), 0],
            [                  0,                  0, 1]
        ])
        print(f"Rz: {rz}")
        return rz.dot(ry.dot(rx))

    # def rotated_corners(self, euler_angles):
    #     return self.euler_rotation_matrix(euler_angles) * self.__corners_base

    '''
    Combination of lines in cube
    '''

    def __segment_for_frame(self, f):
        s = math.floor((f - 483 - 5) / 30.0) - 1
        if s < 0 or s > 124:
            return -1
        return s

    def __bit_sum(self, i):
        i = i - ((i >> 1) & 0x55555555)
        i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
        i = ((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
        return i

    def __pattern_for_segment(self, s):
        c = 0
        for bits in range(1, 6):
            for i in range(64):
                if self.__bit_sum(i) == bits:
                    if c == s:
                        return i
                    c += 1
        for bits in range(1, 6):
            for i in range(64):
                if self.__bit_sum(i) == bits:
                    if c == s:
                        return (i << 6) | int(math.pow(2, 6) - 1)
                    c += 1

    def __bits_to_list(self, i):
        return [int(b) for b in '{:012b}'.format(i)]

    def get_pattern(self):
        pattern = self.__pattern_for_segment(self.segment)
        if pattern is None:
            return None
        return [(pattern & (0x1 << b)) > 0 for b in range(12)]

    '''
    Testing
    '''

    def test(self):
        frame = 1024
        # segment = self.__segment_for_frame(frame)
        # r = self.__pattern_for_segment(segment)
        # print(r)
        angles = self.__angles_at_frame(frame)
        rot = self.__euler_rotation_matrix(angles)
        print("Rotation matrix: ")
        print(rot)
        c = self.get_corner(1)
        print("Frist corner pre rotation:")
        print(c, type(c))
        print("Frist corner rotated:")
        print((rot * c).as_vector())

        # for s in range(1, 4):  # 125
        #     ascii_pattern = ''.join(["\u25A1" if b == 1 else "\u25A0" for b in bits_to_list(pattern_for_segment(s))])
        #     print(f"{s:03}: {ascii_pattern}")

        i = 7
        for n in range(0, 12):
            print(f"Bit {n+1} if {i} is: {i & (0x1 << n) > 0}")

        self.__pattern_for_frame(frame)



if __name__ == "__main__":
    print("Test cubes.py")
    cube = MohrCube()
    cube.test()
