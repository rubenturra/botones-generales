"""Cantidad de piezas: guarda en cada pieza seleccionada la propiedad «Cantidad».

La propiedad (entera, grupo «Fabricación») se guarda con el .FCStd. 1st Nesting
la lee al añadir la pieza y la actualiza si cambias la cantidad en su tabla.
Sirve para cualquier tecnología de corte.
"""
import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtGui

TITLE = "Cantidad de piezas"
PROPERTY = "Cantidad"
GROUP = "Fabricación"


def part_of(obj):
    """El Body que contiene al objeto seleccionado, o el propio objeto."""
    if obj.TypeId == "PartDesign::Body":
        return obj
    for parent in getattr(obj, "InListRecursive", []):
        if parent.TypeId == "PartDesign::Body":
            return parent
    return obj


def selected_parts():
    parts = []
    for obj in Gui.Selection.getSelection():
        part = part_of(obj)
        if hasattr(part, "Shape") and part not in parts:
            parts.append(part)
    return parts


def set_quantity(parts, quantity):
    doc = parts[0].Document
    doc.openTransaction(TITLE)
    try:
        for part in parts:
            if PROPERTY not in part.PropertiesList:
                part.addProperty("App::PropertyInteger", PROPERTY, GROUP,
                                 "Número de piezas a fabricar (1st Nesting)")
            setattr(part, PROPERTY, int(quantity))
    finally:
        doc.commitTransaction()


def run():
    parts = selected_parts()
    if not parts:
        QtGui.QMessageBox.information(Gui.getMainWindow(), TITLE,
                                      "Selecciona una o varias piezas en el árbol o en la vista.")
        return
    current = getattr(parts[0], PROPERTY, 1) if PROPERTY in parts[0].PropertiesList else 1
    names = ", ".join(p.Label for p in parts[:5]) + (" ..." if len(parts) > 5 else "")
    quantity, ok = QtGui.QInputDialog.getInt(Gui.getMainWindow(), TITLE,
                                             "Cantidad para: %s" % names, int(current), 1, 5000, 1)
    if ok:
        set_quantity(parts, quantity)
        App.Console.PrintMessage("Cantidad %d en: %s\n" % (quantity, ", ".join(p.Label for p in parts)))
