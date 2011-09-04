

from artist import Artist
from line import Line
from axis import Axis
from marker import *

class DataPair(object):
    """
    Represents a 2-D set of data. Contains the X and Y data, pointers to the
    x and y axes, and maintains the lines and markers that are drawn.
    """
    
    def __init__(self, canvas, x, y, formatString='', xaxis=None, yaxis=None, linesVisible=True, markersVisible=True, lineProps={}, markerProps={}):
        """
        **Constructor**

        x, y
            lists of something that can be plotted. Normally these are numbers, but
            they can be anything that Axis.mapDataToPlot(), min(), and max() can
            interpret.

        formatString
            a string that specifies some simple line and marker properties. An example is
            'ro' for circle markers, and markers and lines that are red. This is applied
            before the lineProps and markerProps.

        xaxis, yaxis
            the Axis instances that this data will be drawn in reference to. Usually
            xaxis is the abscissa and yaxis is the ordinate, but they can be reversed.

        linesVisible, markersVisible
            Specify whether the lines and markers should be visible universally for this
            datapair. Individual lines or markers can be hidden by updating those
            individual objects. These attributes are used to be more efficient if some
            things are not going to be drawn. If the lines or markers are changed from
            hidden to visible, the DataPair.makeLinesAndMarkers should be called before
            calling DataPair.draw or else they may not appear.

        lineProps, markerProps
            Properties for the line segments and markers that are drawn.
        """

        self._canvas = canvas

        self._lineProps = {}
        self._markerProps = {}
        self._linesVisible = linesVisible
        self._markersVisible = markersVisible

        self.setX(x)
        self.setY(y)
        self.setXAxis(xaxis)
        self.setYAxis(yaxis)
        self.setFormatString(formatString)

        self.setLineProps(**lineProps)
        self.setMarkerProps(**markerProps)

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

    def setFormatString(self, f):
        """
        Set the format string.

        The string should consist of three characters, clm. c specifies the
        color, l specifies the line, and m specifies the marker.  A color
        must be specified, but if the line or marker should be hidden, a space
        can be used in its place. A string that is not exactly three characters
        long will not be processed (and so the defaults will be used instead).
        If a string has an invalid character, then the default is used.

        The following characters are valid:

        =========   =====
        Character   Color
        =========   =====
        r           red
        g           green
        b           blue
        k           black
        w           white
        =========   =====

        =========   =====
        Character   Line Style
        =========   =====
        \-          solid
        =           dashed
        !           dash-dot
        :           dotted
        =========   =====

        =========   =====
        Character   Marker
        =========   =====
        o           circle
        =========   =====

        """
# TODO make the markerChar actually do something

        if len(f) != 3:
            return

        colors = {'r': '#ff0000',
                  'g': '#00ff00',
                  'b': '#0000ff',
                  'k': '#000000',
                  'w': '#ffffff',
                 }

        lines = {'-': 'solid',
                 '=': 'dash',
                 '!': 'dashdot',
                 ':': 'dot',
                }

        markers = {'o': 'CircleMarker',
                  }

        colorChar  = f[0]
        lineChar   = f[1]
        markerChar = f[2]

        lineProps = {}
        markerProps = {}

        if lineChar == ' ':
            self.setLinesVisible(False)

        if markerChar == ' ':
            self.setMarkersVisible(False)

        if colorChar in colors.keys():
            lineProps['color'] = colors[colorChar]
            markerProps['color'] = colors[colorChar]
            markerProps['fillcolor'] = colors[colorChar]

        if lineChar in lines.keys():
            lineProps['style'] = lines[lineChar]

        self.setLineProps(**lineProps)
        self.setMarkerProps(**markerProps)


    def setLinesVisible(self, v=True):
        """Set whether the lines are visible universally."""
        if isinstance(v, bool):
            self._linesVisible = v

    def setMarkersVisible(self, v=True):
        """Set whether the markers are visible universally."""
        if isinstance(v, bool):
            self._markersVisible = v

    def setLineProps(self, **kwprops):
        """Set the line arguments."""
        self._lineProps.update(kwprops)

    def setMarkerProps(self, **kwprops):
        """Set the marker arguments."""
        self._markerProps.update(kwprops)

    def linesVisible(self):
        """Return whether the lines are universally visible."""
        return self._linesVisible

    def markersVisible(self):
        """Return whether the markers are universally visible."""
        return self._markersVisible

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

    def makeLinesAndMarkers(self):
        """
        Create the Lines and Markers that will be drawn on the Figure.

        The Lines and Markers will only be created if they are currently
        set to be visible in this DataPair.
        """
        ox = self._xaxis._ox
        oy = self._xaxis._oy

        xPlotCoords = map(lambda value: self._xaxis.mapDataToPlot(value), self._x)
        yPlotCoords = map(lambda value: self._yaxis.mapDataToPlot(value), self._y)

        self._lineSegments = []
        self._markers = []

        # Default marker type
        markerClass = CircleMarker

        # Make the line segments
        if self.linesVisible():
            for i in range(min(len(xPlotCoords), len(yPlotCoords)) - 1):
                line = Line(self._canvas, **self._lineProps)
                line.setPoints( xPlotCoords[i],
                                yPlotCoords[i],
                                xPlotCoords[i+1],
                                yPlotCoords[i+1],
                                ox,
                                oy)
                self._lineSegments.append(line)

        # Make the markers
        if self.markersVisible():
            for x, y in zip(xPlotCoords, yPlotCoords):
                marker = markerClass(self._canvas, **self._markerProps)
                marker.setOrigin(ox, oy)
                marker.setPosition(x, y)
                self._markers.append(marker)

    def clear(self):
        self.remove()

    def remove(self):
        """
        Remove all the Lines and Markers from the Figure.
        """
        try:
            for line in self._lineSegments:
                line.remove()

            for marker in self._markers:
                marker.remove()
        except:
            # self._lineSegments or self._markers probably doesn't exist yet
            pass

    def draw(self, *args, **kwargs):
        """
        Draw the Lines and Markers to the Figure.

        Note: This does not actually override Artist.draw() because DataPair does
        not subclass Artist.
        """

        # Need to save the current lineSegments and markers so that they can be removed from
        # the plot when the plot is next drawn

        # Draw lines before markers so that the markers cover the lines when the overlap
        # on the canvas.
        if self.linesVisible():
            for line in self._lineSegments:
                line.draw()
    
        if self.markersVisible():
            for marker in self._markers:
                marker.draw()

        self._oldLineSegments = self._lineSegments
        self._oldMarkers = self._markers

