import sys
import math
import lsystem

def leaf(icnt):
    rules = lsystem.LGrammar()
    rules.add_rule("1", "11")
    rules.add_rule("0", "1[0]0")
    rules.add_rule("0", "0")
    rules.add_rule("0", "1[0][0]0")
    axiom = '0'
    ls = lsystem.LSystem(rules, axiom)
    txt = ls.solve(icnt)
    return txt

canvas = lsystem.LCanvas(cursor=(500, 500), angle=math.radians(-90))
rules = leaf(10)

print "LSystem generated"
length = .5
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

viewbox=(0, 0, 1000, 1000)
viewbox = str.join(' ', map(str, viewbox))
svg = lsystem.SVG(width="100%", height="100%", viewbox=viewbox)
path = str.join(' ', [str.join(' ', map(str, val)) for val in canvas.points])
path = lsystem.Path(d=path, fill="none", stroke="black")
svg.append(path)
print "LSystem saving"
svg.save("leaf.svg")
