
import math

from artist import Artist
from line import Line
from text import Text
from font import Font
from ticker import *
from base import Parent

class Axis(Line):
    """
    Represent an axis on a Plot.

    An Axis is attached to exactly one Plot. In addition to being a Line, the
    Axis also contains a label and major and minor Ticks.

    The Axis maintains its current location on the Plot as well as the data range
    that it represents.

    The scaling of an Axis can either be 'linear', 'log', or 'symlog'. If it is 'log'
    or 'semilog', then logBase is used to specify the log's base.

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
    cannot be both a slave and a master. This is for two reasons: 1) to simplify what
    the user needs to worry about, and 2) more importantly, to prevent infinite loops
    if Axis objects are slaved such that Axis1->Axis2->Axis1 occur.
    """

    def __init__(self, canvas, plot, orientation='horizontal', inside='up', scaling='linear', logBase=10, **kwprops):

        # Need to define the label before init'ing the Line. This is because we
        # override Line.setOrigin to include the label, but setOrigin is called
        # in Line.__init__.
        self._label = Text(canvas)

        kwprops.update(aliased=True)
        Line.__init__(self, canvas, **kwprops)

        # Make this the parent of the label, for when they need to be cleared from the screen
        self.addChild(self._label)

        self._plot = plot

        #######
        # Set default location values
        #######
        self.setOrigin(0.0, 0.0)

        # plotStart, plotEnd are start and end position, in plot coordinates. if horizontal,
        # these are x coordinates, if vertical, y coordinates.
        # plotAnchor is the opposite; if horizontal, it is the y coordinate that the axis is
        # located at.
        # plotLength = plotEnd - plotStart
        self._plotAnchor = 0.0
        self._plotStart = 0.0
        self._plotEnd = 0.0
        self._plotLength = 0.0

        # dataStart, dataEnd are the start and end position, in data coordinates.
        # dataLength = dataEnd - dataStart
        self._dataStart = 0.0
        self._dataEnd = 0.0
        self._dataLength = 0.0

        self._autoscaled = True  # holds whether this Axis is currently being autoscaled to the data

        # Setup the major and minor ticks
        self._majorTicks = Ticks(self.canvas(), self, 'major', labeler=FormatLabeler())
        self._minorTicks = Ticks(self.canvas(), self, 'minor', labeler=NullLabeler())
        self._minorTicks.setLocator(num=3)
        self._minorTicks.setLength(3)
        self._minorTicks._labelProps.update(visible=False)

        # Make this the parent of the ticks, for when they need to be cleared from the screen
        self.addChild(self._majorTicks)
        self.addChild(self._minorTicks)

        self._slavedTo = None  # pointer to this Axis' master
        self._masterOf = []    # list of pointers to this Axis' slaves

        # 'up' or 'down'
        self._inside = None
        self.setInside(inside)

        # 'horizontal' or 'vertical'
        self._orientation = None
        self.setOrientation(orientation)

        # Scaling value. Can be 'linear', 'log', or 'symlog'
        self._scaling = None
        self._logBase = 10
        self.setScaling(scaling, logBase=logBase)

    def setOrigin(self, x=0, y=0):
        """
        Set the origin, using figure coordinates.
        """
        Line.setOrigin(self, x, y)
        self.setLabelOrigin()

    def mapDataToPlot(self, value):
        """
        Convert value from data coordinates to plot coordinates. If the data range
        does not actually span any range (say, because both the start and end
        are 0), then this will always return 0.

        This method takes into account the Axis scaling.

        For a linear scaling, the algorithm performed is:

        | ds = dataStart
        | de = dataEnd
        | dl = de - ds = dataLength
        | ps = plotStart
        | pe = plotEnd
        | pl = pe - ps = plotLength
        | return = ps + pl * (value - ds) / dl

        For a logarithmic scaling, the algorithm performed is the same as for linear
        scaling, except that it is done with the logarithms of ds, de, and value.
        """

        # TODO need to take care of symlog

        if self.scaling() == 'linear':
            ds = self._dataStart
            dl = self._dataLength
        elif self.scaling() == 'log':
            try:
                ds = math.log(self._dataStart, self.logBase())
            except ValueError:
                # input is < 0, default to 1e-7
                ds = 1e-7
            try:
                de = math.log(self._dataEnd, self.logBase())
            except ValueError:
                # input is < 0, default to 1e-7
                ds = 1e-7
            dl = de - ds
            try:
                value = math.log(value, self.logBase())
            except ValueError:
                # input is < 0, default to 1e-7
                ds = 1e-7

        try:
            val = self._plotStart + self._plotLength * \
                   (float(value) - ds) / dl
        except ZeroDivisionError:
            val = 0
        return val

