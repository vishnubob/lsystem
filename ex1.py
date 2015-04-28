import math
import lsystem
import svgwrite

def leaf(icnt):
    rules = {"1": "11", "0": "1[0]0"}
    axiom = '0'
    ls = lsystem.LSystem(rules, axiom)
    txt = ls.solve(icnt)
    return txt

canvas = lsystem.LCanvas(cursor=(500, 1000), angle=math.radians(-90))
rules = leaf(10)
print "LSystem generated"
length = 1
for symbol in rules:
    if symbol == '0':
        canvas.push()
        canvas.draw(y=length)
        canvas.pop()
    elif symbol == '1':
        canvas.draw(y=length)
    elif symbol == '[':
        canvas.push()
        canvas.rotate(math.radians(-45))
    elif symbol == ']':
        canvas.pop()
        canvas.rotate(math.radians(45))
print "LSystem processed"

svg = svgwrite.Drawing("leaf.svg")
svg.viewbox(0, 0, 1000, 1000)
pl = svg.path(canvas.points, fill="none", stroke="black")
svg.add(pl)
print "LSystem saving"
svg.save()

