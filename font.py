
from base import PObject
from color import Color

class Font(PObject):
    """
    Encapsulate a font.

    Contains the family name, the style, the weight, and the size
    of the font.

    ======================  =================   =======
    Property                Possible Values     Description
    ======================  =================   =======
    family                  str ('Times')       The font family to use. Needs to be recognized by the canvas being used.
    style                   | 'Normal'
                            | 'Italic'
                            | 'Oblique'
    size                    int (12)            The font size.
    weight                  | 'Normal'
                            | 'Bold'
                            | 'Light'
    color                   Color               The font color.
    ======================  =================   =======

    """


    def __init__(self, *args, **kwprops):
        initialProperties = {'family':  'Times',
                             'style':   'Normal',
                             'weight':  'Normal',
                             'size':    12,
                            }

        initialProperties.update(kwprops)
        PObject.__init__(self, initialProperties)

    def setFamily(self, family):
        """
        Set the font family to use.
        """
        self.setProps(family=family)

    def setStyle(self, style):
        """
        Set the font style to use.
        """
        self.setProps(style=style)

    def setSize(self, size):
        """
        Set the font size to use.
        """
        self.setProps(size=size)

    def setWeight(self, weight):
        """
        Set the font weight to use.
        """
        self.setProps(weight=weight)

    def setProps(self, props={}, **kwprops):
        """
        Remove 'color' from props and/or kwprops. Then set the color, and
        then set the kwprops. props takes precedence over kwprops.
        """

        color = kwprops.pop('color', None)
        color = props.pop('color', color)
        if not isinstance(color, Color):
            kwprops['color'] = Color(color)
        else:
            kwprops['color'] = color

        PObject.setProps(self, props, **kwprops)

