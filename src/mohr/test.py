from cubes import MohrCube
from vector import Vec2, Vec3

import graphics

# use syspath because module is in parent dir...
import sys, os
sys.path.append(os.path.join(sys.path[0],'..'))
from svg import SVG


class MohrSvg:

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.center = Vec2(self.width, self.height) * 0.5

        self.cube_size = self.width * 0.1
        self.c1_center = self.center - Vec2(self.cube_size * 1.4, 0)
        self.c2_center = self.center + Vec2(self.cube_size * 1.4, 0)

        self.cube = MohrCube()

    def draw_svg(self, frame):

        s = SVG()

        s.create(self.width, self.height)
        color = "black"
        line_width = 4

        self.cube.set_frame(frame)
        scale = self.cube_size
        #v0, v1 = self.cube.get_line(0)
        #print(v0)
        pattern = self.cube.get_pattern()
        print(pattern)
        if pattern is None:
            pattern = [False] * 12
        s.new_group()
        for i in range(0, 12):
            center = self.c2_center if pattern[i] else self.c1_center
            v0, v1 = self.cube.get_line(i)
            s.line(
                center.x + scale * v0.x, center.y + scale * v0.y,
                center.x + scale * v1.x, center.y + scale * v1.y,
                color, line_width, linecap='round')
        s.end_group()

        s.add_font('monospaced_font', 'Alte Haas Grotesk', 12, 'bold', 'normal', '#000000', 'None')
        s.text(32, 16, f"Frame: {frame}", 'monospaced_font')

        s.finalize()

        try:
            # s.save(f"mohr_{frame:04}.svg")
            s.save(f"data/mohr_test.svg")
        except IOError as ioe:
            print(ioe)

        print(s)

    def draw_animation(self, win):

        scale = self.cube_size / 2
        pattern = self.cube.get_pattern()
        print(pattern)
        if pattern is None:
            pattern = [False] * 12
        for i in range(0, 12):
            center = self.c2_center if pattern[i] else self.c1_center
            v0, v1 = self.cube.get_line(i)
            line = Line(
                Point(center.x + scale * v0.x, center.y - scale * v0.y),
                Point(center.x + scale * v1.x, center.y - scale * v1.y)
            )
            line.setWidth(2)
            line.draw(win) # draw it to the window
        return


    def test(self):
        self.draw_svg(583)
        return
        frame = 518

        win = GraphWin(width = self.width, height = self.height) # create a window
        win.setCoords(0, self.height, self.width, 0) # set the coordinates of the window
        while True:
            self.cube.set_frame(frame)

            clear = Rectangle(Point(0, 0), Point(self.width, self.height))
            clear.setFill("white")
            clear.draw(win)

            text = Text(Point(120,20), f"Frame: {self.cube.frame}\nSegment: {self.cube.segment}")
            text.draw(win)

            self.draw_animation(win)

            key = win.getKey()
            if key == 'Right':
                frame += 1
            elif key == 'Up':
                frame += 8
            elif key == 'Left':
                frame -= 1
            elif key == 'Down':
                frame -= 8
            else:
                win.close()
                break



if __name__ == "__main__":
    print("Test mohr")
    scale = 0.1
    mohr = MohrSvg(2360*scale, 2596*scale)
    mohr.test()

