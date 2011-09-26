#!/usr/bin/python2

import sys

sys.path.insert(1, '../')

import plotter as plt

p1 = plt.plot([1,2,3],[1,3,2], 'r-o', [1,2,2.5,3], [3,2,1.5,1], 'b-o', new=True, position=[2,1,1])
p2 = plt.plot([1,2,3],[1,3,2], 'r-o', [1,2,3], [3,2,1], 'b-o', new=True, position=[2,1,2])

#print p1._datapairs[0].clipPath()



plt.show()






#plt.plot([1,2,3],[1,3,2], '')
#plt.show()
#
#plt.show()
#
#plt.plot([1,2,3],[1,3,2], '')
#plt.plot([1,2,3,4],[1,3,2,4], '')
#plt.show()


