

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


