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
p._axes['bottom'].setLabelText('bottom')
p._axes['top'].setLabelText('top')
p._axes['left'].setLabelText('left')
p._axes['right'].setLabelText('right')
#p._axes['right'].setVisible(False)
#p._axes['top'].setVisible(False)
#p._axes['bottom'].setVisible(False)
p._figure.draw()
#listFonts()

app.exec_()
sys.exit()

