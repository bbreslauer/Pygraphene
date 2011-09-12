
from PySide.QtGui import *
from PySide.QtCore import Qt, QPointF

from base_canvas import BaseCanvas



class GraphicsLineItem(QGraphicsLineItem):
    """
    A QGraphicsLineItem that has a clip path.
    """

    def __init__(self, *args):
        self._clipPath = None
        QGraphicsLineItem.__init__(self, *args)

    def setClipRect(self, clipPath=None):
        self._clipPath = clipPath

    def paint(self, painter, option, widget=0):
        if self._clipPath is not None:
            painter.setClipRect(*self._clipPath)
        QGraphicsLineItem.paint(self, painter, option, widget)

class AliasedGraphicsLineItem(GraphicsLineItem):
    """
    A GraphicsLineItem that will always be drawn non-antialiased.
    """

    def __init__(self, *args):
        GraphicsLineItem.__init__(self, *args)

    def paint(self, painter, option, widget=0):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing, False)
        GraphicsLineItem.paint(self, painter, option, widget)

class GraphicsRectItem(QGraphicsRectItem):
    """
    A QGraphicsRectItem that has a clip path.
    """

    def __init__(self, *args):
        self._clipPath = None
        QGraphicsRectItem.__init__(self, *args)

    def setClipRect(self, clipPath=None):
        self._clipPath = clipPath

    def paint(self, painter, option, widget=0):
        if self._clipPath is not None:
            painter.setClipRect(*self._clipPath)
        QGraphicsRectItem.paint(self, painter, option, widget)

class AliasedGraphicsRectItem(GraphicsRectItem):
    """
    A GraphicsRectItem that will always be drawn non-antialiased.
    """

    def __init__(self, *args):
        GraphicsRectItem.__init__(self, *args)

    def paint(self, painter, option, widget=0):
        painter.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing, False)
        GraphicsRectItem.paint(self, painter, option, widget)

class GraphicsEllipseItem(QGraphicsEllipseItem):
    """
    A QGraphicsEllipseItem that has a clip path.
    """

    def __init__(self, *args):
        self._clipPath = None
        QGraphicsEllipseItem.__init__(self, *args)

    def setClipRect(self, clipPath=None):
        self._clipPath = clipPath

    def paint(self, painter, option, widget=0):
        if self._clipPath is not None:
            painter.setClipRect(*self._clipPath)
        QGraphicsEllipseItem.paint(self, painter, option, widget)

class GraphicsPolygonItem(QGraphicsPolygonItem):
    """
    A QGraphicsPolygonItem that has a clip path.
    """

    def __init__(self, *args):
        self._clipPath = None
        QGraphicsPolygonItem.__init__(self, *args)

    def setClipRect(self, clipPath=None):
        self._clipPath = clipPath

    def paint(self, painter, option, widget=0):
        if self._clipPath is not None:
            painter.setClipRect(*self._clipPath)
        QGraphicsPolygonItem.paint(self, painter, option, widget)



