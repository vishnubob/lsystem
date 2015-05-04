#!/usr/bin/env python

import math
import random
from . turtle import *
from . lsystem import *
import pprint

class Token(object):
    def __init__(self, token='', profile=None, **kw):
        self.token = token
        self.__dict__.update(kw)
        self.init(profile)

    def init(self, profile):
        pass

    def __str__(self):
        return self.token

    def __repr__(self):
        return "%s(**%s)" % (self.__class__.__name__, self.__dict__)

class RotationToken(Token):
    def init(self, profile):
        if getattr(self, "angle", None) == None:
            self.angle = profile.rotation
            if profile.is_negative_rotation:
                self.angle += math.pi

class DrawToken(Token):
    def init(self, profile):
        self.length = profile.draw_length

class MoveToken(Token):
    def init(self, profile):
        self.length = profile.move_length

class VariableToken(Token):
    pass

class PushToken(Token):
    pass

class PopToken(Token):
    pass

class TreeForm(object):
    def __init__(self, profile):
        self.profile = profile
        self.build_alphabet()
        self.random_rules()

    def build_alphabet(self):
        token_idx = ord('1')
        # variables
        varcnt = self.profile.variable_count
        tokens = [chr(token_idx + idx) for idx in range(varcnt)]
        self.variable_tokens = [VariableToken(token, self.profile) for token in tokens]
        token_idx += varcnt
        # rotations
        rotcnt = self.profile.rotation_count
        self.rotation_tokens = []
        for idx in range(rotcnt):
            angle = self.profile.rotation
            print math.degrees(angle)
            # positive angle
            token1 = chr(token_idx + (idx * 2))
            rtoken1 = RotationToken(token1, self.profile, angle=angle)
            self.rotation_tokens.append(rtoken1)
            # negative angle
            token2 = chr(token_idx + (idx * 2 + 1))
            rtoken2 = RotationToken(token2, self.profile, angle=-angle)
            self.rotation_tokens.append(rtoken2)
        token_idx += (rotcnt * 2)
        # move
        movecnt = self.profile.move_count
        tokens = [chr(token_idx + idx) for idx in range(movecnt)]
        self.move_tokens = [MoveToken(token, self.profile) for token in tokens]
        token_idx += movecnt
        # draw
        drawcnt = self.profile.draw_count
        tokens = [chr(token_idx + idx) for idx in range(drawcnt)]
        self.draw_tokens = [DrawToken(token, self.profile) for token in tokens]
        token_idx += drawcnt
        # push / pop
        self.push_token = PushToken("[", self.profile)
        self.pop_token = PushToken("]", self.profile)
        #
        self.tokens = self.variable_tokens + self.rotation_tokens + self.move_tokens + self.draw_tokens
        self.token_map = {token.token: token for token in (self.tokens + [self.push_token, self.pop_token])}

    def random_rule(self, tokens=None, counters=None):
        if tokens == None:
            tokens = self.tokens
        if counters == None:
            counters = {}
            counters["depth"] = self.profile.rule_depth_count
            counters["rule_count"] = max(1, self.profile.rule_length_count) * 5
        if counters["rule_count"] <= 0:
            return []
        rule_length = self.profile.rule_length_count
        counters["rule_count"] -= rule_length
        rule = []
        for rule_cnt in range(rule_length):
            if counters["depth"] > 0 and self.profile.is_subrule:
                counters["depth"] -= 1
                _rule = self.random_rule(counters=counters)
                if _rule:
                    rule.append(self.push_token)
                    rule += _rule
                    rule.append(self.pop_token)
            else:
                token = random.choice(tokens)
                rule.append(token)
        return rule

    def random_axiom(self):
        counters = {}
        counters["rule_count"] = self.profile.axiom_length
        counters["depth"] = self.profile.rule_depth_count
        tokens = self.variable_tokens + [self.push_token, self.pop_token]
        return self.random_rule(tokens=tokens, counters=counters)

    def random_rules(self):
        self.rules = {}
        for varname in self.variable_tokens:
            rule_count = self.profile.rule_count
            rlist = []
            for cnt in range(rule_count):
                rule = self.random_rule()
                rule = str.join('', map(str, rule))
                rule = {"rule": rule, "weight": 1}
                rlist.append(rule)
            self.rules[str(varname)] = rlist
        axiom = self.random_axiom()
        self.axiom = str.join('', map(str, axiom))

