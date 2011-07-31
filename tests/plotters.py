#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from PySide.QtCore import *
from PySide.QtGui import *

from plotter import *

app = QApplication(sys.argv)

x = [1,2,3,4,5,6,7]
y = [1,2,9,5,9,1,0]

p = plot(x, y)
p.setAxisLabel('bottom', 'bottom')
p.setAxisLabel('top', 'top')
p.setAxisLabel('left', 'left')
p.setAxisLabel('right', 'right')
#p._axes['right'].setVisible(False)
#p._axes['top'].setVisible(False)
#p._axes['bottom'].setVisible(False)
#p._figure.draw()
#listFonts()

show()

app.exec_()
sys.exit()

