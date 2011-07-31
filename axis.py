

from artist import Artist
from line import Line
from text import Text
from font import Font


class Axis(Line):

    def __init__(self, backend, plot, orientation='horizontal', inside='up', **kwargs):
        # Need label defined here because we override Line.setOrigin, which requires self._label to exist
        self._label = Text(backend)


        Line.__init__(self, backend, **kwargs)

        self._plot = plot

        self.setOrigin(0.0, 0.0)
        self._plotAnchor = 0.0
        self._plotStart = 0.0
        self._plotEnd = 0.0
        self._plotLength = 0.0
        self._dataStart = 0.0
        self._dataEnd = 0.0
        self._dataLength = 0.0

        self._majorTicks = Ticks(self._backend, self)
        self._minorTicks = Ticks(self._backend, self)


        # An axis can be slaved to zero or one other axises, but
        # an axis can be the master of an unlimited number of other
        # axises
        #
        # Slaving an axis means that it shares the data range, nothing else
        self._slavedTo = None  # axis instance
        self._masterOf = []    # list of axis instances

        # 'up' or 'down'
        self._inside = None
        self.setInside(inside)

        # 'horizontal' or 'vertical'
        self._orientation = None
        self.setOrientation(orientation)



    def setOrigin(self, x=0, y=0):
        self._label.setOrigin(x, y)
        Line.setOrigin(self, x, y)

    def mapDataToPlot(self, value):
        """
        Convert from data coords to plot coords.

        Performs the following calculation:
        ds = dataStart
        de = dataEnd
        dl = de - ds
        ps = plotStart
        pe = plotEnd
        pl = pe - ps

        return = ps + pl * (value - ds) / dl
        """

        try:
            val = self._plotStart + self._plotLength * \
                   (float(value) - self._dataStart) / self._dataLength
        except ZeroDivisionError:
            val = 0

        return val


    def mapPlotToData(self, value):
        """
        Convert from plot coords to data coords.

        Performs the following calculation:
        ds = dataStart
        de = dataEnd
        dl = de - ds
        ps = plotStart
        pe = plotEnd
        pl = pe - ps

        return = ds + dl * (value - ps) / pl
        """

        try:
            val = self._dataStart + self._dataLength * \
                    (float(value) - self._plotStart) / self._plotLength
        except ZeroDivisionError:
            val = 0

        return val


    def slaveTo(self, other):
        if isinstance(other, Axis):
            self._slavedTo = other
            other.addSlave(self)

    def addSlave(self, slave):
        try:
            self._masterOf.index(slave)
        except:
            # Only add slave if it is not already in the list
            self._masterOf.append(slave)
            

    def unslave(self):
        """
        Make this object no longer a slave.
        """

        self._slavedTo._masterOf.remove(self)
        self._slavedTo = None
        self.autoscale()

    def setOrientation(self, o):
        if o in ('horizontal', 'vertical'):
            self._orientation = o
        elif self._orientation != None:
            return
        else:
            self._orientation = 'horizontal'

        self.setAxisPosition()
        self.setLabelPosition()
        self._majorTicks.determineAxisPosition()
        self._minorTicks.determineAxisPosition()
        self.setTicks()

    def setInside(self, i):
        """
        Set which direction the plot is located from the axis.
        up means increasing plot coords, down means decreasing plot coords.

        For horizontal axes, this is self-explanatory.
        For vertical axes, up means to the right, down to the left.
        """

        if i in ('up', 'down'):
            self._inside = i
        elif self._inside != None:
            return
        else:
            self._inside = 'up'

        self.setLabelPosition()
        self._majorTicks.determineAxisPosition()
        self._minorTicks.determineAxisPosition()
        self.setTicks()


    def setPlotOrigin(self, x, y):
        """
        Set the origin of the axes (not the plot), in figure coords.
        """
        
        self.setOrigin(x, y)
        self.setTicks()

    def setPlotRange(self, anchor, start, end):
        """
        Set the start and end of the axis in plot coords.

        All values are in plot coords
        anchor = if horiz, y value. if vert, x value.
        start  = starting coordinate
        end    = ending coordinate
        """

        start = float(start)
        end = float(end)

        if start == end:
            start = start - 1.0
        elif start > end:
            start, end = end, start

        self._plotAnchor = float(anchor)
        self._plotStart = start
        self._plotEnd = end
        self._plotLength = end - start

        self.setAxisPosition()
        self.setLabelPosition()
        self.setTicks()

    def setDataRange(self, start, end, fromMaster=False):
        """
        Set the start and end of the data range.
        """
        
        # Do not change the data range if this axis is slaved, unless
        # we are calling it from the master
        if self._slavedTo is None or fromMaster is True:
            start = float(start)
            end = float(end)
    
            if start == end:
                start = start - 1.0
            elif start > end:
                start, end = end, start
    
            self._dataStart = start
            self._dataEnd = end
            self._dataLength = end - start
    
            for axis in self._masterOf:
                axis.setDataRange(start, end, True)

    def setTicksFont(self, font):
        self._majorTicks.setFont(font)
        self._minorTicks.setFont(font)

    def setLabelFont(self, font):
        self._label.setKwargs(font=font)

    def setLabelText(self, text):
        self._label.setKwargs(text=text)

    def setLabelPosition(self):

        try:
            if self._orientation == 'horizontal' and self._inside == 'up':  # bottom axis
                self._label.setKwargs({'horizontalalignment': 'center',
                                   'verticalalignment': 'top',
                                  })
                self._label.setPosition(self._plotLength / 2, self._plotAnchor - 20)
            elif self._orientation == 'horizontal' and self._inside == 'down':  # top axis
                self._label.setKwargs({'horizontalalignment': 'center',
                                   'verticalalignment': 'bottom',
                                  })
                self._label.setPosition(self._plotLength / 2, self._plotAnchor + 20)
            elif self._orientation == 'vertical' and self._inside == 'up':  # left axis
                self._label.setKwargs({'horizontalalignment': 'right',
                                   'verticalalignment': 'center',
                                   'rotation': 'vertical',
                                  })
                self._label.setPosition(self._plotAnchor - 20, self._plotLength / 2)
            elif self._orientation == 'vertical' and self._inside == 'down':  # right axis
                self._label.setKwargs({'horizontalalignment': 'left',
                                   'verticalalignment': 'center',
                                   'rotation': 'vertical',
                                  })
                self._label.setPosition(self._plotAnchor + 20, self._plotLength / 2)
            else:  # undefined axis
                self._label.setKwargs({'horizontalalignment': 'center',
                                   'verticalalignment': 'center',
                                  })
                self._label.setPosition(0, 0)
        except:
            self._label.setKwargs({'horizontalalignment': 'center',
                               'verticalalignment': 'center',
                              })
            self._label.setPosition(0, 0)

        pass

    def autoscale(self, fromMaster=False):
        """
        Autoscale the data range so that it fits all the data attached
        to it.
        """

        # Do not change the data range if this axis is slaved, unless
        # we are calling it from the master
        if self._slavedTo is None or fromMaster is True:
            start = None
            end = None
    
            datapairs = self._plot._datapairs
    
            for dp in datapairs:
                if dp._xaxis == self:
                    if start is None:
                        start = dp.minXValue()
                    else:
                        start = min(start, dp.minXValue())
                    
                    if end is None:
                        end = dp.maxXValue()
                    else:
                        end = max(end, dp.maxXValue())
    
                if dp._yaxis == self:
                    if start is None:
                        start = dp.minYValue()
                    else:
                        start = min(start, dp.minYValue())
                    
                    if end is None:
                        end = dp.maxYValue()
                    else:
                        end = max(end, dp.maxYValue())
    
            if start is None:
                start = 0.0
            if end is None:
                end = 10.0
    
            self.setDataRange(start, end)
            self.setTicks('major')
            self.setTicks('minor')

            # setDataRange will call slaves, so only need to call setTicks
            for axis in self._masterOf:
                axis.setTicks('major')
                axis.setTicks('minor')

    def setTicks(self, which='major', num=5):
        if which == 'minor':
            ticks = self._minorTicks
        else:
            ticks = self._majorTicks

        ticks.setTicksNum(num, self._dataStart, self._dataEnd)


    def setAxisPosition(self):
        """
        Recalculate the start, end, and origin points for the axis
        and set the appropriate points for the Line.
        """
        
        if self._orientation == 'horizontal':
            self.setPosition(self._plotStart, self._plotAnchor)
            self.setEnd(self._plotEnd, self._plotAnchor)
        elif self._orientation == 'vertical':
            self.setPosition(self._plotAnchor, self._plotStart)
            self.setEnd(self._plotAnchor, self._plotEnd)

    def hideTicks(self):
        self._majorTicks.setVisible(False)
        self._minorTicks.setVisible(False)

    def showTicks(self):
        self._majorTicks.setVisible(True)
        self._minorTicks.setVisible(True)

    def drawTicks(self):
        if self._visible:
            self._majorTicks.draw()
            self._minorTicks.draw()

    def draw(self, *args, **kwargs):
        Line.draw(self, *args, **kwargs)
        self._label.draw(*args, **kwargs)



