

from artist import Artist


class Text(Artist):
    """

    Valid kwargs:
    text
    font
    horizontalalignment = 'center' | 'right' | 'left'
    verticalalignment = 'center' | 'top' | 'bottom'
    rotation = 'horizontal', 'vertical' or int (for degrees)
    """

    def __init__(self, backend, text='', **kwargs):
        Artist.__init__(self, backend)

        self.setKwargs( font='Times',
                        text=text,
                        horizontalalignment='center',
                        verticalalignment='center',
                        rotation='horizontal',
                        )

        self.setKwargs(**kwargs)

    def _draw(self, *args, **kwargs):
        return self._backend.drawText(  self._x,
                                        self._y,
                                        self._ox,
                                        self._oy,
                                        **self.kwargs())



