

from artist import Artist
from line import Line
from axis import Axis
#from plot import Plot
from marker import *

class DataPair(object):
    """
    Represents a 2-D set of data. Contains the X and Y data, pointers to the
    x and y axes, and maintains the lines and markers that are drawn.
    """
    
    def __init__(self, canvas, x, y, formatString='', plot=None, xaxis=None, yaxis=None, linesVisible=True, markersVisible=True, lineProps={}, markerProps={}):
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
        self._markerClass = CircleMarker

        self.setX(x)
        self.setY(y)
        self.setXAxis(xaxis)
        self.setYAxis(yaxis)
        self.setPlot(plot)
        self.setFormatString(formatString)

        self.setLineProps(**lineProps)
        self.setMarkerProps(**markerProps)

    def canvas(self):
        return self._canvas

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

    def setPlot(self, plot):
        """Set the plot this DataPair is attached to."""
        #if isinstance(plot, Plot):
        if True:
            self._plot = plot
        else:
            self._plot = None

    def plot(self):
        return self._plot

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
        s           square
        |           vertical
        \-          horizontal
        +           plus
        x           x
        *           star
        =========   =====

        """

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
        
        self.setMarkerType(markerChar)
        self.setLineProps(**lineProps)
        self.setMarkerProps(**markerProps)

    def setMarkerType(self, m='o'):
        """
        Set the marker type. This accepts any single character
        string accepted as a marker for the format string, or
        the following strings:

        none
        circle
        square
        vertical line
        horizontal line
        plus
        x
        star
        """
        
        markers = {'o': CircleMarker,
                   'circle': CircleMarker,
                   's': SquareMarker,
                   'square': SquareMarker,
                   '|': VerticalMarker,
                   'vertical': VerticalMarker,
                   '-': HorizontalMarker,
                   '_': HorizontalMarker,
                   'horizontal': HorizontalMarker,
                   '+': PlusMarker,
                   'plus': PlusMarker,
                   'x': XMarker,
                   '*': StarMarker,
                   'star': StarMarker,
                  }

        if m in markers.keys():
            self._markerClass = markers[m]
        else:
            self._markerClass = None

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
        """
        Set the marker arguments.

        In addition to accepting marker arguments, this also accepts
        a keyword 'marker' which, if specified, will call setMarkerType
        with the value.
        """

        if 'marker' in kwprops.keys():
            self.setMarkerType(kwprops.pop('marker'))

        self._markerProps.update(kwprops)

    def linesVisible(self):
        """Return whether the lines are universally visible."""
        return self._linesVisible

    def markersVisible(self):
        """Return whether the markers are universally visible."""
        return self._markersVisible

    def xAxis(self):
        """Return the x Axis instance."""
        return self._xaxis

    def yAxis(self):
        """Return the y Axis instance."""
        return self._yaxis

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

        (ox, oy, w, h) = self.plot().axesRegion()

        minX = self.xAxis().position()[0]
        maxX = self.xAxis().end()[0]
        minY = self.yAxis().position()[1]
        maxY = self.yAxis().end()[1]

        xPlotCoords = map(lambda value: self._xaxis.mapDataToPlot(value), self._x)
        yPlotCoords = map(lambda value: self._yaxis.mapDataToPlot(value), self._y)

        self._lineSegments = []
        self._markers = []

        # Make the line segments
        if self.linesVisible():
            for i in range(min(len(xPlotCoords), len(yPlotCoords)) - 1):
                x1 = xPlotCoords[i]
                x2 = xPlotCoords[i+1]
                y1 = yPlotCoords[i]
                y2 = yPlotCoords[i+1]

                # Do not bother making this line because it is entirely 
                # outside the plot's view. This does not get all the possible
                # lines, but will get some fraction of them. The rest will
                # be clipped by the canvas, so we don't really have to worry
                # about them. This is primarily useful for instances like when
                # x=range(0, 1000) but the plot is only showing (0, 10).
                if (x1 < minX and x2 < minX) or (x1 > maxX and x2 > maxX) \
                or (y1 < minY and y2 < minY) or (y1 > maxY and y2 > maxY):
                    continue

                line = Line(self.canvas(), **self._lineProps)
                line.setPoints(x1,
                               y1,
                               x2,
                               y2,
                               ox,
                               oy)
                line.setClipPath(self.plot().axesRegion())
                self._lineSegments.append(line)

        # Make the markers
        if self.markersVisible() and self._markerClass is not None:
            for x, y in zip(xPlotCoords, yPlotCoords):
                # Do not bother making this marker because it is outside
                # the plot's view
                if (x < minX or x > maxX) or (y < minY or y > maxY):
                    continue

                marker = self._markerClass(self.canvas(), **self._markerProps)
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
        print "lines: " + str(len(self._lineSegments))
        print "markers: " + str(len(self._markers))

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

