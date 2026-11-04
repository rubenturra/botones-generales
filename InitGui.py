# Botones generales: herramientas que valen para cualquier tecnología de corte.
# FreeCAD ejecuta este archivo con espacios de nombres separados: todo lo que
# usan los comandos se importa dentro de cada método.
import FreeCAD as App
import FreeCADGui as Gui


class _CantidadPiezas:
    def GetResources(self):
        import os, BotonesGenerales_Cantidad
        icon = os.path.join(os.path.dirname(BotonesGenerales_Cantidad.__file__), "icons", "cantidad.svg")
        return {"Pixmap": icon,
                "MenuText": "Cantidad de piezas",
                "ToolTip": "Guardar en las piezas seleccionadas cuántas hay que fabricar "
                           "(propiedad Cantidad, la usa 1st Nesting)"}

    def Activated(self):
        import BotonesGenerales_Cantidad
        BotonesGenerales_Cantidad.run()

    def IsActive(self):
        import FreeCAD
        return FreeCAD.ActiveDocument is not None


class _Ir1stNesting:
    def GetResources(self):
        import os, BotonesGenerales_Cantidad
        icon = os.path.join(os.path.dirname(BotonesGenerales_Cantidad.__file__), "icons", "ir_1st_nesting.svg")
        return {"Pixmap": icon,
                "MenuText": "Ir a 1st Nesting",
                "ToolTip": "Cambiar al banco de trabajo 1st Nesting para anidar las piezas"}

    def Activated(self):
        import FreeCADGui
        FreeCADGui.activateWorkbench("Nesting1stWorkbench")

    def IsActive(self):
        import FreeCADGui
        return "Nesting1stWorkbench" in FreeCADGui.listWorkbenches()


Gui.addCommand("BotonesGenerales_Cantidad", _CantidadPiezas())
Gui.addCommand("BotonesGenerales_Ir1stNesting", _Ir1stNesting())

try:
    from BotonesToolbar_Generales import ensure_toolbar
    for _wb in ("PartDesignWorkbench", "PartWorkbench"):
        ensure_toolbar(_wb, "Custom_BotonesGenerales", "Fabricación",
                       ["BotonesGenerales_Cantidad", "BotonesGenerales_Ir1stNesting"])
except Exception as _e:
    App.Console.PrintWarning("Botones generales: no se pudo crear la barra (%s)\n" % _e)
