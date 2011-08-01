

from backends.qt4pyside_backend import Qt4PySideBackend

from plot import *
from text import *



class Figure(object):

    def __init__(self, width, height):
        self._backend = Qt4PySideBackend(width, height)

        self._title = Text(self._backend)
        self._title.setOrigin(0, 0)
        self._title.setPosition(width / 2, height - 10)
        self.setTitle('')
        self._plots = []
        self._currentPlot = None  # index of the current plot

    def addPlot(self, plot):
        self._plots.append(plot)
        self._currentPlot = len(self._plots) - 1


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
        Check if fig already exists. If it does, then set it as active. If not,
        then add it to the figures and set it as active.
        """
        
        if isinstance(plot, Plot):
            try:
                self._currentPlot = self._plots.index(plot)
            except ValueError:
                # plot is not in self._plots
                self.addPlot(plot)

    def width(self):
        return self._backend._scene.width()

    def height(self):
        return self._backend._scene.height()

    def setTitle(self, title):
        if isinstance(title, Text):
            self._title = title
        elif isinstance(title, str):
            self._title.setKwargs(text=title)

    def draw(self):
        self._backend.show()

        for p in self._plots:
            p.draw()

        self._title.draw()
        
    def deleteAllPlots(self):
        for plot in self._plots:
            del plot
        self._plots = []
        self._currentPlot = None

    def clear(self):
        self._backend.clear()



