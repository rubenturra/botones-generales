"""Interface helpers of Botones generales (a real module, so names resolve normally)."""
import FreeCAD as App
import FreeCADGui as Gui

WORKBENCHES = ("PartDesignWorkbench", "PartWorkbench")


def place_toolbar(title="Fabricación"):
    """Busy workbenches squeeze our toolbar behind the » overflow: move it to the
    start of its own toolbar row."""
    try:
        from PySide import QtWidgets, QtCore
        mw = Gui.getMainWindow()
        bars = [t for t in mw.findChildren(QtWidgets.QToolBar) if t.windowTitle() == title and t.isVisible()]
        if not bars:
            return
        bar = bars[0]
        if bar.width() >= bar.sizeHint().width() - 2:
            return
        mw.removeToolBar(bar)
        mw.addToolBarBreak(QtCore.Qt.TopToolBarArea)
        mw.addToolBar(QtCore.Qt.TopToolBarArea, bar)
        bar.show()
    except Exception as e:
        App.Console.PrintLog("Botones generales: barra no recolocada (%s)\n" % e)


def on_workbench(name):
    if name in WORKBENCHES:
        from PySide import QtCore
        QtCore.QTimer.singleShot(300, place_toolbar)
        QtCore.QTimer.singleShot(1500, place_toolbar)


def watch_workbenches():
    try:
        Gui.getMainWindow().workbenchActivated.connect(on_workbench)
    except Exception as e:
        App.Console.PrintWarning("Botones generales: no se pudo vigilar el banco de trabajo (%s)\n" % e)
