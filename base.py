

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

class Parent(object):
    """
    A class that is the parent to another class.

    This is used so that clear can be called on one object and it will automatically
    remove all of its children as well.
    """

    def __init__(self):
        self._children = set()

    def children(self):
        return self._children

    def addChild(self, child):
        self._children.add(child)

    def delChild(self, child):
        try:
            self._children.remove(child)
        except KeyError:
            # Child does not exist
            pass

    def remove(self):
        """
        Remove this object. Default is to do nothing. Usually this will be implemented
        in an Artist subclass, in which case Artist should be subclassed first.
        """
        pass

    def clear(self):
        """
        Removes the current object, and then
        calls clear on all children in no specific order.
        """

        self.remove()
        for c in self.children():
            c.clear()

