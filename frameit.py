#!/usr/bin/env python

import sys
import itertools
from lsystem import svg
import re

outfn = sys.argv[1]
frames = sys.argv[2:]

def grouper(n, iterable, fillvalue=None):
    args = [iter(iterable)] * n
    return itertools.izip_longest(*args, fillvalue=fillvalue)

def get_path(fn):
    path_re = re.compile("<path.*d=\"([^\"]+)\".*>")
    f = open(fn)
    for line in f:
        m = path_re.match(line)
        if m:
            path = m.group(1)
            break
    path = [(cmd, float(x), float(y)) for (cmd, x, y) in grouper(3, path.split(' '))]
    return path

paths = [svg.Path(points=get_path(fn), fill="none", stroke="black") for fn in frames]

width = 12 * 72
height = 12 * 72
gutter = 5
margin = 10

cell_width = width / 2.0 - gutter
cell_height = height / 2.0 - gutter

cell_center_x = cell_width / 2.0
cell_center_y = cell_height / 2.0

rects = []
for (idx, path) in enumerate(paths):
    if idx in (0, 1):
        center_y = cell_center_y
    else:
        center_y = cell_center_y + cell_height + gutter
    if idx in (0, 2):
        center_x = cell_center_x
    else:
        center_x = cell_center_x + cell_width + gutter
    path.transform(size=(cell_width - margin, cell_height - margin), center=(center_x, center_y))
    rect = svg.Rect(fill="none", stroke="black", height=cell_height, width=cell_width, x=center_x - cell_width / 2.0, y=center_y - cell_height / 2.0)
    rects.append(rect)

svg = svg.SVG()
for path in paths:
    svg.append(path)
for rect in rects:
    svg.append(rect)
svg.save(outfn)
