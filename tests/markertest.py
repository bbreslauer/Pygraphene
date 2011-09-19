#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from PySide.QtCore import *
from PySide.QtGui import *

from marker import *

from canvas.qt4pyside_canvas import *

q = QApplication(sys.argv)
canvas = Qt4PySideCanvas(600, 400)

markerClasses = (CircleMarker,
                 SquareMarker,
                 VerticalMarker,
                 HorizontalMarker,
                 PlusMarker,
                 XMarker,
                 StarMarker,
                 UpTriangleMarker,
                 DownTriangleMarker,
                 LeftTriangleMarker,
                 RightTriangleMarker,
          )

markers = []

props = dict(color='#ff0000', fillcolor='#00ff00', width=1)

for row, markerClass in zip(range(1, len(markerClasses) + 1), markerClasses):
    for col in range(1, 8):
        m = markerClass(canvas, 3 * col, **props)
        m.setPosition(50 * row, 50 * col)
        markers.append(m)


for marker in markers:
    marker.draw()


q.exec_()

