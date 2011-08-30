

from artist import Artist
from font import Font


class Text(Artist):
    """
    Represent a label on a canvas.

    The font used can be either a string with the font family name in it,
    or a PyGraphene Font object.

    The Text object contains a color property from Artist, and if font is
    a Font object, then it also contains a color property. The order of
    priority for determining what color the text will be is:

    1. if font is a Font, then use font's color
    2. else, use the Text color

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
        props = self.props()
        if isinstance(self.props('font'), Font):
            try:
                props.update(color=self.props('font').props('color'))
            except:
                pass

        return self._canvas.drawText(  self._x,
                                        self._y,
                                        self._ox,
                                        self._oy,
                                        **props)

