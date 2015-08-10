import sys
sys.path.append('C:\\Program Files (x86)\\FreeCAD 0.15\\bin\\')
import FreeCAD
import FreeCAD as App
FreeCAD.open("C:\\Users\\Master\\Documents\\qt\\test5\\xRodTop.FCStd")
App.setActiveDocument("xRodTop")
App.ActiveDocument=App.getDocument("xRodTop")
App.ActiveDocument.Sketch.setDatum(1,App.Units.Quantity('8.000000 mm'))
App.ActiveDocument.recompute()
App.getDocument('xRodTop').recompute()
App.getDocument("xRodTop").saveAs("C:\\Users\\Master\\Documents\\qt\\test5\\xRodTop2.FCStd")