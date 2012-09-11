import cairo
import rsvg
import math
import colorsys

class TurtleSVG(object):
    def __init__(self, fn, unit_length=0.005, width=1024, height=1024, x=0.5, y=0.5):
        fo = open(fn, 'w')
        self.width = width
        self.height = height
        self.surface = cairo.SVGSurface(fo, self.width, self.height)
        self.context = cairo.Context(self.surface)
        m = cairo.Matrix()
        m.scale(self.width / 1.0, self.height / 1.0)
        m.translate(x, y)
        self.context.set_matrix(m)
        self.context.set_line_width(.002)
        self.unit_length = unit_length
        self.context_stack = []

    def __del__(self):
        self.context.stroke()
        self.surface.finish()

    def move_forward(self):
        (x, y) = (0, -self.unit_length)
        self.context.line_to(x, y)
        self.context.translate(x, y)

    def rotate(self, deg):
        rad = math.radians(deg)
        self.context.rotate(rad)

    def push_context(self):
        self.context_stack.append(self.context.get_matrix())
        hue = len(self.context_stack) / 10.0
        rgb = colorsys.hsv_to_rgb(hue, 1, 1)
        print hue, rgb
        self.context.set_source_rgb(*rgb)

    def pop_context(self):
        self.context.stroke()
        self.context.set_matrix(self.context_stack.pop())

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

def leaf(icnt):
    fn = "leaf_%d.svg" % icnt
    turtle = TurtleSVG(fn)
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

def koch(icnt):
    fn = "koch_%d.svg" % icnt
    turtle = TurtleSVG(fn)
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

def plant(icnt):
    fn = "plant_%d.svg" % icnt
    turtle = TurtleSVG(fn, x=.5, y=1)
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


plant(6)
"""
for x in range(5):
    print x
    plant(x + 5)
"""
