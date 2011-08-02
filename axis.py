

from artist import Artist
from line import Line
from text import Text
from font import Font
from locator import *

class Axis(Line):
    """
    Represent an axis on a Plot.

    An Axis is attached to exactly one Plot. In addition to being a Line, the
    Axis also contains a label and major and minor Ticks.

    The Axis maintains its current location on the Plot as well as the data range
    that it represents.

    The orientation of an Axis can either be 'horizontal' or 'vertical'.

    The Axis also defines which side of it points to the inside of the plot. Valid
    values are 'up' and 'down', which refer to the direction that Figure (or,
    equivalently, Plot) coordinates incrase. For a horizontal axis, this is
    self-explanatory (for a bottom axis, up, and for a top axis, down). For a
    vertical axis this means that a left axis is up, and a right axis is down.

    And now for a simple table explaining this:

    =============   ============    ======
    Axis Location   Orientation     Inside
    =============   ============    ======
    bottom          horizontal      up
    top             horizontal      down
    left            vertical        up
    right           vertical        down
    =============   ============    ======

    It is possible to slave an Axis to another Axis. If this is done, then both Axes
    will share the same data range. A user can only change the data range on the
    master Axis, not the slave (nothing will happen if the user tries to modify the
    slave's data range). An Axis can be either a slave, a master, or neither; it
    cannot be both a slave and a master.
    """

    def __init__(self, backend, plot, orientation='horizontal', inside='up', **kwargs):
        # Need to define the label before init'ing the Line. This is because we
        # override Line.setOrigin to include the label, but setOrigin is called
        # in Line.__init__.
        self._label = Text(backend)

        Line.__init__(self, backend, **kwargs)

        self._plot = plot

        # Set default location values
        self.setOrigin(0.0, 0.0)
        self._plotAnchor = 0.0
        self._plotStart = 0.0
        self._plotEnd = 0.0
        self._plotLength = 0.0
        self._dataStart = 0.0
        self._dataEnd = 0.0
        self._dataLength = 0.0
        self._autoscaled = True  # holds whether this Axis is currently being autoscaled to the data

        # Setup the major and minor ticks
        self._majorTicks = Ticks(self._backend, self, 'major', labeler=StringLabeler())
        self._minorTicks = Ticks(self._backend, self, 'minor', labeler=NullLabeler())
        self._minorTicks.setLocator(num=3)
        self._minorTicks.setLength(3)
        self._minorTicks._labelArgs.update(visible=False)


        self._slavedTo = None  # pointer to this Axis' master
        self._masterOf = []    # list of pointers to this Axis' slaves

        # 'up' or 'down'
        self._inside = None
        self.setInside(inside)

        # 'horizontal' or 'vertical'
        self._orientation = None
        self.setOrientation(orientation)

    def setOrigin(self, x=0, y=0):
        """
        Set the origin, using figure coordinates.
        """
        self._label.setOrigin(x, y)
        Line.setOrigin(self, x, y)

    def mapDataToPlot(self, value):
        """
        Convert value from data coordinates to plot coordinates. If the data range
        does not actually span any range (say, because both the start and end
        are 0), then this will always return 0.

        The algorithm performed is:

        | ds = dataStart
        | de = dataEnd
        | dl = de - ds = dataLength
        | ps = plotStart
        | pe = plotEnd
        | pl = pe - ps = plotLength

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
        Convert value from plot coordinates to data coordinates. If the axis has
        no length (probably because it has not yet been attached to a Plot),
        then this will always return 0.

        The algorithm performed is:

        | ds = dataStart
        | de = dataEnd
        | dl = de - ds = dataLength
        | ps = plotStart
        | pe = plotEnd
        | pl = pe - ps = plotLength

        return = ds + dl * (value - ps) / pl
        """

        try:
            val = self._dataStart + self._dataLength * \
                    (float(value) - self._plotStart) / self._plotLength
        except ZeroDivisionError:
            val = 0
        return val

    def slaveTo(self, other):
        """
        Slave this Axis to other Axis.

        Before slaving this Axis, the method will ensure that this Axis is not
        current the master for any other Axis. If it is, the slaving will fail
        and this method will return false.

        In addition, if this Axis is currently slaved, it will unslave itself
        from its current master.

        Returns True if slaving was successful, False if slaving failed.
        """

        if isinstance(other, Axis):
            if len(self._masterOf) > 0:
                # This Axis is a master, so do not slave
                return False

            # Keep the previous master around in case we need to revert
            oldMaster = None
            if self._slavedTo is not None:
                oldMaster = self.unslave()

            self._slavedTo = other
            ret = other.addSlave(self)

            if ret:
                # Now that we have slaved, initialize the data range
                self.setDataRange(other._dataStart, other._dataEnd, True, other._autoscaled)
            else:
                # The other Axis did not add this axis to its _masterOf list for some reason,
                # then we need to revert what we have already done
                self._slavedTo = oldMaster
                oldMaster.addSlave(self)

            return ret

    def addSlave(self, slave):
        """
        Return True if this Axis becomes slave's master.
        """
        try:
            self._masterOf.index(slave)
        except:
            # Only add slave if it is not already in the list
            self._masterOf.append(slave)

        return True

    def unslave(self):
        """
        Make this Axis no longer a slave. The axis will revert to being autoscaled.

        Returns the object that this Axis was slaved to.
        """

        try:
            self._slavedTo._masterOf.remove(self)
        except:
            # If self is not found, we don't care since it is not in the list
            pass
        oldMaster = self._slavedTo
        self._slavedTo = None
        self.autoscale()
        return oldMaster

    def setOrientation(self, o):
        """
        Set the orientation of this Axis. Valid values are 'horizontal' and 'vertical'.
        If an invalid value is passed, then nothing happens unless the current
        orientation is None, in which case the orientation defaults to 'horizontal'.

        Once the orientation has been set, the following things are done:

        * the Axis position is updated
        * the label position is updated
        * both the major and minor ticks reset their determination of the Axis' position
        """

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

    def setInside(self, i):
        """
        Set the direction that the plot is located, in relation to this Axis.
        Valid values are 'up' and 'down'.
        If an invalid value is passed, then nothing happens unless the current
        value is None, in which case it defaults to 'up'.

        Once it has been set, the following things are done:

        * the label position is updated
        * both the major and minor ticks reset their determination of the Axis' position

        See the class documentation for an explanation of what this value means.
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

    def setPlotRange(self, anchor, start, end):
        """
        Set the axis location in plot coordinates. If start == end, then
        start is moved to start - 1. start and end are swapped if start > end.

        Once the axis location has been set, the following things are done:

        * the Axis position is updated
        * the label position is updated

        **Parameters:**

        anchor
            The position of the Axis. If the Axis is horizontal,
            then this is the y value. If the Axis is vertical,
            then this is the x value.

        start
            The starting coordinate of the Line.

        end
            The ending coordinate of the Line
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

    def setDataRange(self, start, end, fromMaster=False, autoscaled=False):
        """
        Set the data range that this Axis shows. If start == end, then
        start is moved to start - 1. start and end are swapped if start > end.

        This method does nothing if this Axis is slaved to another Axis.

        If this method is the master of other Axis's, then it will set the data
        range on those other Axis instances as well.

        **Parameters:**

        start
            The starting data coordinate.

        end
            The ending data coordinate.

        fromMaster
            boolean specifying whether this method was called from the Axis'
            master. Users should leave this set to its default.

        autoscaled
            boolean specifying whether this axis is being autoscaled (it does
            not autoscale the Axis; to do that, call Axis.autoscale()). Users
            should leave this set to its default.
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

            self._autoscaled = autoscaled
    
            for axis in self._masterOf:
                axis.setDataRange(start, end, True, autoscaled)

    def setTicksFont(self, font):
        """Helper method to set the font for both major and minor Ticks."""
        self._majorTicks.setFont(font)
        self._minorTicks.setFont(font)

    def setLabelFont(self, font):
        """
        Set the Axis label's font.

        font is any string or a Font object.
        """
        self._label.setKwargs(font=font)

    def setLabelText(self, text):
        """
        Set the Axis label's text.

        text is any string
        """
        self._label.setKwargs(text=text)

    def setLabelPosition(self):
        """
        Set the Axis label's alignment, rotation, and position.

        Currently the position is set to be halfway down the Axis, offset by 25 pixels,
        and centered there.

        This method probably never needs to be called by the user.

        Sometime in the future this method may be changed so that the user can
        specify a custom offset for a label, so that they can locate it anywhere on the plot.
        """

        # TODO maybe we should be setting the origin, not the position here, so that
        # the user can specify an offset as well and the offset is done with the position.
        # if we do that, then the setting method here would need to add the origin and the
        # current value in order to get the new origin.
        try:
            if self._orientation == 'horizontal' and self._inside == 'up':  # bottom axis
                self._label.setKwargs({'horizontalalignment': 'center',
                                   'verticalalignment': 'top',
                                   'rotation': 'horizontal',
                                  })
                self._label.setPosition(self._plotLength / 2, self._plotAnchor - 25)
            elif self._orientation == 'horizontal' and self._inside == 'down':  # top axis
                self._label.setKwargs({'horizontalalignment': 'center',
                                   'verticalalignment': 'bottom',
                                   'rotation': 'horizontal',
                                  })
                self._label.setPosition(self._plotLength / 2, self._plotAnchor + 25)
            elif self._orientation == 'vertical' and self._inside == 'up':  # left axis
                self._label.setKwargs({'horizontalalignment': 'right',
                                   'verticalalignment': 'center',
                                   'rotation': 'vertical',
                                  })
                self._label.setPosition(self._plotAnchor - 25, self._plotLength / 2)
            elif self._orientation == 'vertical' and self._inside == 'down':  # right axis
                self._label.setKwargs({'horizontalalignment': 'left',
                                   'verticalalignment': 'center',
                                   'rotation': 'vertical',
                                  })
                self._label.setPosition(self._plotAnchor + 25, self._plotLength / 2)
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


    def autoscale(self):
        """
        Autoscale the Axis' data range so that it fits all the data attached
        to the Axis.
        """

        start = None
        end = None

        datapairs = self._plot._datapairs

        # Find the minimum and maximum values attached to this Axis. It is
        # possible that Axis acts as an X axis for some data, and a y axis
        # for other data.
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

        # If there is no data, then default to a range of [0, 10]
        if start is None:
            start = 0.0
        if end is None:
            end = 10.0

        self.setDataRange(start, end, autoscaled=True)

    def setTicksLocator(self, which='major', locator=None, **kwargs):
        """
        Set the Locator instance for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'major'
            | 'minor'

        If locator is None (the default), then the kwargs are applied to the
        current Ticks' Locator.

        The kwargs are passed to the Locator instance that is used.
        """

        if which == 'minor':
            self._minorTicks.setLocator(locator, **kwargs)
        else:
            self._majorTicks.setLocator(locator, **kwargs)

    def setTicksLabeler(self, which='major', labeler=None, **kwargs):
        """
        Set the Labeler instance for the Ticks specified by which.

        which (a string specifying which ticks to apply the labeler to)
            | Can be one of:
            | 'major'
            | 'minor'

        If labeler is None (the default), then the kwargs are applied to the
        current Ticks' Labeler.

        The kwargs are passed to the Labeler instance that is used.
        """
        
        if which == 'minor':
            self._minorTicks.setLabeler(labeler, **kwargs)
        else:
            self._majorTicks.setLabeler(labeler, **kwargs)

    def setAxisPosition(self):
        """
        Position the Axis based on the plot range and the orientation.
        """
        
        if self._orientation == 'horizontal':
            self.setPosition(self._plotStart, self._plotAnchor)
            self.setEnd(self._plotEnd, self._plotAnchor)
        elif self._orientation == 'vertical':
            self.setPosition(self._plotAnchor, self._plotStart)
            self.setEnd(self._plotAnchor, self._plotEnd)

    def hideTicks(self):
        """Helper method to hide all the Ticks."""
        self._majorTicks.setVisible(False)
        self._minorTicks.setVisible(False)

    def showTicks(self):
        """Helper method to show all the Ticks."""
        self._majorTicks.setVisible(True)
        self._minorTicks.setVisible(True)

    def drawTicks(self):
        """
        Draw all the Ticks, if this Axis is visible.

        If some of the Ticks have been set to be invisible,
        then they will not be drawn.
        """
        if self.isVisible():
            # hide minor ticks behind major ticks if they overlap
            self._minorTicks.draw()
            self._majorTicks.draw()

    def draw(self, *args, **kwargs):
        """
        Draw both the Line and the Axis' label.

        Does not draw the Ticks. See Axis.drawTicks() for that.
        """
        Line.draw(self, *args, **kwargs)
        self._label.draw(*args, **kwargs)



class Ticks(object):
    """
    A Ticks class collects together all the individual Tick objects (either major
    or minor) for a given Axis. It is intended to be used as an easy way to set
    properties for all the Ticks at once.
    """

# TODO need to move the length into the individual ticks, so that it can be modified on an individual tick basis
# should do this in tickmarkargs, but need to determine if this creates a problem with their positions

    def __init__(self, backend, axis, type_='major', length=5, width=1, font=None, locator=None, labeler=None):
        """
        axis
            The Axis instance these ticks are attached to.

        type
            | The type of Axis these ticks are attached to. This is used
            | to modify the number of ticks required if they are minor ticks.
            | Can be one of:
            | 'major'
            | 'minor'

        length
            The default length for each tick.

        width
            The default width for each tick.

        font
            The default font for each tick label.

        locator
            The default Locator for the ticks.

        labeler
            The default Labeleer for the ticks.
        """

        # defaults
        self._tickMarkArgs = {
                            'width': 1,
                       }

        self._labelArgs = {'horizontalalignment': 'center',
                           'verticalalignment': 'center',
                           'font': Font()
                          }

        self._ticks = []
        self._backend = backend
        self._axis = axis
        self._type = type_
        self._length = length
        self.setWidth(width)
        self.setFont(font)
        self._locator = LinearLocator()
        self._labeler = NullLabeler()
        self.setLocator(locator)
        self.setLabeler(labeler)
        self._visible = True  # This class is not an Artist, so it doesn't have the visible keyword


    def determineAxisPosition(self):
        """
        Determine the position of the Axis these Ticks are attached to,
        and set the tick label alignments accordingly.

        This method probably never needs to be called by the user.
        """
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

    def _delTicks(self):
        """Delete the ticks list."""
        del self._ticks

    def isVisible(self):
        """Return whether these Ticks are visible."""
        return self._visible

    def setFont(self, font):
        """Set the font for the tick labels."""
        if isinstance(font, str) or isinstance(font, Font):
            self._labelArgs.update(font=font)

    def setVisible(self, v=True):
        """Set whether the Ticks are visible."""
        if isinstance(v, bool):
            self._visible = v

    def setInvisible(self):
        """Set the Ticks to be invisible."""
        self.setVisible(False)

    def setLength(self, length):
        """Set the default length for the Ticks."""
        if isinstance(length, int):
            self._length = length

    def setWidth(self, width):
        """Set the default width for the Ticks."""
        if isinstance(width, int):
            self._tickMarkArgs.update(width=width)

    def setLocator(self, locator=None, **kwargs):
        """
        Set the Locator instance for these Ticks, and updates it
        with the passed kwargs.

        If locator is not a Locator instance (i.e. it is None), the
        kwargs will be applied to the current locator.
        """

        if isinstance(locator, Locator):
            self._locator = locator
        self._locator.setKwargs(**kwargs)

    def setLabeler(self, labeler, **kwargs):
        """
        Set the Labeler instance for these Ticks, and updates it
        with the passed kwargs.

        If labeler is not a Labeler instance (i.e. it is None), the
        kwargs will be applied to the current labeler.
        """

        if isinstance(labeler, Labeler):
            self._labeler = labeler
        self._labeler.setKwargs(**kwargs)

    def makeTicks(self):
        """
        Create the individual Tick instances, but do not actually draw them.

        If these Ticks are minor ticks, then this method computes the current positions
        of the major ticks (i.e. it does not look up the current major tick locations)
        so that it can space the minor ticks according to the major tick locations.
        Because of this, Ticks.makeTicks() should be be called for both the major and
        minor ticks in close succession.

        Because Ticks.draw() calls Ticks.makeTicks(), it should not be necessary for the
        user to ever call this method.
        """

        # Get rid of the current ticks
        self.removeTicks()
        self._delTicks()
        self._ticks = []

        # Get the start and end data locations for the attached Axis
        start = self._axis._dataStart
        end = self._axis._dataEnd

        # Compute the locations of the ticks
        if self._type == 'minor':
            majorLocations = self._axis._majorTicks._locator.locations(start, end)
            locations = []
            for i in range(len(majorLocations) - 1):
                locations.extend(self._locator.locations(majorLocations[i], majorLocations[i+1], 'minor'))
        else:
            locations = self._locator.locations(start, end)

        # Compute the labels for the ticks
        labels = self._labeler.labels(locations)

        # Create the ticks
        for loc, lab in zip(locations, labels):
            self._labelArgs.update(text=str(lab))
            tick = Tick(self._backend,
                        self._axis,
                        loc,
                        self._length,
                        self._tickMarkArgs,
                        self._labelArgs)
            self._ticks.append(tick)

    def removeTicks(self):
        """
        Remove ticks from the scene, but do not delete the objects.
        """

        for tick in self._ticks:
            tick.remove()

    def draw(self):
        """
        Make the individual ticks, and then draw them.
        """

        if self.isVisible():
            self.makeTicks()
            for tick in self._ticks:
                tick.setTickPosition()
                tick.draw()

class Tick(object):
    """
    An individual tick mark, which contains both a Line and a Text label. It
    is attached to a specific axis.
    """

# TODO in conjunction with Ticks, length should be changed to a tickmarkarg if possible
# actually, i don't think this is possible, because the Line kwargs doesn't have a concept of a length

    def __init__(self, backend, axis, dataLoc, length, tickMarkArgs={}, labelArgs={}):
        """
        axis
            The Axis instance this tick is attached to.

        dataLoc
            The data coordinate that this tick will be located at.

        length
            The length of the tick mark.

        tickMarkArgs
            Keyword arguments for the tick mark Line object.

        labelArgs
            Keyword arguments for the label Text object.
        """

        self._tickMark = Line(backend, **tickMarkArgs)
        self._label = Text(backend, **labelArgs)
        self._axis = axis
        
        # Location where the tick should be placed, in data coords
        self._dataLocation = dataLoc

        self._length = length

    def setLabel(self, text=None, **kwargs):
        """
        Update the label Text object with the passed text and kwargs.

        If text is not a string, then the label's text will not be changed.

        If both text and kwargs['text'] are defined, the text argument takes precedence.
        """

        if isinstance(text, str):
            kwargs['text'] = text
        self._label.setKwargs(**kwargs)

    def setTickMarkArgs(self, **kwargs):
        """Update the tick mark Line object with the passed kwargs."""
        self._tickMark.setKwargs(**kwargs)

    def setTickPosition(self):
        """
        Set the position, in plot coordinates, of both the tick mark Line object
        and the label Text object.
        """

        # Determine various points in plot coordinates
        plotLocation = self._axis.mapDataToPlot(self._dataLocation)
        startPosition = self._axis._plotAnchor
        endPosition = startPosition

        if self._axis._inside == 'up':
            endPosition = startPosition + self._length
        elif self._axis._inside == 'down':
            endPosition = startPosition - self._length

        self._tickMark.setOrigin(self._axis._ox, self._axis._oy)
        self._label.setOrigin(self._axis._ox, self._axis._oy)

        # Actually set the positions of the tick mark and label
        if self._axis._orientation == 'horizontal':
            self._tickMark.setPosition(plotLocation, startPosition)
            self._tickMark.setEnd(plotLocation, endPosition)
            self._label.setPosition(plotLocation, startPosition)
        elif self._axis._orientation == 'vertical':
            self._tickMark.setPosition(startPosition, plotLocation)
            self._tickMark.setEnd(endPosition, plotLocation)
            self._label.setPosition(startPosition, plotLocation)

    def remove(self):
        """Remove both the tick mark and the label from the figure."""
        self._tickMark.remove()
        self._label.remove()

    def draw(self):
        """Draw both the tick mark and the label."""
        self._tickMark.draw()
        self._label.draw()


