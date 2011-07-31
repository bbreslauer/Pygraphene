

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

    def addPlot(self, plot):
        self._plots.append(plot)
        plot.setPlotRegion(0, 0, self._backend._scene.width(), self._backend._scene.height())

    def setTitle(self, title):
        if isinstance(title, Text):
            self._title = title
        elif isinstance(title, str):
            self._title.setKwargs(text=title)

    def draw(self):
        for p in self._plots:
            p.draw()

        self._title.draw()
        

    def clear(self):
        self._backend.clear()



