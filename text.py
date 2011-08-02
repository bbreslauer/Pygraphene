

from artist import Artist


class Text(Artist):
    """
    Represent a label on a canvas.

    The font used can be either a string with the font family name in it,
    or a PyGraphene Font object.

    ======================  =================   ============    =======
    Keyword                 Possible Values     Default         Description
    ======================  =================   ============    =======
    text                    str                 ''              The text that will be displayed.
    font                    | str               'Times'         The font that will be used. Either a Font object or the name of a font family.
                            | Font
    horizontalalignment     | 'center'          'center'        Define where the horizontal anchor point is located in reference to the text.
                            | 'right'
                            | 'left'
    verticalignment         | 'center'          'center'        Define where the vertical anchor point is located in reference to the text.
                            | 'top'
                            | 'bottom'
    rotation                | 'horizontal'      'horizontal'    Define how much to rotate the text. If using an int, specifies degrees clockwise.
                            | 'vertical'
                            | int
    ======================  =================   ============    =======
    """

    def __init__(self, backend, text='', **kwargs):
        """
        If text is given as a kwarg in the initialization, it will not be used.
        """

        Artist.__init__(self, backend)

        self.setKwargs( font='Times',
                        text=text,
                        horizontalalignment='center',
                        verticalalignment='center',
                        rotation='horizontal',
                        )

        kwargs.pop('text', None)

        self.setKwargs(**kwargs)

    def setText(self, text):
        """Convenience method to set the text of this label."""
        if isinstance(text, str):
            self.setKwargs(text=text)

    def _draw(self, *args, **kwargs):
        return self._backend.drawText(  self._x,
                                        self._y,
                                        self._ox,
                                        self._oy,
                                        **self.kwargs())



