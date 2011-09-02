#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

from plotter import *

def c():
    print p.axis('bottom').remove()

#button = QPushButton("Click")
#button.clicked.connect(c)
#button.show()


x = [1,2,3]
y = [1,2,9]

p = plot(x, y)
p.setTitle('title here')
p.setAxisLabel('bottom', 'bottom')
p.setAxisLabel('top', 'top')
p.setAxisLabel('left', 'left')
p.setAxisLabel('right', 'right')
p.setColor('#ff0000')
#print p.axis('bottom')._item
show()

#FigureManager.getActive().clear()

p.setTitle('wwwwwwwwwwwwww')
p.axis('bottom').setDataRange(0, 5)
p.setColor('#00ff00')
#print p.axis('bottom')._item
#p.axis('bottom').remove()
#print p.axis('bottom')._item
show()

p.axis('bottom').setDataRange(0, 15)
#show()






