

from artist import Artist


class Marker(Artist):
    """
    Generic class for any type of marker that is placed on a specific
    location on a plot.

    The shape of the marker is defined by the subclass that is used.
    All markers have an edge line, a size, and a fill color.

    ======================  =================   =======
    Keyword                 Possible Values     Description
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

    def __init__(self, backend, **kwargs):
        Artist.__init__(self, backend, **kwargs)

        self.setOrigin()
        self.setPosition()

    def setFillColor(self, color):
        """
        Set the fill color of the marker.
        """
        self.setKwargs(fillcolor=int(color))

    def setWidth(self, width):
        """
        Set the width of the edge line.
        """
        self.setKwargs(width=int(width))

    def setStyle(self, style):
        """
        Set the style of the edge line.
        """
        self.setKwargs(style=str(style))

    def setCap(self, cap):
        """
        Set the cap of the edge line.
        """
        self.setKwargs(cap=str(cap))

class CircleMarker(Marker):
    """
    A circle marker.

    Radius must be an integer.
    """

    def __init__(self, backend, radius=3, **kwargs):
        self.setRadius(radius)
        Marker.__init__(self, backend, **kwargs)

    def setKwargs(self, args={}, **kwargs):
        """
        Remove 'radius' from args and/or kwargs. Then set the radius, and
        then set the kwargs.
        """

        radius = kwargs.pop('radius', None)
        radius = args.pop('radius', radius)
        self.setRadius(radius)

        Marker.setKwargs(self, args, **kwargs)

    def setRadius(self, radius):
        """
        Set radius of the circle. The radius must be an integer.
        """

        if isinstance(radius, int):
            self._radius = radius

    def _draw(self, *args, **kwargs):
        return self._backend.drawCircle(self._x,
                                        self._y,
                                        self._radius,
                                        self._ox,
                                        self._oy,
                                        **self.kwargs())

