
from base import Kwobject

class Locator(Kwobject):
    """
    A generic class that defines the locations for ticks.
    """

    def __init__(self, **kwargs):
        Kwobject.__init__(self, **kwargs)

class LinearLocator(Locator):
    """
    Define tick locations by evenly spacing a certain number of ticks over the data range.
    """

    def __init__(self, num=5, **kwargs):
        """
        **Constructor**
        
        num
            The number of ticks that should be created.
        """

        Locator.__init__(self, **kwargs)

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

    def setKwargs(self, args={}, **kwargs):
        num = kwargs.pop('num', None)
        num = args.pop('num', num)
        self.setNum(num)

        Locator.setKwargs(self, args, **kwargs)


class Labeler(Kwobject):
    """
    A generic class that defines the labels for ticks.
    """

    def __init__(self, **kwargs):
        Kwobject.__init__(self, **kwargs)
    
    def labels(self, locations):
        """
        Must return a list with exactly the same length as locations.
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


