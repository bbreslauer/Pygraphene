

from artist import Artist


class Text(Artist):
    """
    Represent a label on a canvas.

    The font used can be either a string with the font family name in it,
    or a PyGraphene Font object.

    ======================  =================   =======
    Property                Possible Values     Description
    ======================  =================   =======
    text                    str ('')            The text that will be displayed.
    font                    | str ('Times')     The font that will be used. Either a Font object or the name of a font family.
                            | Font
    horizontalalignment     | 'center'          Define where the horizontal anchor point is located in reference to the text.
                            | 'right'
                            | 'left'
    verticalignment         | 'center'          Define where the vertical anchor point is located in reference to the text.
                            | 'top'
                            | 'bottom'
    rotation                | 'horizontal'      Define how much to rotate the text. If using an int, specifies degrees clockwise.
                            | 'vertical'
                            | int
    ======================  =================   =======
    """

    def __init__(self, canvas, text='', **kwprops):
        """
        If text is given as a kwprops in the initialization, it will not be used.
        """

        initialProperties = {'font': 'Times',
                             'text': text,
                             'horizontalalignment': 'center',
                             'verticalalignment': 'center',
                             'rotation': 'horizontal',
                            }
        initialProperties.update(kwprops)

        Artist.__init__(self, canvas, **initialProperties)

    def setText(self, text):
        """Convenience method to set the text of this label."""
        if isinstance(text, str):
            self.setProps(text=text)

    def _draw(self, *args, **kwargs):
        return self._canvas.drawText(  self._x,
                                        self._y,
                                        self._ox,
                                        self._oy,
                                        **self.props())

