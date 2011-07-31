


class Locator(object):


    def __init__(self, **kwargs):
        self._kwargs = {}
        self.setKwargs(**kwargs)

    def setKwargs(self, args={}, **kwargs):
        self._kwargs.update(args)
        self._kwargs.update(kwargs)

    def kwargs(self):
        return self._kwargs





class LinearLocator(Locator):

    def __init__(self, num=9, **kwargs):
        Locator.__init__(self, **kwargs)

        # in case someone passes in a non-int, we will still have a default
        self._num = 5
        self.setNum(num)



    def setNum(self, num):
        if isinstance(num, int):
            self._num = num

    def locations(self, start, end):
        """
        Return a list of data coords between start and end,
        evenly spaced so that there are num values.
        """

        num = self._num

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

    def kwargs(self):
        return self._kwargs


class LinearLabeler():
    pass













