

from artist import Artist
from line import Line
from axis import Axis
from marker import *

class DataPair(object):
    """
    Represents a 2-D set of data. Contains the X and Y data, pointers to the
    x and y axes, and maintains the lines and markers that are drawn.
    """
    
# TODO should add line and marker visible attributes, so that it is easier and more
# efficient to disable drawing of either one
    def __init__(self, backend, x, y, xaxis, yaxis, lineArgs={}, markerArgs={}):
        """
        **Constructor**

        x, y
            lists of something that can be plotted. Normally these are numbers, but
            they can be anything that Axis.mapDataToPlot(), min(), and max() can
            interpret.
        xaxis, yaxis
            the Axis instances that this data will be drawn in reference to. Usually
            xaxis is the abscissa and yaxis is the ordinate, but they can be reversed.

        lineArgs
            Keyword arguments for the line segments that are drawn.

        markerArgs
            Keyword arguments for the markers that are drawn.
        """

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
        """Set the x data."""
        if isinstance(x, list):
            self._x = x

    def setY(self, y):
        """Set the y data."""
        if isinstance(y, list):
            self._y = y

    def setXAxis(self, xaxis):
        """Set the x axis."""
        if isinstance(xaxis, Axis):
            self._xaxis = xaxis
        else:
            self._xaxis = None

    def setYAxis(self, yaxis):
        """Set the y axis."""
        if isinstance(yaxis, Axis):
            self._yaxis = yaxis
        else:
            self._yaxis = None

    def setLineArgs(self, **args):
        """Set the line arguments."""
        self._lineArgs.update(args)

    def setMarkerArgs(self, **args):
        """Set the marker arguments."""
        self._markerArgs.update(args)

    def maxXValue(self):
        """Get the maximum value in the x data."""
        return max(self._x)

    def maxYValue(self):
        """Get the maximum value in the y data."""
        return max(self._y)

    def minXValue(self):
        """Get the minimum value in the x data."""
        return min(self._x)

    def minYValue(self):
        """Get the minimum value in the y data."""
        return min(self._y)

# TODO making the lines and markers should be separated out from
# actually drawing them, and maybe we should subclass Artist, as is done with Axis
    def draw(self, *args, **kwargs):
        """
        Make the lines and markers and draw them to the Figure.

        Note: This does not actually override Artist.draw() because DataPair does
        not subclass Artist.
        """

        ox = self._xaxis._ox
        oy = self._xaxis._oy

        xPlotCoords = map(lambda value: self._xaxis.mapDataToPlot(value), self._x)
        yPlotCoords = map(lambda value: self._yaxis.mapDataToPlot(value), self._y)

        lineSegments = []
        markers = []

        # Default marker type
        markerClass = CircleMarker

        # Make the line segments
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

        # Make the markers
        for x, y in zip(xPlotCoords, yPlotCoords):
            marker = markerClass(self._backend, **self._markerArgs)
            marker.setOrigin(ox, oy)
            marker.setPosition(x, y)
            markers.append(marker)
            marker.draw()

