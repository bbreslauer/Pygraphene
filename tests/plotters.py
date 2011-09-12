#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from PySide.QtCore import *
from PySide.QtGui import *

from plotter import *

from font import Font
from ticker import *

x = [1,2,3,4,5,6,7]
y = [1,2,9,5,5,9,0]
x2 = [1,2,2.5,5,6,7]

p = plot(x, y, 'b-^')
p.setAxisLabel('bottom', 'bottom')
p.setAxisLabel('top', 'top')
p.setAxisLabel('left', 'left')
p.setAxisLabel('right', 'right')

p.setColor('#00ff00')

p.axis('top').ticks('major').setVisible(False)

p.axis('top').setLabelFont('Comic Sans Ms')
p.axis('left').setLabelFont({'family': 'Comic Sans Ms', 'weight': 'bold'})
p.axis('right').setLabelFont(Font(weight='bold'))

p.axis('bottom').setTicksLocator('major', FixedLocator(x2, 9))
#p.axis('bottom').setTicksLocator('major', LinearLocator(15))
p.axis('bottom').setTicksLabeler('major', FormatLabeler('%.3g'))
p.axis('right').setTicksLabeler('major', FormatLabeler('%.3f'))
#p.axis('bottom').setTicksLabeler('major', StringLabeler(x))

p.axis('bottom').setDataRange(0, 5.5)
p.axis('left').setDataRange(0, 8.5)

#p._datapairs[0].setMarkersVisible(True)
#p._datapairs[0].setLinesVisible(False)

#p.axis('bottom').setLabelPosition(100,200)
#p.axis('right').setLabelPosition(-300,-100)
#p._axes['right'].setVisible(False)
#p._axes['left'].setVisible(False)
#p._axes['top'].setVisible(False)
#p._axes['bottom'].setVisible(False)
#p._figure.draw()
#listFonts()

#show()

save('p.png')

