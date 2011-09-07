

class Locator(object):
    """
    A generic class that defines the locations for ticks.

    Different Locator subclasses can have different pertinent data
    (LinearLocator needs to know the number of ticks it should
    provide, whereas StaticLocator needs to have a list of the specific
    locations for the ticks). This pertinent data can be updated either
    via the appropriate set___ method, or the generic setValues method.
    If the setValues method is used, the user must pass in keyword arguments
    for each datum to update. The accepted keyword arguments are listed
    in the individual setValues methods.
    """

    def __init__(self):
        pass

    def setValues(self, **kwargs):
        """
        Set internal values based on the keywords given. If a keyword
        does not correspond to a value for a specific subclass, then
        it is ignored.
        """
        pass

class LinearLocator(Locator):
    """
    Define tick locations by evenly spacing a certain number of ticks over the data range.
    """

    def __init__(self, num=5):
        """
        **Constructor**
        
        num
            The number of ticks that should be created.
        """

        Locator.__init__(self)

        # in case someone passes in a non-int, we will still have a default
        self._num = 5
        self.setNum(num)

    def setNum(self, num):
        """
        Set the number of ticks to create locations for.
        """
        if isinstance(num, int):
            self._num = num

    def locations(self, start, end, axisType='major'):
        """
        Return a list of data coordinates between start and end,
        evenly spaced so that there are num values.
        """

        num = self._num

        if axisType == 'minor':
            num += 2

        delta = (float(end) - float(start)) / float(num - 1)

        locs = []

        for i in range(num):
            locs.append(start)
            start += delta
        
        return locs

    def setValues(self, **kwargs):
        """
        Accepted keywords:
        
        * num

        """
        num = kwargs.pop('num', None)
        self.setNum(num)

class FixedLocator(Locator):
    """
    Define tick locations with a list of values that are passed in.
    """

    def __init__(self, locations=[], nTicks=None):
        """
        **Constructor**

        locations
            The locations that ticks should be found at. Must be a list, but
            not necessarily of numbers.
        nTicks
            How many ticks should be provided. Must be either None or an
            integer. If nTicks is None, then
            all locations will be provided. If nTicks < 2, then 2 location
            will be provided.
        """

        Locator.__init__(self)

        self._locations = []
        self.setLocations(locations)
        self.setNTicks(nTicks)

    def setLocations(self, locations):
        """
        Set the locations for the ticks. The passed locations will be
        sorted by number.
        """

        if isinstance(locations, list) or isinstance(locations, tuple):
            self._locations = locations

    def setNTicks(self, nTicks):
        """
        Set nTicks.
        """

        if nTicks is None:
            self._nTicks = None
        elif isinstance(nTicks, int):
            if nTicks < 2:
                self._nTicks = 2
            else:
                self._nTicks = nTicks

    def locations(self, start, end, axisType='major'):
        """
        Return the list of locations, subsampled if nTicks is not None.

        Disregards the start and end parameters.
        """
# TODO should subsample such that the min. value is always displayed
# TODO have not tested this with minor axes

        # Do not subsample
        if self._nTicks is None or self._nTicks >= len(self._locations):
            return self._locations

        # Subsample. Always include the two end values in the locations list
        if self._nTicks < 2:
            self._nTicks = 2
        n = self._nTicks - 1

        locs = []

        subsamplingDistance = float(len(self._locations) - 1) / float(n)

        for i in range(n):
            locs.append(self._locations[int(round(i * subsamplingDistance))])

        locs.append(self._locations[-1])

        return locs

    def setValues(self, **kwargs):
        """
        Accepted keywords:

        * locations
        * nTicks

        """

        keys = kwargs.keys()

        if 'locations' in keys:
            self.setLocations(kwargs['locations'])
        if 'nTicks' in keys:
            self.setNTicks(kwargs['nTicks'])

class SpacedLocator(Locator):
    """
    Define tick locations by spacing ticks by 'base'.
    """

    def __init__(self, base=1.0):
        """
        **Constructor**

        base
            The spacing in the data coordinates between ticks.
        """

        Locator.__init__(self)

        # in case someone passes in a non-num, we will still have a default
        self._base = 1.0
        self.setBase(base)

    def setBase(self, base):
        """
        Set the base. base must be a positive int or float.
        """
        if isinstance(base, int) or isinstance(base, float):
            if base > 0:
                self._base = base

    def locations(self, start, end, axisType='major'):
        """
        Return a list of data coordinates between start and end,
        spaced by base but always including the start and end values.
        """

        base = self._base
        locs = [start]
        loc = start

        while loc < end:
            locs.append(loc)
            loc += base

        locs.append(end)

        return locs


    def setValues(self, **kwargs):
        """
        Accepted keywords:

        * base

        """
        base = kwargs.pop('base', None)
        self.setBase(base)


# TODO it doesn't seem like labeler needs to be instantiated. maybe it does when given
# a list of values to print out, instead of using the locations given to it
class Labeler(object):
    """
    A generic class that defines the labels for ticks.
    """

    def __init__(self):
        pass
    
    def labels(self, locations):
        """
        Must return a list with exactly the same length as locations.
        """
        pass

    def setValues(self, **kwargs):
        """
        Set internal values based on the keywords given. If a keyword
        does not correspond to a value for a specific subclass, then
        it is ignored.
        """
        pass

class NullLabeler(Labeler):
    """
    No labels.
    """
    def labels(self, locations):
        return [''] * len(locations)

class StringLabeler(Labeler):
    """
    Labels that are the same as the location value.
    """
    def labels(self, locations):
        return map(str, locations)


