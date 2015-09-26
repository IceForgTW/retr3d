import datetime
import os
import log as l
import sys
log = l.Logging()
from printer import Printer

sys.path.append(Printer().freecadDir)
import FreeCAD as App
import Part
import Sketcher
import Mesh

class Utilities(object):
    def __init__(self):
        self.freecadDir = Printer().freecadDir
        self.printerDir = Printer().printerDir
        self.partsDir  = Printer().partsDir
        self.stlDir = Printer().stlDir

    def saveAndClose(self, name, saveSTL):
        # Save the FCStd file
        if os.path.isfile(self.partsDir + name + ".FCStd"):
            os.remove(self.partsDir + name + ".FCStd")
        App.getDocument(name).saveAs(self.partsDir + name + ".FCStd")

        if saveSTL:

            # Export an STL
            if os.path.isfile(self.stlDir + name + ".stl"):
                os.remove(self.stlDir + name + ".stl")
            __objs__ = []
            __objs__.append(App.getDocument(name).Objects[-1])
            Mesh.export(__objs__, self.stlDir + name + ".stl")
            del __objs__

        # close document
        App.closeDocument(name)

