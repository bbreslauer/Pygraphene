

from figure import *
from plot import *
from datapair import *

class FigureManager(object):
    """
    A class that contains all the figures that have been created using the plotter
    interface. It also keeps track of the active figure.
    """

    _figures = []   # list of all figures that have been created
    _active = None  # index of the active figure

    @staticmethod
    def getActive():
        """
        Return the active Figure object, or None if none exists.
        """

        try:
            return FigureManager._figures[FigureManager._active]
        except TypeError, IndexError:
            # _active is None or not in 0..len(_figures)
            return None

    @staticmethod
    def setActive(fig):
        """
        Check if fig already exists. If it does, then set it as active. If not,
        then add it to the figures and set it as active.
        """

        if isinstance(fig, Figure):
            try:
                FigureManager._active = FigureManager._figures.index(fig)
            except ValueError:
                # fig is not in _figures
                FigureManager._figures.append(fig)
                FigureManager._active = len(FigureManager._figures) - 1


def figure(width=600, height=400):
    """
    Create a figure.
    """

    fig = Figure(width, height)
    FigureManager.setActive(fig)
    return fig

def plot(*args, **kwargs):
    """
    args are x1, y1, x2, y2, etc

    Valid kwargs are:

    new
        Boolean specifying whether a new plot should be created on the current figure.
        Defaults to False.
    position
        A 3-tuple specifying the location of this plot, of the form (numRows, numCols, numPlot).

    Uses the current figure, if one exists, otherwise creates a new figure.
    If the current figure has a current plot, then uses it, otherwise creates a
    plot in position 1, 1, 1.

    Running plot() multiple times will add more data to the last defined plot.
    Running show() multiple times will show the last defined plot.
    """
    
    newPlot = False
    if 'new' in kwargs.keys():
        newPlot = True

    fig = FigureManager.getActive()
    if fig is None:
        figure()
        fig = FigureManager.getActive()
    plot = fig.getCurrentPlot()
    if plot is None or newPlot is True:
        plot = CartesianPlot(fig, fig._canvas)
        fig.addPlot(plot)
        position = [1, 1, 1]
        if 'position' in kwargs.keys():
            position = kwargs['position']
        plot.setPlotLocation(*position)

    args = list(args)
    while len(args) > 0:
        x = args.pop(0)
        y = args.pop(0)
        if len(args) > 0 and isinstance(args[0], str):
            fs = args.pop(0)
        else:
            fs = ''

        d = DataPair(fig._canvas, x, y, fs)
        plot.addDataPair(d)

    return plot

def clearFigure():
    """
    Clear the active figure and remove all plots from it.
    """

    fig = FigureManager.getActive()
    if fig is not None:
        fig.clear()
        fig.deleteAllPlots()

def show():
    """
    Redraw the current figure and display it.
    """

    fig = FigureManager.getActive()
    if fig is not None:
        fig.draw()
        _show_Qt()

def listFonts():
    """
    List all the available fonts for the canvas that is currently
    in use.
    """

    figure = Figure(600, 400)
    figure._canvas.listFonts()




# import necessary modules
import sys
from PySide.QtCore import *
from PySide.QtGui import *


def _start_Qt():
    try:
        QApplication(sys.argv)
    except RuntimeError:
        pass

def _show_Qt():
    qApp.exec_()

app = QApplication(sys.argv)

