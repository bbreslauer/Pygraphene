#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from plotter import *

from PySide.QtGui import QPushButton

def clearfig():
    FigureManager.getActive().clear()

figbutton = QPushButton("Clear Figure")
figbutton.clicked.connect(clearfig)





x = [1,2,3]
y = [1,2,9]

p = plot(x, y, new=True, position=[2, 1, 1])
p2 = plot(x, y, new=True, position=[2, 1, 2])
p.setColor('#ff0000')


p.setTitle('original')
p2.setTitle('second plot')


def clearp():
    p.clear()

pb = QPushButton("Clear plot 1")
pb.clicked.connect(clearp)





p.axis('left').setVisible(False)
p.axis('right').setVisible(False)
p.axis('top').setVisible(False)
#p.axis('bottom').setVisible(False)
#p.setTitle({'visible': False})
FigureManager.getActive().setTitle({'visible': False})

#p.axis('left')._label.setVisible(False)
#p.axis('right')._label.setVisible(False)
#p.axis('top')._label.setVisible(False)
#p.axis('bottom')._label.setVisible(False)

p.axis('right').setLabelText('right')

figbutton.show()
pb.show()
show()


FigureManager.getActive().clear()




p.setColor('#00ff00')

figbutton.show()
pb.show()
show()