# THIS IS NOT USED, MAYBE WE CAN JUST GET RID OF IT
#    def mapPlotToData(self, value):
#        """
#        Convert value from plot coordinates to data coordinates. If the axis has
#        no length (probably because it has not yet been attached to a Plot),
#        then this will always return 0.
#
#        The algorithm performed is:
#
#        | ds = dataStart
#        | de = dataEnd
#        | dl = de - ds = dataLength
#        | ps = plotStart
#        | pe = plotEnd
#        | pl = pe - ps = plotLength
#
#        return = ds + dl * (value - ps) / pl
#        """
#
#        try:
#            val = self._dataStart + self._dataLength * \
#                    (float(value) - self._plotStart) / self._plotLength
#        except ZeroDivisionError:
#            val = 0
#        return val

    def slaveTo(self, other):
        """
        Slave this Axis to other Axis.

        Before slaving this Axis, the method will ensure that this Axis is not
        currently the master for any other Axis. If it is, the slaving will fail
        and this method will return false.

        In addition, if this Axis is currently slaved, it will unslave itself
        from its current master.

        Returns True if slaving was successful, False if slaving failed.
        """

        if isinstance(other, Axis):
            # This Axis is a master, so do not slave
            if len(self._masterOf) > 0:
                return False

            # other Axis is a slave, so do not slave
            if other._slavedTo is not None:
                return False

            # Keep the previous master around in case we need to revert
            oldMaster = None
            if self._slavedTo is not None:
                oldMaster = self.unslave()

            self._slavedTo = other
            ret = other.addSlave(self)

            if ret:
                # Now that we have slaved, initialize the data range and scaling
                self.setDataRange(other._dataStart, other._dataEnd, True, other._autoscaled)
                self.setScaling(other.scaling(), other.logBase(), True)
            else:
                # The other Axis did not add this axis to its _masterOf list for some reason,
                # then we need to revert what we have already done
                self._slavedTo = oldMaster
                oldMaster.addSlave(self)

            return ret
        return False

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

    def orientation(self):
        """Return the orientation of the Axis."""
        return self._orientation

    def inside(self):
        """Return the inside side of the Axis."""
        return self._inside

    def scaling(self):
        """Return the scaling type of the Axis."""
        return self._scaling

    def logBase(self):
        """Return the log base of the Axis."""
        return self._logBase

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
        elif self.orientation() != None:
            return
        else:
            self._orientation = 'horizontal'

        self.setAxisPosition()
        self.setLabelOrigin()
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
        elif self.inside() != None:
            return
        else:
            self._inside = 'up'

        self.setLabelOrigin()
        self.setLabelPosition()
        self._majorTicks.determineAxisPosition()
        self._minorTicks.determineAxisPosition()

    def setScaling(self, s, logBase=10, fromMaster=False):
        """
        Set the scaling of the Axis.
        If an invalid value is passed, then nothing happens unless the current
        value is None, in which case it defaults to 'linear'.

        **Parameters**

        s
            Valid values are 'linear', 'log', and 'symlog'.

        logBase
            float value, specifying the base if using a log scaling. Otherwise
            this value is ignored.

        fromMaster
            boolean specifying whether this method was called from the Axis'
            master. Users should leave this set to its default.
        """

        # Do not change the scaling if this axis is slaved, unless
        # we are calling it from the master
        if self._slavedTo is None or fromMaster is True:
            if s in ('linear', 'log', 'symlog'):
                self._scaling = s
                self._logBase = logBase
            elif self.scaling() != None:
                return
            else:
                self._scaling = 'linear'
                self._logBase = logBase

            for axis in self._masterOf:
                axis.setScaling(s, logBase, True)

    def setLog(self, logBase=10):
        """
        Convenient way to make this axis logarithmically scaled.

        Sets the scaling, and the major and minor ticks locators and labelers.
        """

        self.setScaling('log', logBase)
        self.setTicksLocator('major', LogLocator(logBase, [1]), True)
        self.setTicksLocator('minor', LogLocator(logBase, [1,2,3,4,5,6,7,8,9]), True)
        self.setTicksLabeler('major', FormatLabeler('%.2g'), True)
        self.setTicksLabeler('minor', NullLabeler(), True)


    def setPlotRange(self, anchor, start, end):
        """
        Set the axis location in plot coordinates. If start == end, then
        start is moved to start - 1. start and end are swapped if start > end.

        Once the axis location has been set, the following things are done:

        * the Axis position is updated
        * the label position is updated

        **Parameters**

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
        self.setLabelOrigin()
        self.setLabelPosition()

    def dataRange(self):
        """
        Return a 2-tuple of (data start, data end).
        """
        return (self._dataStart, self._dataEnd)

    def setDataRange(self, start, end, fromMaster=False, autoscaled=False):
        """
        Set the data range that this Axis shows. If start == end, then
        start is moved to start - 1. start and end are swapped if start > end.

        This method does nothing if this Axis is slaved to another Axis.

        If this method is the master of other Axis's, then it will set the data
        range on those other Axis instances as well.

        **Parameters**

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

    def setTicksFont(self, which='major', font=None, applyToSlaves=False):
        """
        Set the Font for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the Locator instance will be applied to all
        slaved Axis objects.
        """
        
        if font is None:
            return

        if which == 'both':
            self._majorTicks.setFont(font)
            self._minorTicks.setFont(font)
        elif which == 'major':
            self._majorTicks.setFont(font)
        elif which == 'minor':
            self._minorTicks.setFont(font)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksFont(which, font, False)

    def setTicksLength(self, which='major', length=None, applyToSlaves=False):
        """
        Set the length for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the length will be applied to all
        slaved Axis objects.
        """

        if length is None:
            return

        if which == 'both':
            self._majorTicks.setLength(length)
            self._minorTicks.setLength(length)
        elif which == 'major':
            self._majorTicks.setLength(length)
        elif which == 'minor':
            self._minorTicks.setLength(length)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksLength(which, length, False)

    def setTicksWidth(self, which='major', width=None, applyToSlaves=False):
        """
        Set the width for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the length will be applied to all
        slaved Axis objects.
        """

        if width is None:
            return

        if which == 'both':
            self._majorTicks.setWidth(width)
            self._minorTicks.setWidth(width)
        elif which == 'major':
            self._majorTicks.setWidth(width)
        elif which == 'minor':
            self._minorTicks.setWidth(width)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksWidth(which, width, False)

    def setTicksDirection(self, which='major', direction=None, applyToSlaves=False):
        """
        Set the direction for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the length will be applied to all
        slaved Axis objects.
        """

        if direction is None:
            return

        if which == 'both':
            self._majorTicks.setDirection(direction)
            self._minorTicks.setDirection(direction)
        elif which == 'major':
            self._majorTicks.setDirection(direction)
        elif which == 'minor':
            self._minorTicks.setDirection(direction)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksDirection(which, direction, False)

    def setTickMarkProps(self, which='major', applyToSlaves=False, **kwprops):
        """
        Set the tick mark props for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the length will be applied to all
        slaved Axis objects.
        """

        if which == 'both':
            self._majorTicks.setTickMarkProps(**kwprops)
            self._minorTicks.setTickMarkProps(**kwprops)
        elif which == 'major':
            self._majorTicks.setTickMarkProps(**kwprops)
        elif which == 'minor':
            self._minorTicks.setTickMarkProps(**kwprops)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTickMarkProps(which, False, **kwprops)

    def setTickLabelProps(self, which='major', applyToSlaves=False, **kwprops):
        """
        Set the tick label props for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If applyToSlaves is True, then the length will be applied to all
        slaved Axis objects.
        """

        if which == 'both':
            self._majorTicks.setTickLabelProps(**kwprops)
            self._minorTicks.setTickLabelProps(**kwprops)
        elif which == 'major':
            self._majorTicks.setTickLabelProps(**kwprops)
        elif which == 'minor':
            self._minorTicks.setTickLabelProps(**kwprops)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTickLabelProps(which, False, **kwprops)

    def setLabelFont(self, font):
        """
        Set the Axis label's font.

        font is any string, a Font object, or a dictionary.
        If a string, the font family is defined by the string.
        If a Font object, the object is passed directly along.
        If a dictionary, the existing Font object is updated with
        the dictionary's values.
        """
        if isinstance(font, str) or isinstance(font, Font) or isinstance(font, dict):
            self._label.setProps(font=font)

    def setLabelText(self, text):
        """
        Set the Axis label's text.

        text is any string
        """
        self._label.setProps(text=text)

    def setLabelOrigin(self):
        """
        Set the Axis label's origin.
        
        Currently the origin is set to be halfway down the Axis, offset by 25 pixels.

        This method probably never needs to be called by the user. It is called when
        the orientation, inside, or plot range are changed.
        """
        location = self.location()

        # Add the plot origin to the offset that the label needs to get to the center
        # of the axis, and make that the label's origin.
        if location == 'bottom':
            self._label.setOrigin(self._ox + self._plotLength / 2, self._oy + self._plotAnchor - 25)
        elif location == 'top':
            self._label.setOrigin(self._ox + self._plotLength / 2, self._oy + self._plotAnchor + 25)
        elif location == 'left':
            self._label.setOrigin(self._ox + self._plotAnchor - 25, self._oy + self._plotLength / 2)
        elif location == 'right':
            self._label.setOrigin(self._ox + self._plotAnchor + 25, self._oy + self._plotLength / 2)
        else:
            self._label.setOrigin(self._ox, self._oy)

    def setLabelPosition(self, x=0, y=0, props=None):
        """
        Set the Axis label's alignment, rotation, and position.

        x, y
            Positions for the label, from the label's origin.
        props
            A dictionary of Text properties. If this is not a dict,
            then the default will be to center the label and rotate
            it in the same direction as the axis is oriented.
        """
        location = self.location()

        if not isinstance(props, dict):
            if location == 'bottom':
                props = {'horizontalalignment': 'center',
                               'verticalalignment': 'top',
                               'rotation': 'horizontal',
                              }
            elif location == 'top':
                props = {'horizontalalignment': 'center',
                               'verticalalignment': 'bottom',
                               'rotation': 'horizontal',
                              }
            elif location == 'left':
                props = {'horizontalalignment': 'right',
                               'verticalalignment': 'center',
                               'rotation': 'vertical',
                              }
            elif location == 'right':
                props = {'horizontalalignment': 'left',
                               'verticalalignment': 'center',
                               'rotation': 'vertical',
                              }
            else:
                props = {'horizontalalignment': 'center',
                               'verticalalignment': 'center',
                               'rotation': 'horizontal',
                              }


        self._label.setProps(props)
        self._label.setPosition(x, y)

    def setLabelProps(self, props={}, **kwprops):
        """
        Set the Axis label's properties.
        """
        self._label.setProps(props, **kwprops)

    def location(self):
        """
        Return the location of the axis, as a string. Return values can be:
        
        * 'bottom'
        * 'top'
        * 'left'
        * 'right'
        * None

        """

        try:
            if self.orientation() == 'horizontal' and self.inside() == 'up':
                return 'bottom'
            elif self.orientation() == 'horizontal' and self.inside() == 'down':
                return 'top'
            elif self.orientation() == 'vertical' and self.inside() == 'up':
                return 'left'
            elif self.orientation() == 'vertical' and self.inside() == 'down':
                return 'right'
            else:
                return None
        except:
            return None

    def autoscaled(self):
        """
        Return True if this Axis is autoscaled, False otherwise.
        """

        return self._autoscaled

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
                    start = dp.minXValue(True)
                else:
                    start = min(start, dp.minXValue(True))
                
                if end is None:
                    end = dp.maxXValue(True)
                else:
                    end = max(end, dp.maxXValue(True))

            if dp._yaxis == self:
                if start is None:
                    start = dp.minYValue(True)
                else:
                    start = min(start, dp.minYValue(True))
                
                if end is None:
                    end = dp.maxYValue(True)
                else:
                    end = max(end, dp.maxYValue(True))

        # If there is no data, then default to a range of [0, 10]
        if start is None:
            start = 0.0
        if end is None:
            end = 10.0

        self.setDataRange(start, end, autoscaled=True)

    def setTicksLocator(self, which='major', locator=None, applyToSlaves=False, **kwprops):
        """
        Set the Locator instance for the Ticks specified by which.

        which (a string specifying which ticks to apply the locator to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If locator is None (the default), then the kwprops are applied to the
        current Ticks' Locator.

        If applyToSlaves is True, then the Locator instance will be applied to all
        slaved Axis objects.

        The kwprops are passed to the Locator instance that is used.
        """

        if which == 'both':
            self._majorTicks.setLocator(locator, **kwprops)
            self._minorTicks.setLocator(locator, **kwprops)
        elif which == 'major':
            self._majorTicks.setLocator(locator, **kwprops)
        elif which == 'minor':
            self._minorTicks.setLocator(locator, **kwprops)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksLocator(which, locator, False, **kwprops)

    def setTicksLabeler(self, which='major', labeler=None, applyToSlaves=False, **kwprops):
        """
        Set the Labeler instance for the Ticks specified by which.

        which (a string specifying which ticks to apply the labeler to)
            | Can be one of:
            | 'both'
            | 'major'
            | 'minor'

        If labeler is None (the default), then the kwprops are applied to the
        current Ticks' Labeler.

        If applyToSlaves is True, then the Locator instance will be applied to all
        slaved Axis objects.

        The kwprops are passed to the Labeler instance that is used.
        """

        if which == 'both':
            self._majorTicks.setLabeler(labeler, **kwprops)
            self._minorTicks.setLabeler(labeler, **kwprops)
        elif which == 'major':
            self._majorTicks.setLabeler(labeler, **kwprops)
        elif which == 'minor':
            self._minorTicks.setLabeler(labeler, **kwprops)

        if applyToSlaves:
            for axis in self._masterOf:
                # applyToSlaves is False because any Axis that is a slave
                # cannot be a master to other slaves.
                axis.setTicksLabeler(which, labeler, False, **kwprops)

    def setAxisPosition(self):
        """
        Position the Axis based on the plot range and the orientation.
        """
        
        if self.orientation() == 'horizontal':
            self.setPosition(self._plotStart, self._plotAnchor)
            self.setEnd(self._plotEnd, self._plotAnchor)
        elif self.orientation() == 'vertical':
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

    def ticks(self, which='major'):
        """
        Return the Ticks object corresponding to which.

        which is a string, and can be either major or minor.
        """
        if which == 'major':
            return self._majorTicks
        elif which == 'minor':
            return self._minorTicks

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



