# import cubes
import svg
from vector import Vector


class MohrSvg:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.center = Vector(self.width, self.height) * 0.5

        self.cube_size = self.width * 0.1
        self.c1_center = self.center - Vector(self.cube_size * 1.2, 0)

    def draw(self, frame):

        s = svg.SVG()

        s.create(self.width, self.height)
        color = "black"
        line_width = 2

        s.line(color, line_width,
               self.c1_center.x - self.cube_size, self.c1_center.y - self.cube_size,
               self.c1_center.x - self.cube_size, self.c1_center.y + self.cube_size)

        # s.text(32, 16, "sans-serif", 16, "#000000", "#000000", "codedrome.com")

        s.finalize()

        try:
            s.save(f"mohr_{frame:04}.svg")
        except IOError as ioe:
            print(ioe)

        print(s)


def test():
    scale = 0.25
    mohr = MohrSvg(2360*scale, 2596*scale)
    mohr.draw(512)


if __name__ == "__main__":
    print("Test mohr")
    test()

