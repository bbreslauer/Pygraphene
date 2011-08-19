
from base import Kwobject

class Font(Kwobject):
    """
    Encapsulate a font.

    Contains the family name, the style, the weight, and the size
    of the font.

    ======================  =================   =======
    Keyword                 Possible Values     Description
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

    defaultKwargs = {'family':  'Times',
                     'style':   'Normal',
                     'weight':  'Normal',
                     'size':    12,
                    }

    def __init__(self, family='Times', style='Normal', weight='Normal', size=12):
        defaultKwargs = {'family': family,
                         'style': style,
                         'weight': weight,
                         'size': size,
                        }

        Kwobject.__init__(self, defaultKwargs)

    def setFamily(self, family):
        """
        Set the font family to use.
        """
        self.setKwargs(family=family)

    def setStyle(self, style):
        """
        Set the font style to use.
        """
        self.setKwargs(style=style)

    def setSize(self, size):
        """
        Set the font size to use.
        """
        self.setKwargs(size=size)

    def setWeight(self, weight):
        """
        Set the font weight to use.
        """
        self.setKwargs(weight=weight)


















