

from figure import *
from plot import *
from datapair import *





def plot(*args, **kwargs):
    """
    args are x1, y1, x2, y2, etc

    kwargs are undef. as of now
    """

    figure = Figure(600, 400)
    plot = CartesianPlot(figure, figure._backend)
    figure.addPlot(plot)

    plot.setPlotRegion(0, 0, figure._backend._scene.width(), figure._backend._scene.height())

    plot._axes['right'].slaveTo(plot._axes['left'])
    plot._axes['top'].slaveTo(plot._axes['bottom'])
    
    args = list(args)
    while len(args) > 0:
        x = args.pop(0)
        y = args.pop(0)

        d = DataPair(figure._backend, x, y, plot._axes['bottom'], plot._axes['left'])
        plot.addDataPair(d)

    
    for axis in plot._axes.values():
        axis.autoscale()
        axis.setTicks(5)


    return plot



def listFonts():
    figure = Figure(600, 400)
    figure._backend.listFonts()


