
from base import Kwobject

class Artist(Kwobject):
    """
    Base class for any object that draws onto a Figure.

    To draw an Artist on a Figure, it must know where to draw.
    This is done by setting an origin and a position in relation
    to that origin. The origin is defined in the Figure's global
    coordinates, and is usually set to the origin of the Artist's
    parent Plot. In this case, if the Plot is moved on the Figure,
    then the Artist just needs its origin changed, and it will still
    be presented in the same position relative to the Plot.

    **Coordinates**

    The specific backend being used will have its own coordinates
    specifying positions of items on its canvas. To convert from
    PyGraphene coordinates to the backend's coordinates, each backend
    must provide figureToScene and sceneToFigure methods.
    
    Figure coordinates start in the bottom-left corner of the canvas
    and increase up and to the right.

    Plot coordinates have the same units and directions as figure
    coordinates, but their origin can be offset from the Figure's
    origin by an arbitrary amount. This allows for Artists to set
    their position in relation to a plot, enabling vastly simplified
    moving of plots around the Figure. Plot coordinates also increase
    up and to the right.

    ======================  =================   =======
    Keyword                 Possible Values     Description
    ======================  =================   =======
    color                   str ('#000000')     The primary color to be used when drawing this Artist.
    visible                 bool (True)         Determine whether to draw this Artist.
    ======================  =================   =======
    """


    def __init__(self, backend, *args, **kwargs):
        """
        **Constructor**

        Initialize the origin and position. Also set the backend for this Artist to draw with.
        """

        initialKwargs = {'color': '#000000', 'visible': True}
        initialKwargs.update(kwargs)

        Kwobject.__init__(self, initialKwargs)

        self._backend = backend
        self._item = None

        self.setOrigin()
        self.setPosition()

    def setOrigin(self, x=0, y=0):
        """
        Set the origin, using figure coordinates.
        """
        self._ox = float(x)
        self._oy = float(y)

    def setPosition(self, x=0, y=0):
        """
        Set the position of this artist, using plot coordinates.
        """
        self._x = float(x)
        self._y = float(y)

    def isVisible(self):
        """Return whether this Artist will be drawn."""
        return self.kwargs('visible')

    def setVisible(self, v=True):
        """Set whether to draw this Artist."""
        if isinstance(v, bool):
            self.setKwargs(visible=v)

    def setInvisible(self):
        """Set whether to hide this Artist."""
        self.setVisible(False)
    
    def setColor(self, color):
        """
        Convenience method to set the primary color of this Artist.

        color is anything valid as a color keyword.
        """
        self.setKwargs(color=color)

    def draw(self, *args, **kwargs):
        """
        Draw this Artist if it is visible. args and kwargs may be
        used when drawing, but this is not guaranteed. Specifically,
        kwargs is not used to update the Artist's keyword arguments.

        Implementation hint: After testing whether the Artist is
        visible, this method calls _draw. If subclassing Artist,
        drawing should be done entirely in _draw(), and draw()
        should not be overridden.
        """

        if self.isVisible():
            self._item = self._draw(*args, **kwargs)

    def _draw(self, *args, **kwargs):
        """
        Does the actual drawing of this Artist.
        Must be overwritten in the subclass.
        """
        pass

    def remove(self):
        """
        Remove this Artist from the backend, but do not delete the Artist.
        """
        
        if self._item is not None:
            try:
                self._backend.remove(self._item)
            except:
                # Don't worry if it cannot be deleted; it probably doesn't exist anymore
                pass