class Ticks(object):

    def __init__(self, backend, axis, length=5, width=1, font=Font()):
        """
        axis is the object these ticks are attached to.
        length is the default length for each tick.
        """

        self._ticks = []
        self._backend = backend
        self._axis = axis
        self._length = length
        self._width = width
        self._font = font
        self._visible = True

        # temporary until there is a better way to set locations of ticks
        self.setTicksNum(5, 0.0, 0.0)

        # defaults
        self._tickMarkArgs = {                    
                       }

        self._labelArgs = {'horizontalalignment': 'center',
                           'verticalalignment': 'center',
                          }



    def determineAxisPosition(self):
        try:
            if self._axis._orientation == 'horizontal' and self._axis._inside == 'up':  # bottom axis
                self._labelArgs.update({'horizontalalignment': 'center',
                                   'verticalalignment': 'top',
                                  })
            elif self._axis._orientation == 'horizontal' and self._axis._inside == 'down':  # top axis
                self._labelArgs.update({'horizontalalignment': 'center',
                                   'verticalalignment': 'bottom',
                                  })
            elif self._axis._orientation == 'vertical' and self._axis._inside == 'up':  # left axis
                self._labelArgs.update({'horizontalalignment': 'right',
                                   'verticalalignment': 'center',
                                  })
            elif self._axis._orientation == 'vertical' and self._axis._inside == 'down':  # right axis
                self._labelArgs.update({'horizontalalignment': 'left',
                                   'verticalalignment': 'center',
                                  })
            else:  # undefined axis
                self._labelArgs.update({'horizontalalignment': 'center',
                                   'verticalalignment': 'center',
                                  })
        except:
            self._labelArgs.update({'horizontalalignment': 'center',
                               'verticalalignment': 'center',
                              })

    def delTicks(self):
        del self._ticks

    def setFont(self, font):
        if isinstance(font, str) or isinstance(font, Font):
            self._font = font

    def setVisible(self, v):
        if isinstance(v, bool):
            self._visible = v

    def setTicksNum(self, num, start, end):
        """
        start and end are in data coords
        num is the number of ticks to display.
        """

        self._num = int(num)
        self._start = float(start)
        self._end = float(end)

    def makeTicks(self):
        
        self.removeTicks()
        self.delTicks()
        self._ticks = []

        start = self._start
        end = self._end
        num = self._num

        delta = (float(end) - float(start)) / float(num - 1)

        for i in range(num):
            self._tickMarkArgs.update(width=self._width)
            self._labelArgs.update(text=str(start), font=self._font)

            tick = Tick(self._backend,
                        self._axis,
                        start,
                        self._length,
                        self._tickMarkArgs,
                        self._labelArgs)
            self._ticks.append(tick)
            start += delta

    def removeTicks(self):
        """
        Remove ticks from the scene.
        """

        for tick in self._ticks:
            tick.remove()

    def draw(self):
        if self._visible:
            self.makeTicks()
            for tick in self._ticks:
                tick.setTickPosition()
                tick.draw()




