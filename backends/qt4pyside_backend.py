
from PySide.QtGui import *
from PySide.QtCore import Qt

from backend_base import BackendBase


class Qt4PySideBackend(BackendBase):
    """
    Abstract class representing all the methods a backend must implement.
    """

    def __init__(self, width, height):

        self._scene = QGraphicsScene(0, 0, width, height)
        self._view = QGraphicsView(self._scene)
        self._view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        
        self._view.show()

    def show(self):
        self._view.show()

    def figureToScene(self, x, y, ox=0, oy=0):
        """
        Convert from figure coords to scene coords.

        ox, oy = origin in figure coordinates
        """

        # Shift x value to the right
        x += ox

        # Shift y value up, and then invert to reach the scene
        y += oy
        y = self._scene.height() - y

        return (x, y)

    def sceneToFigure(self, x, y, ox=0, oy=0):
        """
        Convert from scene coords to figure coords.
        
        ox, oy = origin in figure coordinates
        """

        # Shift x value to the left
        x -= ox

        # Invert from scene to figure, then shift y value down
        y = self._scene.height() - y
        y -= oy

        return (x, y)


    def drawLine(self, sx, sy, ex, ey, ox=0, oy=0, **kwargs):
        """
        Draw a line from (sx, sy) to (ex, ey).
        The local origin is at (ox, oy).

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.
        """

        (sx, sy) = self.figureToScene(sx, sy, ox, oy)
        (ex, ey) = self.figureToScene(ex, ey, ox, oy)

        return self._scene.addLine(sx, sy, ex, ey, makePen(**kwargs))



    def drawRect(self, sx, sy, ex, ey, ox=0, oy=0, fill=False):
        """
        Draw a rectangle with corners (sx, sy) and (ex, ey).
        The local origin is at (ox, oy).

        """

        pass




    def drawCircle(self, cx, cy, r, ox=0, oy=0, **kwargs):
        """
        Draw a circle centered at (cx, cy) with radius r.
        The local origin is at (ox, oy).

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.
        """

        # Shift the center of the circle to the corner, which is used by QT.
        cx -= r
        cy += r

        (cx, cy) = self.figureToScene(cx, cy, ox, oy)

        fillcolor = kwargs.pop('fillcolor', '#000000')

        return self._scene.addEllipse(cx, cy, 2*r, 2*r, makePen(**kwargs), QBrush(fillcolor, Qt.SolidPattern))





    def drawText(self, x, y, ox=0, oy=0, **kwargs):
        """
        x, y are figure coords that define the top-left corner of the text item.

        kwargs that are taken care of:
        text = string
        font = Font object or str
        horizontalalignment = str
        verticalalignment = str
        rotation = 'horizontal', 'vertical' or int (for degrees)
        """
        
        t = QGraphicsTextItem(str(kwargs['text']))
        t.setFont(makeFont(kwargs['font']))
       
        # Need to rotate first so that we can set the position correctly
        # based on the height and width after rotation.
        if kwargs['rotation'] == 'horizontal':
            kwargs['rotation'] = 0
        elif kwargs['rotation'] == 'vertical':
            kwargs['rotation'] = -90
        
        t.setRotation(kwargs['rotation'])

        # The boundingRect() is in item coordinates, so it gives the same rect regardless
        # of whether the item is rotated or not. So long as the BoundingRegionGranularity
        # is 0 (the default), this is just the boundingRect transformed into the scene, 
        # which gives us the proper height and width
        boundingRect = t.boundingRegion(t.sceneTransform()).rects()[0]
        height = boundingRect.height()
        width = boundingRect.width()

        # the setPos() method used below sets the top-left corner of the item to the given
        # position. However, if the item is rotated, then the top-left corner of the item
        # is no longer the same as the top-left corner of the bounding rectangle in the scene
        # (as retrieved above). So we need to adjust x and y so that we are in effect placing
        # the top-left corner of the bounding rect, not the item. As an example, if the item
        # is rotated 45deg CCW, the top-left corner of the item is near the bottom-left
        # corner of the bounding rect.
        x += boundingRect.x()
        y += boundingRect.y()

        # take care of text location
        if kwargs['horizontalalignment'] == 'right':
            x = x - width
        elif kwargs['horizontalalignment'] == 'center':
            x = x - width / 2
        
        if kwargs['verticalalignment'] == 'bottom':
            y = y + height
        elif kwargs['verticalalignment'] == 'center':
            y = y + height / 2

        (x, y) = self.figureToScene(x, y, ox, oy)

#        if kwargs['rotation'] == 'horizontal':
#            kwargs['rotation'] = 0
#        elif kwargs['rotation'] == 'vertical':
#            kwargs['rotation'] = -90

        t.setPos(x, y)
#        t.setRotation(kwargs['rotation'])
        self._scene.addItem(t)

        return t

    def clear(self):
        self._scene.clear()

    def remove(self, item):
        """
        Remove the given item from the scene.
        """
        self._scene.removeItem(item)
        del item



    def listFonts(self):
        """
        Print out a list of the fonts that are available to use.
        """

        d = QFontDatabase()

        for font in d.families():
            print font
            for style in d.styles(font):
                print "  " + style,
                for size in d.smoothSizes(font, style):
                    print size,
                print ""







def makePen(**kwargs):
    """
    Create a QPen from the given properties. Valid properties are:

    color
    width
    """
    
    styles = {  
                'solid': Qt.SolidLine,
                'dash': Qt.DashLine,
                'dot': Qt.DotLine,
                'dashdot': Qt.DashDotLine,
                'dashdotdot': Qt.DashDotDotLine,
                }

    caps = {
            'square': Qt.SquareCap,
            'flat': Qt.FlatCap,
            'round': Qt.RoundCap,
            }

    joins = {
            'bevel': Qt.BevelJoin,
            'miter': Qt.MiterJoin,
            'round': Qt.RoundJoin,
            }

    pen = QPen()
    
    keys = kwargs.keys()
    if 'color' in keys: 
        pen.setColor(kwargs['color'])
    if 'width' in keys: 
        pen.setWidth(kwargs['width'])
    if 'style' in keys:
        pen.setStyle(styles[kwargs['style']])
    if 'cap' in keys:
        pen.setCapStyle(caps[kwargs['cap']])
    if 'join' in keys:
        pen.setJoinStyle(joins[kwargs['join']])
    
    return pen


def makeFont(font):
    """
    font is a Font object or a string
    """
    
    fontStyles = {
            'normal': QFont.StyleNormal,
            'italic': QFont.StyleItalic,
            'oblique': QFont.StyleOblique,
            }

    fontWeights = {
            'light': QFont.Light,
            'normal': QFont.Normal,
            'bold': QFont.Bold,
            }

    qf = QFont()

    if isinstance(font, str):
        qf.setFamily(font)
    else:
        qf.setFamily(str(font.kwargs('family')))
        qf.setStyle(fontStyles[str(font.kwargs('style')).lower()])
        qf.setWeight(fontWeights[str(font.kwargs('weight')).lower()])
        qf.setPointSize(int(font.kwargs('size')))

    return qf

