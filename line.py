

from artist import Artist


class Line(Artist):
    """
    Represent a line to draw on the canvas.

    The line has start and end points, and properties defining
    how the line will appear.

    ======================  =================   =======
    Property                Possible Values     Description
    ======================  =================   =======
    width                   int (1)             The width of the line.
    style                   | 'solid'           The line style.
                            | 'dash'
                            | 'dot'
                            | 'dashdot'
                            | 'dashdotdot'
    cap                     | 'square'          How the end of the line should be drawn.
                            | 'flat'
                            | 'round'
    join                    | 'bevel'           How two lines should be joined. NOT SUPPORTED.
                            | 'miter'
                            | 'round'
    ======================  =================   =======

    """

    def __init__(self, canvas, **kwprops):

        initialProperties = {'width': 1,
                         'style': 'solid',
                         'cap': 'square',
                         'join': 'bevel',
                        }
        initialProperties.update(kwprops)

        Artist.__init__(self, canvas, **initialProperties)

        self.setOrigin()
        self.setPosition()
        self.setEnd()

    def setStart(self, x=0, y=0):
        """
        Set the starting point of the line, in plot coordinates. Equivalent
        to calling setPosition.
        """
        self.setPosition(x, y)

    def setEnd(self, x=0, y=0):
        """
        Set the ending point of the line, in plot coordinates.
        """
        self._ex = float(x)
        self._ey = float(y)

    def setPoints(self, sx, sy, ex, ey, ox, oy):
        """
        Set the start, end, and origin points for this line. Start and end are
        in plot coordinates, and origin is in figure coordinates. Equivalent
        to calling setStart, setEnd, and setOrigin separately.
        """
        self.setOrigin(ox, oy)
        self.setPosition(sx, sy)
        self.setEnd(ex, ey)

    def setWidth(self, width):
        """
        Set the width of the line.
        """
        self.setProps(width=int(width))

    def setStyle(self, style):
        """
        Set the style of the line.
        """
        self.setProps(style=str(style))

    def setCap(self, cap):
        """
        Set the cap of the line.
        """
        self.setProps(cap=str(cap))

    def setJoin(self, join):
        """
        Set the join of the line.
        """
        self.setProps(join=str(join))


    def _draw(self, *args, **kwargs):

        return self._canvas.drawLine(self._x,
                                     self._y,
                                     self._ex,
                                     self._ey,
                                     self._ox,
                                     self._oy,
                                     **self.props())







