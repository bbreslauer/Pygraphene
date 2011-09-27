#!/usr/bin/python2

import sys
import math

sys.path.insert(1, '../')

from plotter import *
from ticker import *

x = range(361)
y = map(lambda x:math.sin(x * math.pi / 180), x)


p = plot(x, y, 'b=o')

p.axis('bottom').setTicksLabeler('major', FormatLabeler('%.1d'), True)
p.axis('left').setTicksLabeler('major', FormatLabeler('%.2g'), True)

#p.axis('left').setTicksLocator('major', SpacedLocator(0.5, 0), True)

p.axis('bottom').setDataRange(0, 10)

show()

