


class Font(object):
    """
    Encapsulate a font.

    Properties:
    family = any valid font family for the given backend
    style = Normal, Italic, Oblique
    size = any int
    weight = Light, Normal, Bold
    """


    def __init__(self, family='Times', style='Normal', weight='Normal', size=12):
        self.setFamily(family)
        self.setStyle(style)
        self.setWeight(weight)
        self.setSize(size)

    def setFamily(self, family):
        self._family = family

    def setStyle(self, style):
        self._style = style

    def setSize(self, size):
        self._size = size

    def setWeight(self, weight):
        self._weight = weight


















