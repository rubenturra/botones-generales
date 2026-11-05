# -*- coding: utf-8 -*-
"""Hacer todo: anidar y mecanizar plasma con la configuracion de la ultima vez.

1. Abre 1st Nesting. Piezas: las seleccionadas (si hay), si no la lista de la
   ultima vez. Chapas, espesores y ajustes: los guardados en 1st Nesting.
2. Anida (por espesores, como siempre) sin parar a mostrar el resumen.
3. Cierra la tarea de anidado, pasa a CAM y mecaniza SOLO los anidados nuevos
   con las opciones guardadas de Mecanizar plasma, sin abrir su ventana.
4. Un unico resumen final con el anidado y el mecanizado.
"""
import gc
import time

import FreeCAD as App
import FreeCADGui as Gui
from PySide import QtCore, QtWidgets

TITLE = "Hacer todo"
_state = {}


def _panel():
    for obj in gc.get_objects():
        if type(obj).__name__ == "NestingTaskPanel":
            try:
                if obj.form is not None and obj.form.isVisible():
                    return obj
            except (RuntimeError, AttributeError):
                continue
    return None


def _wait(condition, seconds):
    end = time.time() + seconds
    while time.time() < end:
        QtWidgets.QApplication.processEvents()
        if condition():
            return True
        time.sleep(0.05)
    return condition()


def _activate(doc):
    App.setActiveDocument(doc.Name)
    try:
        mdi = Gui.getMainWindow().findChild(QtWidgets.QMdiArea)
        for sub in mdi.subWindowList():
            if sub.windowTitle().split(" : ")[0] == doc.Label:
                mdi.setActiveSubWindow(sub)
                break
    except Exception:
        pass
    QtWidgets.QApplication.processEvents()


def _warn(text):
    QtWidgets.QMessageBox.warning(Gui.getMainWindow(), TITLE, text)


def _rows(panel):
    return max(0, panel.table.rowCount() - panel.control_rows)


def run():
    if _state.get("busy"):
        return
    missing = [n for n, wb in (("1st Nesting", "Nesting1stWorkbench"), ("CAM", "CAMWorkbench"))
               if wb not in Gui.listWorkbenches()]
    try:
        import BotonesPlasma_Mecanizar  # noqa: F401
    except ImportError:
        missing.append("Botones plasma")
    if missing:
        _warn("Falta instalar: %s" % ", ".join(missing))
        return
    selection = [o for o in Gui.Selection.getSelection() if hasattr(o, "Shape")]
    _state.clear()
    _state.update(busy=True, t0=time.time(), before=set(App.listDocuments()))
    try:
        # 1. 1st Nesting with its task panel
        Gui.activateWorkbench("Nesting1stWorkbench")
        if _panel() is None:
            try:
                if Gui.Control.activeDialog():
                    Gui.Control.closeDialog()
            except Exception:
                pass
            Gui.runCommand("Nesting1st_RunNesting")
        if not _wait(lambda: _panel() is not None, 10):
            raise RuntimeError("no se ha podido abrir 1st Nesting")
        panel = _panel()
        if selection:
            # The selected parts replace the list of last time.
            if _rows(panel):
                panel.table.clearSelection()
                mode = panel.table.selectionMode()
                panel.table.setSelectionMode(QtWidgets.QAbstractItemView.MultiSelection)
                for r in range(_rows(panel)):
                    panel.table.selectRow(r)
                panel.table.setSelectionMode(mode)
                panel.remove_selected_rows()
            # 1st Nesting adds the selection of the ACTIVE document: go back to
            # the design document (opening the panel activated the preview).
            source = selection[0].Document
            _activate(source)
            Gui.Selection.clearSelection()
            for o in selection:
                Gui.Selection.addSelection(o.Document.Name, o.Name)
            panel.add_selected_objects()
        else:
            _wait(lambda: _rows(panel) > 0, 3)     # the list of last time is restored
        if not _rows(panel):
            _state.clear()
            _warn("No hay piezas para anidar.\n\nSelecciona las piezas (o abre 1st Nesting y añádelas) "
                  "y vuelve a pulsar «Hacer todo».")
            return
        if not getattr(panel, "offcuts", None):
            _state.clear()
            _warn("1st Nesting no tiene chapas en el almacén. Añade las chapas y vuelve a pulsar «Hacer todo».")
            return
        # 2. nesting, keeping the summary for the end
        panel._summary_sink = []
        _state["panel"] = panel
        panel.execute_nesting()
        QtCore.QTimer.singleShot(300, _after_nesting)
    except Exception as e:
        _state.clear()
        _warn("No se ha podido completar: %s" % e)


def _after_nesting():
    panel = _state.get("panel")
    try:
        busy = panel is not None and panel.nesting_busy()
    except RuntimeError:
        busy = False
    if busy:
        QtCore.QTimer.singleShot(300, _after_nesting)
        return
    try:
        summary = list(getattr(panel, "_summary_sink", None) or [])
        try:
            panel._summary_sink = None
        except Exception:
            pass
        new_docs = [App.getDocument(n) for n in App.listDocuments()
                    if n not in _state["before"] and n.startswith("Nesting_Result")]
        nest_secs = time.time() - _state["t0"]
        intro = "ANIDADO (%.0f s)\n%s" % (nest_secs, "\n".join(summary) if summary else
                                          "\n".join("  " + d.Label for d in new_docs))
        if not new_docs:
            _warn("El anidado no ha creado ningún resultado (¿se ha cancelado?). No se mecaniza nada.")
            return
        # 3. close the nesting task, go to CAM and machine the new results
        try:
            import Nesting1stGui
            Nesting1stGui.close_nesting_panel()
        except Exception:
            pass
        Gui.activateWorkbench("CAMWorkbench")
        import BotonesPlasma_Mecanizar as M
        M.activate_doc(new_docs[0])
        M.main(auto_docs=new_docs, intro=intro + "\n\nMECANIZADO PLASMA")
    except Exception as e:
        _warn("No se ha podido completar: %s" % e)
    finally:
        _state.clear()
