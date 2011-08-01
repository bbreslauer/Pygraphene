

class Kwobject(object):
    """
    A class that contains keyword arguments in a self._kwargs dict.
    """

    def __init__(self, **kwargs):
        self._kwargs = {}
        self.setKwargs(**kwargs)

    def setKwargs(self, args={}, **kwargs):
        self._kwargs.update(args)
        self._kwargs.update(kwargs)

    def kwargs(self):
        return self._kwargs

