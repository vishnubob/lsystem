import math
import lsystem
import svgwrite

def penrose(icnt):
    rules = {
        "M": "OA++PA----NA[-OA----MA]++",
        "N": "+OA--PA[---MA--NA]+",
        "O": "-MA++NA[+++OA++PA]-",
        "P": "--OA++++MA[+PA++++NA]--NA",
        "A": ""
    }
    axiom = '[N]++[N]++[N]++[N]++[N] '
    ls = lsystem.LSystem(rules)
    txt = ls.solve(axiom=axiom, iterations=icnt)
    return txt

canvas = lsystem.LCanvas(cursor=(500, 500), angle=math.radians(-90))
rules = penrose(5)
print "LSystem generated"
length = 40
for symbol in rules:
    if symbol == '+':
        canvas.rotate(math.radians(36))
    elif symbol == '-':
        canvas.rotate(math.radians(-36))
    elif symbol == '[':
        canvas.push()
    elif symbol == ']':
        canvas.pop()
    elif symbol in 'ABCDEF':
        canvas.draw(y=length)
    #else:
        #canvas.draw(y=length, move=True)
print "LSystem processed"

svg = svgwrite.Drawing("leaf.svg")
svg.viewbox(0, 0, 1000, 1000)
pl = svg.path(canvas.points, fill="none", stroke="black")
svg.add(pl)
print "LSystem saving"
svg.save()

