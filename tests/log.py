#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from plotter import *
from ticker import *

x = range(1, 1000)
y = [i * i for i in x]



p = plot(x, y, 'k- ')
p.axis('bottom').setDataRange(0.00001, 1000)
p.axis('bottom').setLog()
p.axis('left').setLog()
#p.axis('bottom').setScaling('log')
#p.axis('bottom').setTicksLocator('major', LogLocator(10))
#p.axis('bottom').setTicksLocator('minor', LogLocator(10, [1,2,3, 4, 5, 6, 7, 8, 9]))
#p.axis('bottom').setTicksLabeler('major', FormatLabeler('%.1g'))
#p.axis('left').setVisible(False)
#p.axis('right').setVisible(False)
#p.axis('top').setVisible(False)

show()




