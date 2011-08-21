

class PObject(object):
    """
    A standard Python object that contains a set of properties.

    Properties are used by the canvas to customize how to draw an object (i.e. a line, circle, etc).
    """

    def __init__(self, props={}, **kwprops):
        """
        **Constructor**

        Initialize the object and then call setProperties.
        """
        self._properties = {}
        self.setProps(props, **kwprops)

    def setProps(self, props={}, **kwprops):
        """
        Update the object's properties.

        Updates the object's properties first with all keyword arguments
        (kwprops). Then, if props is a dictionary, the object's properties
        will be updated it. If props is not a dictionary, it is ignored. This
        allows the user to override kwprops that may be passed with default
        values.
        """

        self._properties.update(kwprops)
        if isinstance(props, dict):
            self._properties.update(props)

    def props(self, key=None):
        """
        Return object's properties as a dictionary.

        If key is None, return all the properties as a dictionary.

        If key is not None, then return the value corresponding to that
        key. If the key does not exist, then raise a KeyError.
        """

        if key is None:
            return self._properties
        else:
            return self._properties[key]

