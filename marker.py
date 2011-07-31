

from artist import Artist


class Marker(Artist):
    """

    Valid kwargs:
    color = edge color
    width = any int for the edge
    style = solid, dash, dot, dashdot, dashdotdot for the edge
    cap = square, flat, round for the edge
    join (not supported) = bevel, miter, round for the edge
    fillcolor = fill color
    """

    def __init__(self, backend, **kwargs):
        Artist.__init__(self, backend, **kwargs)

        self.setOrigin()
        self.setPosition()



    def setFillColor(self, color):
        self.setKwargs(fillcolor=int(color))

    def setWidth(self, width):
        self.setKwargs(width=int(width))

    def setStyle(self, style):
        self.setKwargs(style=str(style))

    def setCap(self, cap):
        self.setKwargs(cap=str(cap))

    def setJoin(self, join):
        self.setKwargs(join=str(join))
    

class CircleMarker(Marker):
    """
    Valid kwargs:
    radius
    """


    def __init__(self, backend, **kwargs):
        self.setRadius(3)
        Marker.__init__(self, backend, **kwargs)




    def setKwargs(self, **kwargs):
        """
        Pull radius out.
        """

        radius = kwargs.pop('radius', None)
        if radius is not None:
            self.setRadius(radius)

        Marker.setKwargs(self, **kwargs)


    def setRadius(self, radius):
        """
        Set radius of circle.
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










