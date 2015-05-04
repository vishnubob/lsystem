#!/usr/bin/env python

import flask
from flask import Flask, make_response
import json
import math
import random
import pickle
import os
from lsystem import *

app = Flask(__name__)
pixels_per_inch = 72

class RandomWords(object):
    Words = None
    Dictonary = "/usr/share/dict/words"

    @classmethod
    def load(cls):
        if cls.Words == None:
            f = open(cls.Dictonary)
            cls.Words = f.readlines()

    @classmethod
    def __call__(cls):
        cls.load()
        return random.choice(cls.Words).strip().lower()

random_word = RandomWords.__call__

class TreeformRunner(object):
    def bootstrap(self):
        self.seed_word = random_word()
        self.profile = TreeFormProfile()
        self.treeform = TreeForm(self.profile)
        self._svg = None

    def get_svg(self):
        if self._svg == None:
            self._svg = self.frame()
        return self._svg
    svg = property(get_svg)

    def save(self):
        svgfn = self.seed_word + ".svg"
        svgfn = os.path.join("output", svgfn)
        f = open(svgfn, 'w')
        f.write(str(self.svg))
        picklefn = self.seed_word + ".pickle"
        picklefn = os.path.join("output", picklefn)
        data = {"rules": self.treeform.rules, "tokens": self.treeform.tokens}
        f = open(picklefn, 'w')
        pickle.dump(data, f)

    def render(self, iterations):
        print "iterations", iterations
        tfcanvas = TreeFormCanvas(self.treeform)
        canvas = tfcanvas.render(iterations=iterations, seed=self.seed_word, limit=1000000)
        return canvas

    def frame(self, rows=2, cols=2, iterlist=None, width=12, height=12, inner_margin=.2, outer_margin=.2, gulley=.2):
        width = width * pixels_per_inch
        height = height * pixels_per_inch
        inner_margin = inner_margin * pixels_per_inch
        outer_margin = outer_margin * pixels_per_inch
        gulley = gulley * pixels_per_inch
        cell_width = (width - (outer_margin * 2) - (inner_margin * cols * 2) - (gulley * (cols - 1))) / float(cols)
        cell_height = (height - (outer_margin * 2) - (inner_margin * rows * 2) - (gulley * (rows - 1))) / float(rows)
        if iterlist == None:
            cell_count = rows * cols
            iterlist = range(2, cell_count + 2)
        iteridx = 0
        # svg
        frame_groups = Group(id="frames")
        path_groups = Group(id="paths")
        for row in range(rows):
            y_offset = outer_margin + (2 * inner_margin * row) + (gulley * row) + (cell_height * row)
            for col in range(cols):
                x_offset = outer_margin + (2 * inner_margin * col) + (gulley * col) + (cell_width * col)
                iterations = iterlist[iteridx]
                canvas = self.render(iterations)
                # path
                path = Path(points=canvas.points, fill="none", stroke="black")
                center = (x_offset + inner_margin + cell_width / 2.0, y_offset + inner_margin + cell_height / 2.0)
                path.transform(size=(cell_width, cell_height), center=center)
                path_name = "path_%d" % iterations
                path_group = Group(id=path_name)
                path_group.append(path)
                path_groups.append(path_group)
                # frame
                style = {"stroke-width": "1", "stroke": "black", "fill": "none"}
                frame = Rect(x=x_offset, y=y_offset, width=cell_width + (2 * inner_margin), height=cell_height + (2 * inner_margin), **style)
                frame_name = "group_%d" % iterations
                frame_group = Group(id=frame_name)
                frame_group.append(frame)
                frame_groups.append(frame_group)
                iteridx += 1
        viewbox=(0, 0, width, height)
        viewbox = str.join(' ', map(str, viewbox))
        svg = SVG(width=width, height=height, viewBox=viewbox)
        svg.append(frame_groups)
        svg.append(path_groups)
        return svg

treeform = TreeformRunner()

@app.route('/')
def index():
    f = open("index.html")
    html = f.read()
    return html

@app.route('/lsystem')
def draw_svg():
    treeform.bootstrap()
    resp = {
        "name": treeform.seed_word,
        "svg": str(treeform.svg),
    }
    return flask.jsonify(**resp)

@app.route('/save')
def save_svg():
    treeform.save()
    resp = {
        "name": treeform.seed_word,
    }
    return flask.jsonify(**resp)

if __name__ == '__main__':
    app.debug = True
    app.reloader_type = "stat"
    app.run()
