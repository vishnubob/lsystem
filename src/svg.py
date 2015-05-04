class Style(dict):
    def __str__(self):
        style = ["%s:%s" % kv for kv in self.items()]
        style = str.join(';', style)
        return style

class Tag(dict):
    Name = "__tag__"
    Header = None

    def __init__(self, style=None, **attrs):
        if style != None:
            attrs["style"] = Style(style)
        super(Tag, self).__init__(attrs)
        self.children = []

    def __str__(self):
        attrs = ['%s="%s"' % kv for kv in self.items()]
        attrs = str.join(' ', attrs)
        if self.children:
            children = str.join('\n', map(str, self.children))
            ret = "<%s %s>\n%s\n</%s>" % (self.Name, attrs, children, self.Name)
        else:
            ret = "<%s %s />" % (self.Name, attrs)
        if self.Header != None:
            ret = self.Header + ret
        return ret
    
    def append(self, child):
        self.children.append(child)

    def get_bbox(self):
        bbox = [float("inf"), float("inf"), -float("inf"), -float("inf")]
        for (x, y) in self.get_points():
            bbox[0] = min(bbox[0], x)
            bbox[1] = min(bbox[1], y)
            bbox[2] = max(bbox[2], x)
            bbox[3] = max(bbox[3], y)
        return bbox

    def transform(self, points, size=None, center=None, keep_aspect_ratio=True):
        bbox = self.get_bbox()
        x_offset = 0 - bbox[0]
        y_offset = 0 - bbox[1]
        x_length = x_offset + bbox[2]
        y_length = y_offset + bbox[3]
        if size == None:
            size = (x_length, y_length)
        if center == None:
            center = (size[0] / 2.0, size[1] / 2.0)
        left_margin = center[0] - size[0] / 2.0
        top_margin = center[1] - size[1] / 2.0
        try:
            x_scale = size[0] / float(x_length)
        except ZeroDivisionError:
            x_scale = 1
        try:
            y_scale = size[1] / float(y_length)
        except ZeroDivisionError:
            y_scale = 1
        if keep_aspect_ratio:
            if x_length > y_length:
                if y_length * x_scale <= size[1]:
                    y_scale = x_scale
                else:
                    x_scale = y_scale
            else:
                if x_length * y_scale <= size[0]:
                    x_scale = y_scale
                else:
                    y_scale = x_scale
            top_margin += center[1] - ((y_length * y_scale / 2.0) + top_margin)
            left_margin += center[0] - ((x_length * x_scale / 2.0) + left_margin)
        for (x, y) in points:
            yield ((x + x_offset) * x_scale + left_margin, (y + y_offset) * y_scale + top_margin)

class Rect(Tag):
    Name = "rect"

class Group(Tag):
    Name = "g"

class Path(Tag):
    Name = "path"

    def __init__(self, points=None, **kw):
        super(Path, self).__init__(**kw)
        if points == None:
            points = []
        self.points = points

    def add_point(self, point, command='L'):
        self.points.append((command, ) + tuple(point))

    def add_points(self, points):
        self.points += points

    def get_points(self):
        for (cmd, x, y) in self.points:
            yield (x, y)

    def __str__(self):
        points = str.join(' ', [str.join(' ', map(str, cmdpt)) for cmdpt in self.points])
        self["d"] = points
        tagstr =  super(Path, self).__str__()
        del self["d"]
        return tagstr

    def transform(self, size=None, center=None):
        commands = (cmdpt[0] for cmdpt in self.points)
        points = ((cmdpt[1], cmdpt[2]) for cmdpt in self.points)
        new_points = []
        for (cmd, pt) in zip(commands, super(Path, self).transform(points, size=size, center=center)):
            new_points += [(cmd, ) + tuple(pt)]
        self.points = new_points

class SVG(Tag):
    Name = "svg"
    Header = '<?xml version="1.0" encoding="UTF-8" standalone="no"?>'

    def __init__(self, **kw):
        kw["xmlns"] = "http://www.w3.org/2000/svg" 
        kw["xmlns:xlink"] = "http://www.w3.org/1999/xlink"
        kw["version"] = "1.1"
        super(SVG, self).__init__(**kw)

    def save(self, svgfn):
        f = open(svgfn, 'w')
        f.write(str(self))
