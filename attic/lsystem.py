import cairo
import math
import colorsys

class TurtleSVG(object):
    def __init__(self, fn, step=0.0005, width=1024, height=1024, line_width=0.0001, x=0.5, y=0.5):
        self.fo = open(fn, 'w')
        self.width = width
        self.height = height
        self.surface = cairo.SVGSurface(self.fo, self.width, self.height)
        self.context = cairo.Context(self.surface)
        m = cairo.Matrix()
        m.scale(self.width / 1.0, self.height / 1.0)
        m.translate(x, y)
        self.context.set_matrix(m)
        self.context.set_line_width(line_width)
        self.context.move_to(0, 0)
        self.turtle = (0, 0)
        self.unit_length = step
        self.context_stack = []

    def close(self):
        self.context.stroke()
        self.surface.finish()
        if self.fo:
            self.fo.close()

    def move_forward(self):
        (x, y) = (0, -self.unit_length)
        self.context.line_to(x, y)
        self.context.translate(x, y)
        if self.is_clipped():
            raise ValueError, "clipped"

    def rotate(self, deg):
        rad = math.radians(deg)
        self.context.rotate(rad)

    def push_context(self):
        frame = self.context.get_matrix()
        self.context_stack.append(frame)

    def is_clipped(self):
        (x, y) = self.context.user_to_device(0, 0)
        return (x < 0 or x > self.width) or (y < 0 or y > self.height)

    def pop_context(self):
        #self.context.stroke()
        matrix = self.context_stack.pop()
        self.context.set_matrix(matrix)
        self.context.move_to(0, 0)

class LSystem(object):
    def __init__(self, rules, start):
        self.rules = rules
        self.state = []
        self.state.append(start)
        
    def iterate(self):
        state = self.state[-1]
        out = ''
        for ch in state:
            if ch not in self.rules:
                out += ch
            else:
                out += self.rules[ch]
        self.state.append(out)
        return self.state[-1]

    def solve(self, icnt):
        res = None
        for x in range(icnt):
            res = self.iterate()
        return res

def leaf(icnt, step, line_width):
    try:
        fn = "leaf_%d.svg" % icnt
        turtle = TurtleSVG(fn, step=step, line_width=line_width, x=0.5, y=1)
        rules = {"1": "11", "0": "1[0]0"}
        ls = LSystem(rules, '0')
        txt = ls.solve(icnt)
        for ch in txt:
            if ch == '1' or ch == '0':
                turtle.move_forward()
            elif ch == '[':
                turtle.push_context()
                turtle.rotate(-45)
            elif ch == ']':
                turtle.pop_context()
                turtle.rotate(45)
    finally:
        turtle.close()

def koch(icnt, step, line_width):
    try:
        fn = "koch_%d.svg" % icnt
        turtle = TurtleSVG(fn, step=step, line_width=line_width, x=0, y=1)
        rules = {"F": "F+F-F-F+F"}
        ls = LSystem(rules, 'F')
        txt = ls.solve(icnt)
        for ch in txt:
            if ch == 'F':
                turtle.move_forward()
            elif ch == '+':
                turtle.rotate(90)
            elif ch == '-':
                turtle.rotate(-90)
    finally:
        turtle.close()

def plant(icnt, step, line_width):
    try:
        fn = "plant_%d.svg" % icnt
        turtle = TurtleSVG(fn, step=step, line_width=line_width, x=.5, y=1)
        rules = {"X": "F-[[X]+X]+F[+FX]-X)", "F": "FF"}
        ls = LSystem(rules, 'X')
        txt = ls.solve(icnt)
        for ch in txt:
            if ch == 'F':
                turtle.move_forward()
            elif ch == '-':
                turtle.rotate(-25)
            elif ch == '+':
                turtle.rotate(25)
            elif ch == '[':
                turtle.push_context()
            elif ch == ']':
                turtle.pop_context()
    finally:
        turtle.close()

def scale(func):
    step = 0.01
    width = 0.005
    for x in range(8):
        while 1:
            try:
                func(x + 1, step, width)
                break
            except ValueError, err:
                width *= 0.9
                step *= 0.9
        print x, width, step 

