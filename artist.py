


class Artist(object):
    """
    Valid kwargs:
    color
    """


    def __init__(self, backend, *args, **kwargs):
        self._backend = backend

        self._item = None

        self.setOrigin()
        self.setPosition()

        # Properties
        self._visible = True

        self._kwargs = {}
        self.setKwargs(**kwargs)

    def item(self):
        return self._item

    def setOrigin(self, x=0, y=0):
        """
        Set the origin, in figure coords.
        """
        self._ox = float(x)
        self._oy = float(y)

    def setPosition(self, x=0, y=0):
        """
        Set the position of this artist, in plot coords.
        """
        self._x = float(x)
        self._y = float(y)

    def setVisible(self, v):
        if isinstance(v, bool):
            self._visible = v
    
    def setKwargs(self, args={}, **kwargs):
        self._kwargs.update(args)
        self._kwargs.update(kwargs)

    def kwargs(self):
        return self._kwargs

    def setColor(self, color):
        self.setKwargs(color=color)

    def draw(self, *args, **kwargs):
        """
        Determine if this should be drawn, and if so,
        then call _draw.
        """

        if self._visible:
            self._item = self._draw(*args, **kwargs)

    def _draw(self, *args, **kwargs):
        """
        Does the actual drawing.
        Must be overwritten in the subclass.
        """
        pass

    def remove(self):
        """
        Remove this artist from the scene, but do not delete the artist.
        """
        
        item = self.item()

        if item is not None:
            self._backend.remove(item)

