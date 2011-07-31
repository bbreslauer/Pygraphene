
from artist import Artist
from axis import Axis
from datapair import DataPair
from text import *

class Plot(Artist):
    """
    Abstract class defining necessary methods for any plot class.
    """

    def __init__(self, backend):
        Artist.__init__(self, backend)

class CartesianPlot(Plot):
    """
    Cartesian plot.
    """

    def __init__(self, figure, backend):

        Plot.__init__(self, backend)

        self._figure = figure

        self._title = Text(self._backend)
        self._title.setOrigin(0, 0)
        self.setTitle('')

        self._axes = {}
        self.addAxes()

        self._datapairs = []

        self._plotWidth = 0
        self._plotHeight = 0
        self._tpad = 0
        self._rpad = 0
        self._bpad = 0
        self._lpad = 0

        self.setPadding()

    def setTitlePosition(self):
        self._title.setPosition(self._plotWidth / 2, self._plotHeight - 10)

    def setPlotRegion(self, x, y, width, height):
        """
        Set the region of the figure (in figure coords) that this
        plot may occupy.
        """
        
        self.setOrigin(x, y)
        self._plotWidth = width
        self._plotHeight = height

        self.setAxesRegion()
        self.setTitlePosition()

    def setPadding(self, top=50, right=50, bottom=50, left=50):
        """
        Set the padding between the region this plot can occupy
        and the axes.
        """

        self._tpad = top
        self._rpad = right
        self._bpad = bottom
        self._lpad = left
        
        self.setAxesRegion()

    def setTopPadding(self, p):
        self._tpad = p
        self.setAxesRegion()

    def setRightPadding(self, p):
        self._rpad = p
        self.setAxesRegion()

    def setBottomPadding(self, p):
        self._bpad = p
        self.setAxesRegion()

    def setLeftPadding(self, p):
        self._lpad = p
        self.setAxesRegion()

    def setAxesRegion(self):
        """
        Calculate the region that the axes can occupy, in figure coords.
        """

        # Origin of axes, in figure coords
        self._axesOx = self._ox + self._tpad
        self._axesOy = self._oy + self._tpad

        # Length of axes
        self._axesWidth = self._plotWidth - self._rpad - self._lpad
        self._axesHeight = self._plotHeight - self._tpad - self._bpad

        self._axes['left'].setPlotOrigin(self._axesOx, self._axesOy)
        self._axes['right'].setPlotOrigin(self._axesOx, self._axesOy)
        self._axes['top'].setPlotOrigin(self._axesOx, self._axesOy)
        self._axes['bottom'].setPlotOrigin(self._axesOx, self._axesOy)

        self._axes['left'].setOrientation('vertical')
        self._axes['right'].setOrientation('vertical')
        self._axes['top'].setOrientation('horizontal')
        self._axes['bottom'].setOrientation('horizontal')

        self._axes['right'].setInside('down')
        self._axes['top'].setInside('down')
        
        self._axes['left'].setPlotRange(0, 0, self._axesHeight)
        self._axes['right'].setPlotRange(self._axesWidth, 0, self._axesHeight)
        self._axes['top'].setPlotRange(self._axesHeight, 0, self._axesWidth)
        self._axes['bottom'].setPlotRange(0, 0, self._axesWidth)
       
    def setAxesDataRange(self):
        self._axes['left'].setDataRange(0, 10)
        self._axes['right'].setDataRange(0, 10)
        self._axes['top'].setDataRange(0, 10)
        self._axes['bottom'].setDataRange(0, 10)

    def addAxis(self, key, **kwargs):
        if key not in self._axes.keys():
            self._axes[key] = Axis(self._figure._backend, self, **kwargs)

    def addAxes(self):
        self._axes['left']   = Axis(self._figure._backend, self)
        self._axes['top']    = Axis(self._figure._backend, self)
        self._axes['right']  = Axis(self._figure._backend, self)
        self._axes['bottom'] = Axis(self._figure._backend, self)

    def addDataPair(self, datapair):
        if isinstance(datapair, DataPair):
            self._datapairs.append(datapair)

    def setTitle(self, title):
        if isinstance(title, Text):
            self._title = title
        elif isinstance(title, str):
            self._title.setKwargs(text=title)


    def _draw(self):
        self.drawAxes()
        self.drawData()
        self._title.draw()


    def drawAxes(self):
        axes = self._axes.values()
        
        # need to draw ticks here so that they don't cover up the axis
        for axis in axes:
            axis.drawTicks()

        for axis in axes:
            axis.draw()

    def drawData(self):
        # draw the data
        for datapair in self._datapairs:
            datapair.draw()