class Qt4PySideCanvas(BaseCanvas):
    """
    Abstract class representing all the methods a canvas must implement.
    """

    #scene and canvas are used interchangably.

    def __init__(self, width, height):


        self._scene = QGraphicsScene(0, 0, width, height)
        self._view = QGraphicsView(self._scene)
        self._view.setAlignment(Qt.AlignLeft | Qt.AlignTop)
        self._view.setRenderHints(QPainter.Antialiasing | QPainter.TextAntialiasing)
        
        self._view.show()

    def show(self):
        self._view.show()

    def widget(self):
        return self._view

    def scene(self):
        return self._scene

    def figureToCanvas(self, x, y, ox=0, oy=0):
        """
        Convert from figure coords to canvas coords.

        ox, oy = origin in figure coordinates
        """

        # Shift x value to the right
        x += ox

        # Shift y value up, and then invert to reach the canvas
        y += oy
        y = self._scene.height() - y

        return (x, y)

    def canvasToFigure(self, x, y, ox=0, oy=0):
        """
        Convert from canvas coords to figure coords.
        
        ox, oy = origin in figure coordinates
        """

        # Shift x value to the left
        x -= ox

        # Invert from canvas to figure, then shift y value down
        y = self._scene.height() - y
        y -= oy

        return (x, y)


    def drawLine(self, sx, sy, ex, ey, ox=0, oy=0, aliased=False, clipPath=None, **kwargs):
        """
        Draw a line from (sx, sy) to (ex, ey).
        The local origin is at (ox, oy).

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.

        If aliased is False, then the line is drawn with anti-aliasing turned on.
        If aliased is True, then the line is drawn without anti-aliasing.

        clipPath defines the path that the line will be clipped to. Anything outside
        the clipPath will not be drawn. clipPath can be either None, in which case
        there will be no clipping, or a 4-tuple of the form (x, y, width, height).
        x and y must be in figure coordinates.
        """

        (sx, sy) = self.figureToCanvas(sx, sy, ox, oy)
        (ex, ey) = self.figureToCanvas(ex, ey, ox, oy)

        if aliased:
            line = AliasedGraphicsLineItem(sx, sy, ex, ey)
            line.setPen(makePen(**kwargs))
        else:
            line = GraphicsLineItem(sx, sy, ex, ey)
            line.setPen(makePen(**kwargs))

        if clipPath is not None:
            line.setFlags(QGraphicsItem.ItemClipsToShape)
            line.setClipRect(clipPath)

        self._scene.addItem(line)
        return line



    def drawRect(self, sx, sy, ex, ey, ox=0, oy=0, **kwargs):
        """
        Draw a rectangle with corners (sx, sy) and (ex, ey).
        The local origin is at (ox, oy).

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.
        """

        (sx, sy) = self.figureToCanvas(sx, sy, ox, oy)
        (ex, ey) = self.figureToCanvas(ex, ey, ox, oy)

        rect = AliasedGraphicsRectItem(sx, sy, ex-sx, ey-sy)
        rect.setPen(makePen(**kwargs))
        rect.setBrush(makeBrush(**kwargs))

        self._scene.addItem(rect)
        return rect



    def drawCircle(self, cx, cy, r, ox=0, oy=0, **kwargs):
        """
        Draw a circle centered at (cx, cy) with radius r.
        The local origin is at (ox, oy).

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.
        """

        r = int(round(r))

        # Qt uses the corner of the circle, not the center.
        x = cx - r
        y = cy + r

        (x, y) = self.figureToCanvas(x, y, ox, oy)

        circle = GraphicsEllipseItem(x, y, 2*r, 2*r)
        circle.setPen(makePen(**kwargs))
        circle.setBrush(makeBrush(**kwargs))

        self._scene.addItem(circle)
        return circle



    def drawTriangle(self, cx, cy, l, orientation='up', ox=0, oy=0, **kwargs):
        """
        Draw an equilateral triangle centered at (cx, cy) and with side length l
        The local origin is at (ox, oy).
        The orientation can be 'up', 'down', 'left', 'right'.

        The origin is defined as the bottom left corner, so this will transform
        to the top-left corner to display in Qt4.
        """

        halfHeight = l * 0.866 / 2.
        halfLength = l / 2.

        (cx, cy) = self.figureToCanvas(cx, cy, ox, oy)

        triangle = QPolygonF()
        if orientation == 'up':
            triangle.append(QPointF(cx - halfLength, cy + halfHeight))
            triangle.append(QPointF(cx + halfLength, cy + halfHeight))
            triangle.append(QPointF(cx,              cy - halfHeight))
            triangle.append(QPointF(cx - halfLength, cy + halfHeight))
        elif orientation == 'down':
            triangle.append(QPointF(cx - halfLength, cy - halfHeight))
            triangle.append(QPointF(cx + halfLength, cy - halfHeight))
            triangle.append(QPointF(cx,              cy + halfHeight))
            triangle.append(QPointF(cx - halfLength, cy - halfHeight))
        elif orientation == 'right':
            triangle.append(QPointF(cx - halfHeight, cy - halfLength))
            triangle.append(QPointF(cx - halfHeight, cy + halfLength))
            triangle.append(QPointF(cx + halfHeight, cy             ))
            triangle.append(QPointF(cx - halfHeight, cy - halfLength))
        elif orientation == 'left':
            triangle.append(QPointF(cx + halfHeight, cy - halfLength))
            triangle.append(QPointF(cx + halfHeight, cy + halfLength))
            triangle.append(QPointF(cx - halfHeight, cy             ))
            triangle.append(QPointF(cx + halfHeight, cy - halfLength))

        polygon = GraphicsPolygonItem(triangle)
        polygon.setPen(makePen(**kwargs))
        polygon.setBrush(makeBrush(**kwargs))

        self._scene.addItem(polygon)
        return polygon


    def drawText(self, x, y, ox=0, oy=0, **kwargs):
        """
        x, y are figure coords that define the top-left corner of the text item.

        kwargs that are taken care of:
        text = string
        font = Font object or str
        horizontalalignment = str
        verticalalignment = str
        rotation = 'horizontal', 'vertical' or int (for degrees)

        if font provides a color, then that is the text color.
        """
        
        t = QGraphicsTextItem(str(kwargs['text']))
        t.setDefaultTextColor(kwargs['color'])
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

        (x, y) = self.figureToCanvas(x, y, ox, oy)

        t.setPos(x, y)
        self._scene.addItem(t)

        return t

    def clear(self):
        self._scene.clear()

    def update(self):
        self._scene.update()

    def remove(self, item):
        """
        Remove the given item from the canvas.
        """

        try:
            if self._scene == item.scene():
                self._scene.removeItem(item)
        except:
            "Failed to remove item: " + str(item)

    def save(self, filename):
        """
        Save the canvas to a file.
        """

        painter = QPainter()

        # How the canvas is saved depends on what kind of file is requested.
        # PDF and PS use a QPrinter, others use a QPixmap.
        if filename.split('.')[-1] in ('pdf', 'ps'):
            printer = QPrinter()
            printer.setOutputFileName(filename)
            painter.begin(printer)
            painter.setRenderHint(QPainter.Antialiasing)
            self.scene().render(painter)
            painter.end()
        else:
            pixmap = QPixmap(self.scene().width(), self.scene().height())
            painter.begin(pixmap)
            painter.setRenderHint(QPainter.Antialiasing)
            self.scene().render(painter)
            painter.end()
            pixmap.save(filename)

    def items(self, sx, sy, ex, ey, ox, oy):
        """
        Return a list of all the items on the canvas in a rectangle between
        (sx, sy) and (ex, ey).
        """
        width = ex - sx
        height = ey - sy
        (sx, ey) = self.figureToCanvas(sx, sy, ox, oy)
        (ex, sy) = self.figureToCanvas(ex, ey, ox, oy)

        return self._scene.items(sx, sy, width, height, Qt.IntersectsItemShape, Qt.AscendingOrder)

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
    style
    cap
    join
    """
    # The properties use for makePen must be distinct from makeBrush.
    
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
    pen.setCosmetic(True)
    
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

def makeBrush(**kwargs):
    """
    Create a QBrush from the given properties. Valid properties are:

    fillcolor
    fillstyle
    """
    # The properties use for makeBrush must be distinct from makePen.

    styles = {
            'none': Qt.NoBrush,
            'solid': Qt.SolidPattern,
            }
    
    brush = QBrush(Qt.SolidPattern)

    keys = kwargs.keys()
    if 'fillcolor' in keys:
        brush.setColor(kwargs['fillcolor'])
    if 'fillstyle' in keys:
        brush.setStyle(styles[kwargs['fillstyle']])

    return brush

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
        qf.setFamily(str(font.props('family')))
        qf.setStyle(fontStyles[str(font.props('style')).lower()])
        qf.setWeight(fontWeights[str(font.props('weight')).lower()])
        qf.setPointSize(int(font.props('size')))

    return qf

