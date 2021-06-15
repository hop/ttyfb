import array
import os
import sys

DOTS = {
    (0, 0): 1,
    (0, 1): 2,
    (0, 2): 4,
    (0, 3): 64,
    (1, 0): 8,
    (1, 1): 16,
    (1, 2): 32,
    (1, 3): 128,
}

out = sys.stdout.write


class Kinemacolor:
    def __init__(self):
        w, h = os.get_terminal_size()
        self._size = w * h
        self.w = 2 * w
        self.h = 5 * h
        self.clear()

    def clear(self):
        self.gfx_buffer = array.array('B', [0] * self._size)
        self.clr_buffer = array.array('I', [0x00ff] * self._size)
        self.txt_buffer = [None] * self._size

    def render(self):
        out('\033[H\033[0m')
        out('\033[38;5;15m')
        out('\033[48;5;0m')

        def r():
            for g, c, t in zip(self.gfx_buffer, self.clr_buffer, self.txt_buffer):
                if t:
                    yield t
                else:
                    yield chr(0x2800+g)

        out(''.join(r()))

    def set_pixel(self, x, y):
        if not (0 < x < self.w and 0 < y < self.h):
            return

        px, x = divmod(int(x), 2)
        py, y = divmod(int(y), 5)

        p = py * (self.w//2) + px
        v = DOTS.get((x, y), 0)
        self.gfx_buffer[p] |= v

    def line(self, x0, y0, x1, y1):
        dx = x1 - x0
        dy = y1 - y0

        if abs(dx) > abs(dy):
            if dx < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                dx *= -1
                dy *= -1
            for x in range(abs(int(dx+1))):
                if dx < 0:
                    x *= -1
                y = int(x*dy/dx)
                self.set_pixel(x0+x, y0+y)
        else:
            if dy < 0:
                x0, x1 = x1, x0
                y0, y1 = y1, y0
                dx *= -1
                dy *= -1
            for y in range(abs(int(dy+1))):
                if dy < 0:
                    y *= -1
                x = int(y*dx/(dy or 1))
                self.set_pixel(x0+x, y0+y)

    def circle(self, cx, cy, r):
        # https://iq.opengenus.org/bresenhams-circle-drawing-algorithm/
        def draw(x, y):
            self.set_pixel(cx+x, cy+y)
            self.set_pixel(cx-x, cy+y)
            self.set_pixel(cx+x, cy-y)
            self.set_pixel(cx-x, cy-y)
            self.set_pixel(cx+y, cy+x)
            self.set_pixel(cx-y, cy+x)
            self.set_pixel(cx+y, cy-x)
            self.set_pixel(cx-y, cy-x)

        x = 0
        y = r
        decision = 3 - 2 * r
        draw(x, y)
        while y >= x:
            x += 1
            if decision > 0:
                y -= 1
                decision += 4 * (x - y) + 10
            else:
                decision += 4 * x + 6
            draw(x, y)


if __name__ == '__main__':
    demo = Kinemacolor()

    demo.line(0, 0, demo.w-1, demo.h-1)
    demo.line(0, demo.h-1, demo.w-1, 0)
    demo.circle(demo.w//2, demo.h//2, demo.h//3)
    demo.render()
    input()