class Tick(object):

    def __init__(self, backend, axis, dataLoc, length, tickMarkArgs={}, labelArgs={}):
        self._tickMark = Line(backend, **tickMarkArgs)
        self._label = Text(backend, **labelArgs)
        self._axis = axis
        
        # Location where the tick should be placed, in data coords
        self._dataLocation = dataLoc

        self._length = length

    def setLabel(self, text, **kwargs):
        self._label.setKwargs(**kwargs)

    def setTickMarkArgs(self, **kwargs):
        self._tickMark.setKwargs(**kwargs)

    def setTickPosition(self):
        plotLocation = self._axis.mapDataToPlot(self._dataLocation)
        startPosition = self._axis._plotAnchor
        endPosition = startPosition

        if self._axis._inside == 'up':
            endPosition = startPosition + self._length
        elif self._axis._inside == 'down':
            endPosition = startPosition - self._length

        self._tickMark.setOrigin(self._axis._ox, self._axis._oy)
        self._label.setOrigin(self._axis._ox, self._axis._oy)

        if self._axis._orientation == 'horizontal':
            self._tickMark.setPosition(plotLocation, startPosition)
            self._tickMark.setEnd(plotLocation, endPosition)
            self._label.setPosition(plotLocation, startPosition)
        elif self._axis._orientation == 'vertical':
            self._tickMark.setPosition(startPosition, plotLocation)
            self._tickMark.setEnd(endPosition, plotLocation)
            self._label.setPosition(startPosition, plotLocation)

    def remove(self):
        self._tickMark.remove()
        self._label.remove()

    def draw(self):
        self._tickMark.draw()
        self._label.draw()


