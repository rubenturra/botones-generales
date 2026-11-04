# Botones generales: herramientas que valen para cualquier tecnología de corte.
import os
import FreeCAD as App
import FreeCADGui as Gui

_DIR = os.path.dirname(os.path.abspath(__file__)) if "__file__" in dir() else os.path.join(
    App.getUserAppDataDir(), "Mod", "botones-generales")


class _CantidadPiezas:
    def GetResources(self):
        return {"Pixmap": os.path.join(_DIR, "icons", "cantidad.svg"),
                "MenuText": "Cantidad de piezas",
                "ToolTip": "Guardar en las piezas seleccionadas cuántas hay que fabricar "
                           "(propiedad Cantidad, la usa 1st Nesting)"}

    def Activated(self):
        import BotonesGenerales_Cantidad
        BotonesGenerales_Cantidad.run()

    def IsActive(self):
        return App.ActiveDocument is not None


Gui.addCommand("BotonesGenerales_Cantidad", _CantidadPiezas())

try:
    from BotonesToolbar_Generales import ensure_toolbar
    for _wb in ("PartDesignWorkbench", "PartWorkbench"):
        ensure_toolbar(_wb, "Custom_BotonesGenerales", "Fabricación", ["BotonesGenerales_Cantidad"])
except Exception as _e:
    App.Console.PrintWarning("Botones generales: no se pudo crear la barra (%s)\n" % _e)
