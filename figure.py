

from backends.qt4pyside_backend import Qt4PySideBackend

from plot import *
from text import *



class Figure(object):
    """
    Represents a figure that is being drawn on a canvas. The canvas is stored
    as a backend, which must be a subclass of BackendBase. The Figure can contain
    an unlimited number of Plots.

    One Plot being designated as the current Plot at any given time. This is used
    mainly for the non-OO plotter interface.
    """

    def __init__(self, width, height):
        """
        width, height
            The width and height of the figure, in pixels.
        """

        self._backend = Qt4PySideBackend(width, height)

        self._title = Text(self._backend)
        self._title.setOrigin(0, 0)
        self._title.setPosition(width / 2, height - 10)
        self.setTitle('')
        self._plots = []
        self._currentPlot = None  # index of the current plot

    def addPlot(self, plot):
        """
        Add a Plot to the Figure and set it as current.
        """
        self._plots.append(plot)
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
        return self._backend._scene.width()

    def height(self):
        """Return the height of the Figure."""
        return self._backend._scene.height()

    def setTitle(self, title):
        """
        Set the title label to title.

        title can be either a str or a Text object. If it is a str, then
        then current label's text is updated. If it is a Text object, then
        the current label is replaced with title.
        """

        if isinstance(title, Text):
            self._title = title
        elif isinstance(title, str):
            self._title.setKwargs(text=title)

    def draw(self):
        """
        Show the backend, draw all plots, and draw the Figure title.
        """

        self._backend.show()

        for p in self._plots:
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

    def clear(self):
        """
        Wipe the canvas clean.
        """
        self._backend.clear()

