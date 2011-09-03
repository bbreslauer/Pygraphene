
from base import *

class Artist(PObject, Parent):
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

    The specific canvas being used will have its own coordinates
    specifying positions of items on its canvas. To convert from
    PyGraphene coordinates to the canvas's coordinates, each canvas
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
    Property                Possible Values     Description
    ======================  =================   =======
    color                   str ('#000000')     The primary color to be used when drawing this Artist.
    visible                 bool (True)         Determine whether to draw this Artist.
    aliased                 bool (False)        Whether this Artist is antialiased (False) or aliased (True).
    ======================  =================   =======
    """


    def __init__(self, canvas, *args, **kwprops):
        """
        **Constructor**

        Initialize the origin and position. Also set the canvas for this Artist to draw with.
        """

        initialProperties = {'color': '#000000',
                             'visible': True,
                             'aliased': False,
                            }
        initialProperties.update(kwprops)

        Parent.__init__(self)
        PObject.__init__(self, initialProperties)

        self._canvas = canvas
        self._item = None

        self.setOrigin()
        self.setPosition()

    def canvas(self):
        """
        Return the canvas object.
        """
        return self._canvas

    def origin(self):
        """
        Return the origin of this artist, in figure coordinates.
        """
        return self._ox, self._oy

    def setOrigin(self, x=0, y=0):
        """
        Set the origin, using figure coordinates.
        """
        self._ox = float(x)
        self._oy = float(y)

    def position(self):
        """
        Return the position of this artist, in plot coordinates.
        """
        return self._x, self._y

    def setPosition(self, x=0, y=0):
        """
        Set the position of this artist, using plot coordinates.
        """
        self._x = float(x)
        self._y = float(y)

    def isVisible(self):
        """Return whether this Artist will be drawn."""
        return self.props('visible')

    def setVisible(self, v=True):
        """Set whether to draw this Artist."""
        if isinstance(v, bool):
            self.setProps(visible=v)

    def setInvisible(self):
        """Set whether to hide this Artist."""
        self.setVisible(False)
    
    def setColor(self, color):
        """
        Convenience method to set the primary color of this Artist.

        color is anything valid as a color property.
        """
        self.setProps(color=color)

    def color(self):
        """Return the color of this Artist."""
        return self.props('color')

    def draw(self, *args, **kwargs):
        """
        Draw this Artist if it is visible. args and kwargs may be
        used when drawing, but this is not guaranteed. Specifically,
        kwargs is not used to update the Artist's properties.

        Implementation hint: After testing whether the Artist is
        visible, this method calls _draw. If subclassing Artist,
        drawing should be done entirely in _draw(), and draw()
        should not be overridden.
        """

        self.remove()
        if self.isVisible():
            self._item = self._draw(*args, **kwargs)
            self._canvas.update()

    def _draw(self, *args, **kwargs):
        """
        Does the actual drawing of this Artist.
        Must be overwritten in the subclass.
        """
        pass

    def remove(self):
        """
        Remove this Artist from the canvas, but do not delete the Artist.
        """
        
        if self._item is not None:
            try:
                self._canvas.remove(self._item)
            except:
                # Don't worry if it cannot be deleted; it probably doesn't exist anymore
                pass

