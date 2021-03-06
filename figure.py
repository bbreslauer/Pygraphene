

from canvas.qt4pyside_canvas import Qt4PySideCanvas

from font import *
from plot import *
from text import *
from base import *

class Figure(Artist):
    """
    Represents a figure that is being drawn on a canvas. The canvas is stored
    as a canvas, which must be a subclass of BaseCanvas. The Figure can contain
    an unlimited number of Plots.

    One Plot being designated as the current Plot at any given time. This is used
    mainly for the non-OO plotter interface.
    """

    def __init__(self, width=600, height=400):
        """
        **Constructor**

        width, height
            The width and height of the figure, in pixels.
        """

        self._canvas = Qt4PySideCanvas(self, width, height)

        Artist.__init__(self, self._canvas)

        # Make the plot background white
        self.setColor('white')

        self._title = Text(self.canvas())
        self._title.setOrigin(0, 0)
        self._title.setPosition(width / 2, height - 10)
        self.setTitle('')
        self.addChild(self._title)
        self._plots = []
        self._currentPlot = None  # index of the current plot

    def canvas(self):
        return self._canvas

    def addPlot(self, plot):
        """
        Add a Plot to the Figure and set it as current.
        """
        self._plots.append(plot)
        self.addChild(plot)
        self._currentPlot = len(self._plots) - 1

    def delPlot(self, plot):
        """
        Delete the given plot from the Figure and set the current
        Plot to the first one, if one exists.
        """

        try:
            self._plots.remove(plot)
            if len(self._plots) == 0:
                self._currentPlot = None
            else:
                self._currentPlot = 0
        except:
            pass

    def getCurrentPlot(self):
        """
        Return the current plot, or None if none exists.
        """

        try:
            return self._plots[self._currentPlot]
        except TypeError, IndexError:
            # self._currentPlot is None or not in 0..len(self._plots)
            return None

    def setCurrentPlot(self, plot):
        """
        Check if plot is already attached to this Figure. If it is, then
        set it to be the current plot. If it is not, then add it to the
        Figure and set it as the current plot.
        """
        
        if isinstance(plot, Plot):
            try:
                self._currentPlot = self._plots.index(plot)
            except ValueError:
                # plot is not in self._plots
                self.addPlot(plot)

    def width(self):
        """Return the width of the Figure."""
        return self.canvas().scene().width()

    def height(self):
        """Return the height of the Figure."""
        return self.canvas().scene().height()

    def setSize(self, width, height, updateViewSize=True):
        """
        Set the width and height of the Figure, and update all children of
        the figure with their new relative positions and sizes.

        This does not redraw anything.

        Return True if the Figure's size is actually changed (i.e. if the old
        size is different from the new size), False otherwise.
        """

        oldWidth = self.width()
        oldHeight = self.height()
        
        if int(oldWidth) == int(width) and int(oldHeight) == int(height):
            return False

        self.canvas().setSceneSize(width, height)
        if updateViewSize:
            self.canvas().setViewSize(width, height)

        # Scale all children
        for child in self.children():
            try:
                child.resize(oldWidth, oldHeight, width, height)
            except:
                pass
        
        return True

    def title(self):
        return self._title

    def setTitle(self, text=None, font=None):
        """
        Set the title label.

        text can be either a str, a Text object, or a dict. If it is a str, then
        the current label's text is updated. If it is a Text object, then
        the current label is replaced with title. If it is a dict, then the
        current Text object is updated with the properties in the dict. If it is none
        of these (i.e. None) then the text is not updated.

        After that is done, if font is not None, then the title's font will
        be updated. font can be a string or Font object.
        """

        if text is not None:
            if isinstance(text, Text):
                self._title = text
            elif isinstance(text, str):
                self._title.setProps(text=text)
            elif isinstance(text, dict):
                self._title.setProps(**text)

        if font is not None:
            if isinstance(font, str) or isinstance(font, Font):
                self._title.setProps(font=font)

    def _draw(self):
        """
        Show the canvas, draw all plots, and draw the Figure title.
        """
        self.clear()
        self.canvas().show()

        # Draw the background
        self.canvas().drawRect(0, 0, self.canvas().scene().width(), self.canvas().scene().height(), 0, 0, **{'color': self.color(), 'fillcolor': self.color()})

        for p in self._plots:
            p.clear()
            p.draw()

        self._title.draw()
        
    def deleteAllPlots(self):
        """
        Remove all plots from the Figure.
        """

        for plot in self._plots:
            del plot
        self._plots = []
        self._currentPlot = None

    def save(self, filename):
        """
        Draw and save the canvas.
        """
        self.draw()
        self.canvas().save(filename)

    def clear(self):
        Parent.clear(self)
        self.canvas().update()

