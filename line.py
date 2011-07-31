

from artist import Artist


class Line(Artist):
    """

    Valid kwargs:
    width = any int
    style = solid, dash, dot, dashdot, dashdotdot
    cap = square, flat, round
    join (not supported) = bevel, miter, round
    """

    def __init__(self, backend, **kwargs):
        Artist.__init__(self, backend, **kwargs)

        self.setOrigin()
        self.setPosition()
        self.setEnd()


    def setEnd(self, x=0, y=0):
        """
        Set the ending point of the line, in plot coords.
        """
        self._ex = float(x)
        self._ey = float(y)

    def setPoints(self, sx, sy, ex, ey, ox, oy):
        """
        Convenience method to set all data points.
        """
        self.setOrigin(ox, oy)
        self.setPosition(sx, sy)
        self.setEnd(ex, ey)

    def setWidth(self, width):
        self.setKwargs(width=int(width))

    def setStyle(self, style):
        self.setKwargs(style=str(style))

    def setCap(self, cap):
        self.setKwargs(cap=str(cap))

    def setJoin(self, join):
        self.setKwargs(join=str(join))


    def _draw(self, *args, **kwargs):

        return self._backend.drawLine(  self._x,
                                        self._y,
                                        self._ex,
                                        self._ey,
                                        self._ox,
                                        self._oy,
                                        **self.kwargs())







