class Color(object):
    """
    A class that defines a specific color.

    A color is specified in RGBA space, and internally stored as a 4-list of
    integers in the range 0-255. If an A value is not given, then it defaults
    to opaque.

    Colors can be specified by the user in the following manners:
    
    =================   =============
    Format              Description
    =================   =============
    (r, g, b)           Each value can be either an integer in the range 0-255, or a float in the range 0-1.
    (r, g, b, a)        Each value can be either an integer in the range 0-255, or a float in the range 0-1.
    '#rrggbb'           Each letter is a single hex value.
    '#rrggbbaa'         Each letter is a single hex value.
    name                A string representing a color name. Valid names are given below.
    Color()             A current Color object.
    =================   =============
    
    ===========     ===
    Name
    ===========     ===
    red
    green
    blue
    black
    white
    ===========     ===

    If an invalid value is given, then the color defaults to black (0, 0, 0, 255).

    """

    _namedColors = {'red': (255, 0, 0, 255),
                    'green': (0, 255, 0, 255),
                    'blue': (0, 0, 255, 255),
                    'black': (0, 0, 0, 255),
                    'white': (255, 255, 255, 255),
                   }

    def __init__(self, color=None):
        self._color = [0, 0, 0, 255]

        self.setColor(color)

    def color(self):
        """
        Return the RGBA version of the color, as a 4-list of ints.
        """
        return self.rgba()
    
    def rgb(self):
        """
        Return the RGB version of the color, as a 3-list of ints.
        """
        return self._color[0:3]

    def rgba(self):
        """
        Return the RGBA version of the color, as a 4-list of ints.
        """
        return self._color

    def setColor(self, color):
        """
        Generic method to set the color. Accepts the color in any format.

        Return True if the color is set, False otherwise.
        """

        # Check which format is being used, and call the appropriate method
        if isinstance(color, Color):
            return self.setColor(color.rgba())

        elif isinstance(color, tuple) or isinstance(color, list):
            if len(color) == 3:
                return self.setRgb(color)
            elif len(color) == 4:
                return self.setRgba(color)

        elif isinstance(color, str):
            if color[0] == '#':
                if len(color) == 7:
                    return self.setRgbHex(color)
                elif len(color) == 9:
                    return self.setRgbaHex(color)
            else:
                return self.setName(color)

        return False

    def setRgb(self, color):
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 3:
            return False

        # Check if all values are ints
        if all([isinstance(x, int) for x in color]):
            # Check if all values are between 0 and 255
            if all([(x >= 0 and x <= 255) for x in color]):
                self._color[0:3] = color
                return True

        # Check if all values are floats
        if all([isinstance(x, float) for x in color]):
            # Check if all values are between 0 and 255
            if all([(x >= 0.0 and x <= 1.0) for x in color]):
                self._color[0:3] = [int(round(x * 255.)) for x in color]
                return True

        return False
 
    def setRgba(self, color):
        if not (isinstance(color, tuple) or isinstance(color, list)) or len(color) != 4:
            return False

        # Check if all values are ints
        if all([isinstance(x, int) for x in color]):
            # Check if all values are between 0 and 255
            if all([(x >= 0 and x <= 255) for x in color]):
                self._color[0:4] = color
                return True

        # Check if all values are floats
        if all([isinstance(x, float) for x in color]):
            # Check if all values are between 0 and 255
            if all([(x >= 0.0 and x <= 1.0) for x in color]):
                self._color[0:4] = [int(round(x * 255.)) for x in color]
                return True

        return False

    def setRgbHex(self, color):
        if not isinstance(color, str) or color[0] != '#' or len(color) != 7:
            return False
        
        hexValues = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')

        if any([x not in hexValues for x in color[1:]]):
            return False

        self._color[0] = int(color[1:3], 16)
        self._color[1] = int(color[3:5], 16)
        self._color[2] = int(color[5:7], 16)

        return True

    def setRgbaHex(self, color):
        if not isinstance(color, str) or color[0] != '#' or len(color) != 9:
            return False
        
        hexValues = ('0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'a', 'b', 'c', 'd', 'e', 'f')

        if any([x not in hexValues for x in color[1:]]):
            return False

        self._color[0] = int(color[1:3], 16)
        self._color[1] = int(color[3:5], 16)
        self._color[2] = int(color[5:7], 16)
        self._color[3] = int(color[7:9], 16)

        return True

    def setName(self, color):
        if not isinstance(color, str):
            return False
        
        if color in self._namedColors.keys():
            return self.setColor(self._namedColors[color])

        return False







