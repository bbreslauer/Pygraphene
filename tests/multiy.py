#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from PySide.QtCore import *
from PySide.QtGui import *

from plotter import *
from font import *

x = [1,2,3,4,5,6,7,8,9]
y1 = [1,2,9,5,8,1,5]
y2 = [1, 15, 90, 89, 90, 30, 34, 60, 0]
y3 = [0, 0.01, 0.2, 0.6]

p = plot(x, y1, x, y2, x, y3)

p.setRightPadding(100)

p._axes['right'].unslave()
p._datapairs[1].setYAxis(p._axes['right'])
p._datapairs[1].setLineArgs(width=5, join='bevel')
p._axes['left'].autoscale()
p._axes['right'].autoscale()
p._axes['top'].hideTicks()

p.addAxis('y3', color='blue', width=2)
p._axes['y3'].setOrientation('vertical')
p._axes['y3'].setInside('down')
p._axes['y3'].setPlotRange(p._axes['right']._plotAnchor + 50, p._axes['right']._plotStart, p._axes['right']._plotEnd)
p._axes['y3'].setOrigin(p._axes['right']._ox, p._axes['right']._oy)
p._axes['y3'].setAxisPosition()
p._datapairs[2].setYAxis(p._axes['y3'])

p._axes['y3'].autoscale()


p._axes['right'].setColor('red')
p._axes['right'].setTicksFont(Font('Courier', size=16, style='italic', weight='bold'))
p._datapairs[1].setLineArgs(color='red')
p._datapairs[1].setMarkerArgs(color='black', width=5, style='dot', fillcolor='green', radius=10)

p._datapairs[2].setLineArgs(color='blue', width=2)
p._datapairs[2].setLineArgs(width=5, style='dashdot', cap='round')

p.draw()

#pixmap = QPixmap(600, 400)
#painter = QPainter()
#painter.begin(pixmap)
#p._figure._backend._scene.render(painter)
#painter.end()
#pixmap.save('multiy.png')


app.exec_()
sys.exit()