class Ticks(Parent):
    """
    A Ticks class collects together all the individual Tick objects (either major
    or minor) for a given Axis. It is intended to be used as an easy way to set
    properties for all the Ticks at once.
    """

    def __init__(self, canvas, axis, type_='major', length=5, width=1, direction='in', font=None, locator=None, labeler=None):
        """
        **Constructor**

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

        direction
            The direction of the tick relative to the axis.

        font
            The default font for each tick label.

        locator
            The default Locator for the ticks.

        labeler
            The default Labeleer for the ticks.
        """

        Parent.__init__(self)

        # defaults
        self._tickMarkProps = {
                            'width': 1,
                            'aliased': True,
                       }

        self._labelProps = {'horizontalalignment': 'center',
                           'verticalalignment': 'center',
                           'font': Font()
                          }

        self._ticks = []
        self._canvas = canvas
        self._axis = axis
        self._type = type_

        self._length = 5
        self._width = 1
        self._direction = 'in'
        self._font = Font()

        self.setLength(length)
        self.setWidth(width)
        self.setDirection(direction)
        self.setFont(font)

        self._locator = LinearLocator()
        self._labeler = NullLabeler()
        self.setLocator(locator)
        self.setLabeler(labeler)
        self._visible = True  # This class is not an Artist, so it doesn't have the visible property

    def canvas(self):
        return self._canvas

    def determineAxisPosition(self):
        """
        Determine the position of the Axis these Ticks are attached to,
        and set the tick label alignments accordingly.

        This method probably never needs to be called by the user.
        """
        
        location = self._axis.location()

        if location == 'bottom':
            self._labelProps.update({'horizontalalignment': 'center',
                               'verticalalignment': 'top',
                              })
        elif location == 'top':
            self._labelProps.update({'horizontalalignment': 'center',
                               'verticalalignment': 'bottom',
                              })
        elif location == 'left':
            self._labelProps.update({'horizontalalignment': 'right',
                               'verticalalignment': 'center',
                              })
        elif location == 'right':
            self._labelProps.update({'horizontalalignment': 'left',
                               'verticalalignment': 'center',
                              })
        else:  # undefined axis
            self._labelProps.update({'horizontalalignment': 'center',
                               'verticalalignment': 'center',
                              })
    
    def _delTicks(self):
        """Delete the ticks list."""
        for tick in self._ticks:
            self.delChild(tick)
        del self._ticks

    def isVisible(self):
        """Return whether these Ticks are visible."""
        return self._visible

    def setFont(self, font):
        """Set the font for the tick labels."""
        if isinstance(font, str) or isinstance(font, Font) or isinstance(font, dict):
            self._labelProps.update(font=font)

    def setVisible(self, v=True):
        """Set whether the Ticks are visible."""
        if isinstance(v, bool):
            self._visible = v

    def setInvisible(self):
        """Set the Ticks to be invisible."""
        self.setVisible(False)

    def setLength(self, length):
        """
        Set the default length for the Ticks. The length must be an int.
        """
        if isinstance(length, int):
            self._length = length

    def setDirection(self, direction):
        """
        Update the direction of the tick mark. The direction must be either 'in'
        or 'out', and refers to whether the tick mark should be inside or outside
        the plot. The label will always be outside.
        """
        if direction in ('in', 'out', 'both'):
            self._direction = direction

    def setWidth(self, width):
        """
        Set the default width for the Ticks. The width must be an int.
        """
        if isinstance(width, int):
            self._tickMarkProps.update(width=width)

    def setLocator(self, locator=None, **kwargs):
        """
        Set the Locator instance for these Ticks, and updates it
        with the passed kwargs.

        If locator is not a Locator instance (i.e. it is None), the
        kwargs will be applied to the current locator.
        """

        if isinstance(locator, Locator):
            self._locator = locator
        self._locator.setValues(**kwargs)

    def setLabeler(self, labeler=None, **kwargs):
        """
        Set the Labeler instance for these Ticks, and updates it
        with the passed kwargs.

        If labeler is not a Labeler instance (i.e. it is None), the
        kwargs will be applied to the current labeler.
        """

        if isinstance(labeler, Labeler):
            self._labeler = labeler
        self._labeler.setValues(**kwargs)

    def setTickMarkProps(self, **kwprops):
        """
        Update the default tick mark properties with kwprops.
        """
        self._tickMarkProps.update(kwprops)

    def setTickLabelProps(self, **kwprops):
        """
        Update the default tick label properties with kwprops.
        """
        self._labelProps.update(kwprops)

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
            # TODO another method should be devised for getting the majorLocations
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
            # Do not create a tick if it is outside of the plot range to be displayed
            if (loc < start) or (loc > end):
                continue

            self._labelProps.update(text=str(lab))
            tick = Tick(self.canvas(),
                        self._axis,
                        loc,
                        self._length,
                        self._direction,
                        self._tickMarkProps,
                        self._labelProps)
            self._ticks.append(tick)
            self.addChild(tick)

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

