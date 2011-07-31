

from artist import Artist
from line import Line
from axis import Axis
from marker import *

class DataPair(object):
    

    def __init__(self, backend, x, y, xaxis, yaxis, lineArgs={}, markerArgs={}):

        self._backend = backend

        self.setX(x)
        self.setY(y)
        self.setXAxis(xaxis)
        self.setYAxis(yaxis)

        self._lineArgs = {}
        self._markerArgs = {}
        self.setLineArgs(**lineArgs)
        self.setMarkerArgs(**markerArgs)



    def setX(self, x):
        if isinstance(x, list):
            self._x = x

    def setY(self, y):
        if isinstance(y, list):
            self._y = y

    def setXAxis(self, xaxis):
        if isinstance(xaxis, Axis):
            self._xaxis = xaxis
        else:
            self._xaxis = None

    def setYAxis(self, yaxis):
        if isinstance(yaxis, Axis):
            self._yaxis = yaxis
        else:
            self._yaxis = None

    def setLineArgs(self, **args):
        self._lineArgs.update(args)

    def setMarkerArgs(self, **args):
        self._markerArgs.update(args)

    def maxXValue(self):
        return max(self._x)

    def maxYValue(self):
        return max(self._y)

    def minXValue(self):
        return min(self._x)

    def minYValue(self):
        return min(self._y)


    def draw(self, *args, **kwargs):
        ox = self._xaxis._ox
        oy = self._xaxis._oy

        xPlotCoords = map(lambda value: self._xaxis.mapDataToPlot(value), self._x)
        yPlotCoords = map(lambda value: self._yaxis.mapDataToPlot(value), self._y)

        lineSegments = []
        markers = []

        markerClass = CircleMarker

        for i in range(min(len(xPlotCoords), len(yPlotCoords)) - 1):
            line = Line(self._backend, **self._lineArgs)
            line.setPoints( xPlotCoords[i],
                            yPlotCoords[i],
                            xPlotCoords[i+1],
                            yPlotCoords[i+1],
                            ox,
                            oy)

            # TODO is this really needed? do we save the lines for later use?
            lineSegments.append(line)
            line.draw()

        for x, y in zip(xPlotCoords, yPlotCoords):
            marker = markerClass(self._backend, **self._markerArgs)
            marker.setOrigin(ox, oy)
            marker.setPosition(x, y)
            markers.append(marker)
            marker.draw()


