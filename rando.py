import math
import lsystem
import svgwrite
import random
import uuid
import os

class RandomLSystem(object):
    Modes = {
        "stack": ('[', ']'),
        "rotate": ('+', '-'),
        "draw": ('A', 'B', 'C', 'D'),
        "move": ('G', 'H', 'I', 'J'),
        "variables": ('W', 'X', 'Y', 'Z')
    }
    Tokens = Modes["draw"] + Modes["move"] + Modes["variables"]
    Alphabet = Modes["stack"] + Modes["rotate"] + Modes["draw"] + Modes["move"] + Modes["variables"]

    def __init__(self, **kw):
        self.max_rules = 10
        self.min_rules = 2
        self.max_rule_len = 30
        self.min_rule_len = 0

    def random_rule(self):
        rule_len = random.randint(self.min_rule_len, self.max_rule_len)
        token = random.choice(self.Tokens)
        rule = str.join('', [random.choice(self.Alphabet) for x in range(rule_len)])
        return (token, rule)
    
    def random_rules(self):
        rules = {}
        rule_count = random.randint(self.min_rules, self.max_rules)
        for ridx in range(rule_count):
            (token, rule) = self.random_rule()
            if token not in rules:
                rules[token] = []
            rules[token].append(rule)
        return rules
    
    def random_axiom(self):
        axiom_len = random.randint(self.min_rule_len, self.max_rule_len)
        axiom = str.join('', [random.choice(self.Alphabet) for x in range(axiom_len)])
        return axiom

    def random_angle(self):
        return random.random() * (2 * math.pi)
    
    def generate(self):
        res = {
            "angle": self.random_angle(),
            "rules": self.random_rules(),
            "axiom": self.random_axiom(),
        }
        return res

def generate_path(rules='', axiom='', angle=0, iterations=0, seed=None):
    if seed != None:
        random.seed(seed)
    canvas = lsystem.LCanvas(cursor=(500, 500), angle=math.radians(-90))
    ls = lsystem.LSystem(rules)
    txt = ls.solve(axiom=axiom, iterations=iterations)
    length = 40
    did_something = set()
    for symbol in txt:
        if symbol == '+':
            did_something.add('left')
            canvas.rotate(angle)
        elif symbol == '-':
            did_something.add('right')
            canvas.rotate(-angle)
        elif symbol == '[':
            did_something.add('push')
            canvas.push()
        elif symbol == ']':
            did_something.add('pop')
            canvas.pop()
        elif symbol in 'ABCD':
            canvas.draw(y=length)
            did_something.add('draw')
        elif symbol in 'GHIJ':
            canvas.draw(y=length, move=True)
            did_something.add('move')
    return (did_something, canvas)

def is_viable(threshold=2, **kw):
    (did_something, canvas) = generate_path(**kw)
    return len(did_something) > threshold

def save_path(stem='', **kw):
    (did_something, canvas) = generate_path(**kw)
    fn = stem + ".svg"
    viewbox=(0, 0, 1000, 1000)
    viewbox = str.join(' ', map(str, viewbox))
    svg = lsystem.SVG(width="1000", height="1000", viewBox=viewbox)
    path = str.join(' ', [str.join(' ', map(str, val)) for val in canvas.get_path(1000, 1000)])
    path = lsystem.Path(d=path, fill="none", stroke="black")
    svg.append(path)
    print "LSystem saving", fn
    svg.save(fn)

def save_rules(stem='', **rules):
    fn = stem + ".txt"
    f = open(fn, 'w')
    f.write(str(rules))
    f.close()

rando = RandomLSystem()
rstate = None
while 1:
    if rstate != None:
        random.setstate(rstate)
    res = rando.generate()
    res["seed"] = 1
    rstate = random.getstate()
    try:
        res["iterations"] = 1
        if not is_viable(threshold=3, **res):
            continue
    except IndexError:
        continue
    try:
        _stem = str(uuid.uuid4())
        dirstem = "rando_" + _stem
        os.mkdir(dirstem)
        stem = dirstem + "/" + _stem + "_rules"
        save_rules(stem=stem, **res)
        for itr in range(8):
            res["iterations"] = itr
            stem = dirstem + "/iteration_" + str(itr)
            save_path(stem=stem, **res)
    except IndexError:
        os.system("rm -rf " + dirstem)