class TreeFormProfile(object):
    DefaultProfile = {
        "max_rule_count": 1,
        "min_rule_count": 1,
        "max_variable_count": 10,
        "min_variable_count": 3,
        "max_rotation_count": 1,
        "min_rotation_count": 1,
        "max_move_count": 1,
        "min_move_count": 0,
        "max_draw_count": 1,
        "min_draw_count": 1,
        "max_rotation": 2 * math.pi,
        "min_rotation": 0,
        "max_rule_length_count": 10,
        "min_rule_length_count": 3,
        "is_subrule_weight": .9,
        "is_negative_rotation_weight": .5,
        "max_move_length": 4,
        "min_move_length": 1,
        "max_draw_length": 4,
        "min_draw_length": 1,
        "max_axiom_length": 10,
        "min_axiom_length": 1,
        "max_rule_depth_count": 10,
        "min_rule_depth_count": 0,
    }

    def __init__(self, **profile):
        self.profile = self.DefaultProfile.copy()
        self.profile.update(profile)

    def __getattr__(self, attr):
        try:
            if attr == "rotation":
                return self.normal_rotation()
            if attr.startswith("is_"):
                wattr = attr + "_weight"
                weight = self.profile[wattr]
                return self.random_chance(weight)
            max_attr = "max_" + attr
            min_attr = "min_" + attr
            _max = self.profile[max_attr]
            _min = self.profile[min_attr]
            if type(_min) == float or type(_max) == float:
                return random.random() * (_max - _min) + _min
            else:
                return random.randint(_min, _max)
        except KeyError:
            raise AttributeError, "Unknown profile attribute: %s" % attr

    def normal_rotation(self):
        degrees = [360.0 / x for x in range(3, 9)]
        rot = random.choice(degrees)
        return math.radians(rot)

    def random_chance(self, weight):
        assert weight >= 0.0 and weight <= 1.0, weight
        return random.random() > weight

class TreeFormCanvas(object):
    def __init__(self, treeform):
        self.treeform = treeform

    def render(self, iterations=5, seed=None, limit=None):
        if seed != None:
            random.seed(seed)
        canvas = LCanvas(cursor=(500, 500), angle=math.radians(-90))
        ls = LSystem(self.treeform.rules)
        txt = ls.solve(axiom=iter(self.treeform.axiom), iterations=iterations)
        for token in txt:
            if limit != None:
                limit -= 1
                if limit < 0:
                    break
            token = self.treeform.token_map[token]
            if isinstance(token, RotationToken):
                canvas.rotate(token.angle)
            elif isinstance(token, PushToken):
                canvas.push()
            elif isinstance(token, PopToken):
                canvas.pop()
            elif isinstance(token, DrawToken):
                canvas.draw(y=token.length)
            elif isinstance(token, MoveToken):
                canvas.draw(y=token.length, move=True)
        return canvas

def save_path(canvas, fn):
    viewbox=(0, 0, 1000, 1000)
    viewbox = str.join(' ', map(str, viewbox))
    svg = lsystem.SVG(width="1000", height="1000", viewBox=viewbox)
    path = lsystem.Path(points=canvas.points, fill="none", stroke="black")
    path.transform(size=(1000, 1000), center=(500, 500))
    svg.append(path)
    svg.save(fn)

if __name__ == "__main__":
    profile = TreeFormProfile()
    tf = TreeForm(profile)
    pprint.pprint(tf.rules)
    pprint.pprint(tf.tokens)
    print tf.axiom
    tfcanvas = TreeFormCanvas(tf)
    for x in range(5):
        x += 1
        fn = "treeform_%d.svg" % x
        print fn
        canvas = tfcanvas.render(iterations=x)
        save_path(canvas, fn)