class Tick(Parent):
    """
    An individual tick mark, which contains both a Line and a Text label. It
    is attached to a specific axis.
    """

    def __init__(self, canvas, axis, dataLoc, length, direction, tickMarkProps={}, labelProps={}):
        """
        **Constructor**

        axis
            The Axis instance this tick is attached to.

        dataLoc
            The data coordinate that this tick will be located at.

        length
            The length of the tick mark.

        direction
            Whether the tick should be drawn to the inside or outside of the axis.
            Valid values are 'in', 'out', and 'both'. Defaults to 'in'.

        tickMarkProps
            Keyword arguments for the tick mark Line object.

        labelProps
            Keyword arguments for the label Text object.
        """

        Parent.__init__(self)

        self._tickMark = Line(canvas, **tickMarkProps)
        self._label = Text(canvas, **labelProps)
        self._axis = axis

        self.addChild(self._tickMark)
        self.addChild(self._label)
        
        # Location where the tick should be placed, in data coords
        self._dataLocation = dataLoc

        self._length = 5
        self.setLength(length)

        self._direction = 'in'
        self.setDirection(direction)

    def setLabel(self, text=None, **kwprops):
        """
        Update the label Text object with the passed text and kwprops.

        If text is not a string, then the label's text will not be changed.

        If both text and kwprops['text'] are defined, the text argument takes precedence.
        """

        if isinstance(text, str):
            kwprops['text'] = text
        self._label.setProps(**kwprops)

    def setLength(self, length):
        """
        Update the length of the tick mark. The length must be an int.
        """
        if isinstance(length, int):
            self._length = length

    def setDirection(self, direction):
        """
        Update the direction of the tick mark. The direction must be either 'in'
        or 'out', and refers to whether the tick mark should be inside or outside
        the plot. The label will always be outside.
        """
        if direction in ('in', 'out', 'both'):
            self._direction = direction

    def setTickMarkProps(self, **kwprops):
        """Update the tick mark Line object with the passed kwprops."""
        self._tickMark.setProps(**kwprops)

    def setTickPosition(self):
        """
        Set the position, in plot coordinates, of both the tick mark Line object
        and the label Text object.
        """

        # Determine various points in plot coordinates
        plotLocation = self._axis.mapDataToPlot(self._dataLocation)
        labelPosition = self._axis._plotAnchor
        startPosition = self._axis._plotAnchor
        endPosition = startPosition

        if self._axis.inside() == 'up' and self._direction == 'in':
            endPosition = startPosition + self._length
        elif self._axis.inside() == 'up' and self._direction == 'out':
            endPosition = startPosition - self._length
        elif self._axis.inside() == 'up' and self._direction == 'both':
            endPosition = startPosition - self._length
            startPosition += self._length
        elif self._axis.inside() == 'down' and self._direction == 'in':
            endPosition = startPosition - self._length
        elif self._axis.inside() == 'down' and self._direction == 'out':
            endPosition = startPosition + self._length
        elif self._axis.inside() == 'down' and self._direction == 'both':
            endPosition = startPosition + self._length
            startPosition -= self._length

        self._tickMark.setOrigin(self._axis._ox, self._axis._oy)
        self._label.setOrigin(self._axis._ox, self._axis._oy)

        # Actually set the positions of the tick mark and label
        if self._axis.orientation() == 'horizontal':
            self._tickMark.setPosition(plotLocation, startPosition)
            self._tickMark.setEnd(plotLocation, endPosition)
            self._label.setPosition(plotLocation, labelPosition)
        elif self._axis.orientation() == 'vertical':
            self._tickMark.setPosition(startPosition, plotLocation)
            self._tickMark.setEnd(endPosition, plotLocation)
            self._label.setPosition(labelPosition, plotLocation)

    def remove(self):
        """Remove both the tick mark and the label from the figure."""
        self._tickMark.remove()
        self._label.remove()

    def draw(self):
        """Draw both the tick mark and the label."""
        self._tickMark.draw()
        self._label.draw()


