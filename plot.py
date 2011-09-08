
from artist import Artist
from axis import Axis
from datapair import DataPair
from text import *
from base import Parent

class Plot(Artist):
    """
    Abstract class defining necessary methods for any plot class.
    """

    def __init__(self, figure, canvas):
        """
        **Constructor**

        figure
            The figure to draw the plot on.
        canvas
            The canvas that the figure uses.
        """
        self._figure = figure
        Artist.__init__(self, canvas)

class CartesianPlot(Plot):
    """
    A cartesian plot. The plot contains a title and four initial axes. The plot can
    contain any number of DataPairs.

    The plot's location is specified by an origin point in figure coordinates, along
    with a width and a height. This specifies the absolute size of the plot; the actual
    space contained within the axes will almost certainly be smaller, in order to 
    leave space for the plot title, the axis labels, and the tick marks/labels. The
    amount of space between this absolute plot size and the locations of the axes is
    defined as the plot padding.
    """

    def __init__(self, figure, canvas):
        Plot.__init__(self, figure, canvas)

        # Make the plot background white
        self.setColor('#ffffff')

        self._title = Text(self._canvas)
        self._title.setOrigin(0, 0)
        self.setTitle('')

        self._axes = {}
        self._defaultAxes = {}
        self.addInitialAxes()

        self._datapairs = []

        self._plotWidth = 0
        self._plotHeight = 0
        self._tpad = 0
        self._rpad = 0
        self._bpad = 0
        self._lpad = 0

        self.setPadding()

    def title(self):
        return self._title

    def setTitlePosition(self):
        """
        Set the position for the title. Currently, this is centered at the top of the
        plot, but in the future it may take x and y arguments.
        """

        self._title.setOrigin(*self.origin())
        self._title.setPosition(self._plotWidth / 2, self._plotHeight - 10)

    def setPlotLocation(self, nRows, nCols, num):
        """
        A simple way to set the plot region. Specify how many rows and columns
        should be on the figure, and which plot this is, and then calculate
        the appropriate region.
        """

        
        num -= 1  # need to zero-index the plot number so that div and mod work properly
        row = num / nCols
        col = num % nCols
        
        # We are setting the plot region using figure coordinates, which are from
        # the bottom to the top. But plot #1 should be at the top-left corner, so
        # to convert to the top, we invert the row value. The -1 is used because
        # we still need to specify the bottom-left corner of the plot.
        invertRow = nRows - row - 1

        plotWidth = float(self._figure.width()) / float(nCols)
        plotHeight = float(self._figure.height()) / float(nRows)

        x = float(col) * plotWidth
        y = float(invertRow) * plotHeight

        self.setPlotRegion(x, y, plotWidth, plotHeight)

    def setPlotRegion(self, x, y, width, height):
        """
        Set the region of the figure that this plot may occupy, in figure coordinates.
        """

        self.setOrigin(x, y)
        self._plotWidth = width
        self._plotHeight = height

        self.setAxesRegion()
        self.setTitlePosition()

    def setPadding(self, top=50, right=50, bottom=50, left=50):
        """
        Set the padding between the plot region (the area of the figure that this 
        plot can occupy) and the axes.

        Padding values must be non-negative integers.
        """
        
        if isinstance(top, int) and top >= 0:
            self._tpad = top
        if isinstance(right, int) and right >= 0:
            self._rpad = right
        if isinstance(bottom, int) and bottom >= 0:
            self._bpad = bottom
        if isinstance(left, int) and left >= 0:
            self._lpad = left
        
        self.setAxesRegion()

    def setTopPadding(self, p):
        """
        Set the padding for just the top of the plot.

        Padding value must be a non-negative integer.
        """
        if isinstance(p, int) and p >= 0:
            self._tpad = p
            self.setAxesRegion()

    def setRightPadding(self, p):
        """
        Set the padding for just the right of the plot.

        Padding value must be a non-negative integer.
        """
        if isinstance(p, int) and p >= 0:
            self._rpad = p
            self.setAxesRegion()

    def setBottomPadding(self, p):
        """
        Set the padding for just the bottom of the plot.

        Padding value must be a non-negative integer.
        """
        if isinstance(p, int) and p >= 0:
            self._bpad = p
            self.setAxesRegion()

    def setLeftPadding(self, p):
        """
        Set the padding for just the left of the plot.

        Padding value must be a non-negative integer.
        """
        if isinstance(p, int) and p >= 0:
            self._lpad = p
            self.setAxesRegion()

    def setAxesRegion(self):
        """
        Calculate the region that the axes can occupy, in figure coordinates.

        This is basically the plot region made smaller by the padding on each axis.
        """

        # Origin of axes, in figure coords
        self._axesOx = self._ox + self._lpad
        self._axesOy = self._oy + self._bpad

        # Length of axes
        self._axesWidth = self._plotWidth - self._rpad - self._lpad
        self._axesHeight = self._plotHeight - self._tpad - self._bpad

        self._axes['left'].setOrigin(self._axesOx, self._axesOy)
        self._axes['right'].setOrigin(self._axesOx, self._axesOy)
        self._axes['top'].setOrigin(self._axesOx, self._axesOy)
        self._axes['bottom'].setOrigin(self._axesOx, self._axesOy)

        self._axes['left'].setPlotRange(0, 0, self._axesHeight)
        self._axes['right'].setPlotRange(self._axesWidth, 0, self._axesHeight)
        self._axes['top'].setPlotRange(self._axesHeight, 0, self._axesWidth)
        self._axes['bottom'].setPlotRange(0, 0, self._axesWidth)

    def width(self):
        return self._plotWidth

    def height(self):
        return self._plotHeight

    def addAxis(self, key, **kwprops):
        """
        Add a new axis to the plot, with its name given by key. If key already exists,
        do nothing.

        Return the axis, regardless of whether it already exists or was just created.
        """

        if key not in self._axes.keys():
            self._axes[key] = Axis(self._figure._canvas, self, **kwprops)
            self.addChild(self._axes[key])
        return self._axes[key]

    def addInitialAxes(self, **kwprops):
        """
        Create the initial 4 axes. These are given the names top, bottom, left, right.
        """

        for key in ('left', 'top', 'right', 'bottom'):
            self.addAxis(key, **kwprops)

        self._axes['left'].setOrientation('vertical')
        self._axes['right'].setOrientation('vertical')
        self._axes['top'].setOrientation('horizontal')
        self._axes['bottom'].setOrientation('horizontal')

        self._axes['right'].setInside('down')
        self._axes['top'].setInside('down')
        self._axes['left'].setInside('up')
        self._axes['bottom'].setInside('up')

        self._axes['right'].slaveTo(self._axes['left'])
        self._axes['top'].slaveTo(self._axes['bottom'])

        self._defaultAxes['x'] = self._axes['bottom']
        self._defaultAxes['y'] = self._axes['left']

    def addDataPair(self, datapair):
        """
        Add a DataPair to this plot. datapair must be a DataPair instance, or nothing
        happens.
        """
        if isinstance(datapair, DataPair):
            if datapair.xAxis() is None:
                datapair.setXAxis(self._defaultAxes['x'])
            if datapair.yAxis() is None:
                datapair.setYAxis(self._defaultAxes['y'])
            self._datapairs.append(datapair)
            self.addChild(datapair)

    def removeDataPair(self, datapair):
        """
        Remove the specified DataPair from this plot. Returns True if it was removed,
        False if it was not or the specified DataPair did not exist in the Plot.
        """

        try:
            self._datapairs.remove(datapair)
            return True
        except:
            return False

    def setTitle(self, text=None, font=None):
        """
        Set the title label.

        text can be either a str, a Text object, or a dict. If it is a str, then
        the current label's text is updated. If it is a Text object, then
        the current label is replaced with title. If it is a dict, then the
        current Text object is updated with the properties in the dict. If it is none
        of these (i.e. None) then the text is not updated.

        After that is done, if font is not None, then the title's font will
        be updated. font can be a string or Font object.
        """

        if text is not None:
            if isinstance(text, Text):
                self._title = text
            elif isinstance(text, str):
                self._title.setProps(text=text)
            elif isinstance(text, dict):
                self._title.setProps(**text)

        if font is not None:
            if isinstance(font, str) or isinstance(font, Font):
                self._title.setProps(font=font)

    def setAxisLabel(self, key='bottom', label='', font=''):
        """
        Set the label (and label font) for the axis with the name given by key.
        """

        try:
            self._axes[key].setLabelText(label)
            self._axes[key].setLabelFont(font)
        except:
            pass

    def setAxisAutoscale(self, key='bottom', autoscale=True):
        """
        Set the axis with the name given by key to autoscale to its data range.
        """

        if isinstance(autoscale, bool):
            try:
                self._axes[key]._autoscaled = autoscale
            except:
                pass

    def axis(self, key):
        """
        Return the axis with the name given by key. If the key does not exist,
        then this raises a KeyError.
        """
        return self._axes[key]

    def clear(self):
        Parent.clear(self)
        self._canvas.update()

    def _draw(self):
        self.clear()
        item = self.drawBackground()
        self.drawAxes()
        self.drawData()
        self._title.draw()
        return item

    def drawBackground(self):
        """
        Draw the background color of the plot. This only colors in the space
        between the axes.
        """
        
        sx, sy = self.axis('bottom').start()
        ex, ey = self.axis('top').end()
        ox, oy = self.axis('bottom').origin()

        # origin of the plot is the position of the plot in figure coordinates
        return self._canvas.drawRect(sx, sy, ex, ey, ox, oy, **{'color': self.color(), 'fillcolor': self.color()})


    def drawAxes(self):
        """
        Draw the axes and tick marks for the plot.
        """

        axes = self._axes.values()
        
        for axis in axes:
            if axis._autoscaled:
                axis.autoscale()

        for axis in axes:
            axis.draw()
        
        # need to draw ticks here so that they cover up the axis
        for axis in axes:
            axis.drawTicks()

    def drawData(self):
        """
        Draw all the data attached to this plot.
        """
        
        for datapair in self._datapairs:
            datapair.remove()
            datapair.makeLinesAndMarkers()
            datapair.draw()

