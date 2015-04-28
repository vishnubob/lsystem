import numpy as np
import math

class LCanvas(object):
    def __init__(self, cursor=(0, 0), angle=0):
        self.context = []
        self.cursor = np.asarray(map(float, cursor))
        self.angle = angle
        self.points = []
        self.add_point(command='M')

    def draw(self, x=0, y=0, move=False):
        point = np.asarray(map(float, (x, y)))
        rotmat = np.matrix([[math.cos(self.angle), -math.sin(self.angle)], [math.sin(self.angle), math.cos(self.angle)]])
        point = np.asarray(np.rot90(rotmat * np.rot90(np.asmatrix(point))))[0]
        self.cursor = self.cursor + point
        if move:
            command = 'M'
        else:
            command = 'L'
        self.add_point(command=command)

    def rotate(self, angle):
        self.angle += angle

    def push(self):
        self.context.append((self.cursor, self.angle))

    def pop(self):
        (self.cursor, self.angle) = self.context.pop()
        self.add_point(command='M')

    def add_point(self, point=None, command='L'):
        if point == None:
            point = self.cursor
        self.points.append((command, ) + tuple(point))

