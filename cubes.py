import math
import os


'''
Rotation of cube
'''


def rotation(f):
    r = math.pi/180
    x = 83 * math.sin((f - 98) * r) + 7 * math.sin((3 * f + 114) * r)
    y = 30 * math.sin((2 * f + 16) * r)
    z = 83 * math.sin((f - 8) * r) + 7 * math.sin((3 * f + 156) * r) + (518 - f)

    return x, y, z


'''
Combination of lines in cube
'''


def segment_for_frame(f):
    s = math.floor((f - 482) / 30.0) - 1
    if s < 0.0 or s > 124.0:
        return -1
    return round(s)


def countNonZeroBits(i):
    i = i - ((i >> 1) & 0x55555555)
    i = (i & 0x33333333) + ((i >> 2) & 0x33333333)
    i = ((i + (i >> 4) & 0xF0F0F0F) * 0x1010101) >> 24
    return i

def pattern_for_segment(s):
    c = 0
    for bits in range(1, 6):
        for i in range(64):
            if countNonZeroBits(i) == bits:
                c += 1
                if c == s:
                    return i
    for bits in range(1, 6):
        for i in range(64):
            if countNonZeroBits(i) == bits:
                c += 1
                if c == s:
                    return (i << 6) | int(math.pow(2, 6) - 1)


def bits_to_list(i):
    return [int(b) for b in '{:012b}'.format(i)]


def pattern(f):
    p = [0] * 12
    s = pattern_for_segment(f)

    return s


frame = 512
print(rotation(f=frame))
#print(pattern(f=frame))
for s in range(1, 125):
    print(s, bits_to_list(pattern_for_segment(s)))

