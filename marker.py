

from artist import Artist


class Marker(Artist):
    """
    Generic class for any type of marker that is placed on a specific
    location on a plot.

    The shape of the marker is defined by the subclass that is used.
    All markers have an edge line, a size, and a fill color.

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

    def __init__(self, canvas, **kwprops):
        Artist.__init__(self, canvas, **kwprops)

        self.setOrigin()
        self.setPosition()

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

class CircleMarker(Marker):
    """
    A circle marker.

    Radius must be an integer.
    """

    def __init__(self, canvas, radius=3, **kwprops):
        # A SyntaxError or TypeError will be received if the user tries to
        # supply the radius as an arg and a kwarg. So we don't have to worry
        # about a radius property being set in Marker.__init__.

        self.setRadius(radius)
        Marker.__init__(self, canvas, **kwprops)

    def setProps(self, props={}, **kwprops):
        """
        Remove 'radius' from props and/or kwprops. Then set the radius, and
        then set the kwprops. props takes precedence over kwprops.
        """

        radius = kwprops.pop('radius', None)
        radius = props.pop('radius', radius)
        self.setRadius(radius)

        Marker.setProps(self, props, **kwprops)

    def setRadius(self, radius):
        """
        Set radius of the circle. The radius must be an integer.
        """

        if isinstance(radius, int):
            self._radius = radius

    def _draw(self, *args, **kwargs):
        return self._canvas.drawCircle(self._x,
                                        self._y,
                                        self._radius,
                                        self._ox,
                                        self._oy,
                                        **self.props())

