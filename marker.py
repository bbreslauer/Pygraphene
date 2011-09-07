

from artist import Artist


class Marker(Artist):
    """
    Generic class for any type of marker that is placed on a specific
    location on a plot.

    The shape of the marker is defined by the subclass that is used.
    All markers have an edge line, a size, and a fill color.

    The size of the Marker should be an integer. This is a generalized
    diameter-type size, in pixels.

    ======================  =================   =======
    Property                Possible Values     Description
    ======================  =================   =======
    color                   str ('#000000')     The color of the edge line.
    fillcolor               str ('#000000')     The color of the center of the marker.
    width                   int (1)             The width of the edge line.
    style                   | 'solid'           The edge line style.
                            | 'dash'
                            | 'dot'
                            | 'dashdot'
                            | 'dashdotdot'
    cap                     | 'square'          How the end of the edge line should be drawn.
                            | 'flat'
                            | 'round'
    ======================  =================   =======

    """

    def __init__(self, canvas, size=5, **kwprops):
        # A SyntaxError or TypeError will be received if the user tries to
        # supply the size as an arg AND a kwarg. So we don't have to worry
        # about a size property being set in Marker.__init__.

        Artist.__init__(self, canvas, **kwprops)

        self.setOrigin()
        self.setPosition()
        self.setSize(size)

    def setSize(self, size):
        """
        Set the size of the marker.
        """
        self._size = size

    def setFillColor(self, color):
        """
        Set the fill color of the marker.
        """
        self.setProps(fillcolor=int(color))

    def setWidth(self, width):
        """
        Set the width of the edge line.
        """
        self.setProps(width=int(width))

    def setStyle(self, style):
        """
        Set the style of the edge line.
        """
        self.setProps(style=str(style))

    def setCap(self, cap):
        """
        Set the cap of the edge line.
        """
        self.setProps(cap=str(cap))

    def setProps(self, props={}, **kwprops):
        """
        Remove 'size' from props and/or kwprops. Then set the size, and
        then set the kwprops. props takes precedence over kwprops.
        """

        size = kwprops.pop('size', None)
        size = props.pop('size', size)
        self.setSize(size)

        Artist.setProps(self, props, **kwprops)

class CircleMarker(Marker):
    """
    A circle marker.
    """

    def __init__(self, canvas, size=6, **kwprops):
        Marker.__init__(self, canvas, size, **kwprops)

    def _draw(self, *args, **kwargs):
        return self._canvas.drawCircle(self._x,
                                       self._y,
                                       self._size / 2,
                                       self._ox,
                                       self._oy,
                                       **self.props())

class SquareMarker(Marker):
    """
    A square marker.
    """

    def __init__(self, canvas, size=5, **kwprops):
        Marker.__init__(self, canvas, size, **kwprops)

    def _draw(self, *args, **kwargs):
        # These seem to be the appropriate offsets required
        sx = self._x - (self._size / 2) - 2
        sy = self._y - (self._size / 2)
        ex = self._x + (self._size / 2) - 1
        ey = self._y + (self._size / 2) + 1

        return self._canvas.drawRect(sx,
                                     sy,
                                     ex,
                                     ey,
                                     self._ox,
                                     self._oy,
                                     **self.props())







