
from base import PObject

class Font(PObject):
    """
    Encapsulate a font.

    Contains the family name, the style, the weight, and the size
    of the font.

    ======================  =================   =======
    Property                Possible Values     Description
    ======================  =================   =======
    family                  str ('Times')       The font family to use. Needs to be recognized by the backend being used.
    style                   | 'Normal'          Italicize font.
                            | 'Italic'
                            | 'Oblique'
    size                    int (12)            The font size.
    weight                  | 'Normal'          Boldness.
                            | 'Bold'
                            | 'Light'
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

