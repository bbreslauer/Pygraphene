

class Kwobject(object):
    """
    A standard Python object that contains a set of keywords.

    Initialize the object and then call setKwargs.
    """

    def __init__(self, args={}, **kwargs):
        self._kwargs = {}
        self.setKwargs(args, **kwargs)

    def setKwargs(self, args={}, **kwargs):
        """
        Update object's keyword arguments with kwargs.

        If args is a dictionary, then the object's keyword arguments
        will be updated with it first. If args is not a dictionary,
        it is ignored.
        """

        if isinstance(args, dict):
            self._kwargs.update(args)
        self._kwargs.update(kwargs)

    def kwargs(self, key=None):
        """
        Return object's keyword arguments as a dictionary.

        If key is None, return all the keyword arguments as a dictionary.

        If key is not None, then return the value corresponding to that
        key. If the key does not exist, then raise a KeyError.
        """

        if key is None:
            return self._kwargs
        else:
            return self._kwargs[key]

