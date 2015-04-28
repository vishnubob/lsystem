#!/usr/bin/env python

import flask
from flask import Flask, make_response
import json
import math
import random
from lsystem import *

app = Flask(__name__)

class TreeformRunner(object):
    def bootstrap(self):
        self.profile = TreeFormProfile()
        self.treeform = TreeForm(self.profile)

    def render(self, iterations):
        print "iterations", iterations
        tfcanvas = TreeFormCanvas(self.treeform)
        canvas = tfcanvas.render(iterations=iterations)
        return canvas

    def frame(self, rows=2, cols=2, iterlist=None, width=800, height=800, inner_margin=20, outer_margin=5, gulley=5):
        cell_width = (width - (outer_margin * 2) - (inner_margin * cols * 2) - (gulley * (cols - 1))) / float(cols)
        cell_height = (height - (outer_margin * 2) - (inner_margin * rows * 2) - (gulley * (rows - 1))) / float(rows)
        if iterlist == None:
            cell_count = rows * cols
            iterlist = range(2, cell_count + 2)
        iteridx = 0
        # svg
        viewbox=(0, 0, width, height)
        viewbox = str.join(' ', map(str, viewbox))
        svg = SVG(width=width, height=height, viewBox=viewbox)
        for row in range(rows):
            y_offset = outer_margin + (2 * inner_margin * row) + (gulley * row) + (cell_height * row)
            for col in range(cols):
                x_offset = outer_margin + (2 * inner_margin * col) + (gulley * col) + (cell_width * col)
                iterations = iterlist[iteridx]
                canvas = self.render(iterations)
                path = Path(points=canvas.points, fill="none", stroke="black")
                center = (x_offset + inner_margin + cell_width / 2.0, y_offset + inner_margin + cell_height / 2.0)
                path.transform(size=(cell_width, cell_height), center=center)
                svg.append(path)
                style = {"stroke-width": "1", "stroke": "black", "fill": "none"}
                box = Rect(x=x_offset, y=y_offset, width=cell_width + (2 * inner_margin), height=cell_height + (2 * inner_margin), **style)
                svg.append(box)
                iteridx += 1
        return svg

treeform = TreeformRunner()
treeform.bootstrap()

@app.route('/')
def hello_world():
    f = open("draw.html")
    html = f.read()
    return html

@app.route('/rules')
def get_lsystem_rules():
    resp = {}
    resp["rules"] = treeform.treeform.rules
    #resp["tokens"] = treeform.treeform.tokens
    print resp
    return flask.json.jsonify(resp)

@app.route('/draw.svg')
def draw_svg():
    treeform.bootstrap()
    svg = treeform.frame(rows=2, cols=2, width=800, height=800)
    response = make_response(str(svg))
    response.content_type = 'image/svg+xml'
    return response

if __name__ == '__main__':
    app.debug = True
    app.reloader_type = "stat"
    app.run()
