#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from PySide.QtCore import *
from PySide.QtGui import *

from figure import *
from plot import *
from datapair import *

app = QApplication(sys.argv)

f = Figure(600, 400)
p = CartesianPlot(f, f._canvas)
p2 = CartesianPlot(f, f._canvas)
f.addPlot(p)
f.addPlot(p2)

p.setPlotRegion(0, 0, f._canvas._scene.width()/2, f._canvas._scene.height())
p2.setPlotRegion(f._canvas._scene.width()/2, 0, f._canvas._scene.width()/2, f._canvas._scene.height())

for axis in p._axes.values():
    axis._majorTicks.makeTicks(11, 0, 10)


#p._axes['top'].setVisible(False)
p._axes['left'].setColor('#ff0000')
p._axes['right'].setColor('#00ff00')
p._axes['bottom'].setWidth(2)
p._axes['right'].hideTicks()
p._axes['top'].hideTicks()

d = DataPair(f._canvas, [1,2,3,4,5,6,7], [1,2,9,5,9,1,0,5], p._axes['bottom'], p._axes['left'])
p.addDataPair(d)

f.draw()

def c():
    p.setPadding(50, 50, 50, 50)
    f.draw()
    print "hi"

#button = QPushButton("Click")
#button.clicked.connect(c)
#button.show()

app.exec_()
sys.exit()

