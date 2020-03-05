#!/usr/bin/env python3
# coding: utf8

class COLORS(object):

    def __init__(self):
        pass

    def to_rgb(self, minimum, maximum, value):
        minimum, maximum = float(minimum), float(maximum)
        ratio = 2 * (value-minimum) / (maximum - minimum)
        b = int(max(0, 255*(1 - ratio)))
        r = int(max(0, 255*(ratio - 1)))
        g = 255 - b - r
        return (r, g, b, 1)
