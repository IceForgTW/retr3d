#import Math stuff
from __future__ import division # allows floating point division from integersimport math
import math
from itertools import product

#import FreeCAD modules
import FreeCAD as App
import FreeCAD# as #
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv

class XRodTop(object):
	def __init__(self):
		pass

	def assemble(self):
		App.ActiveDocument=App.getDocument("xRodTop")
		xRodTop = App.ActiveDocument.Pad.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature','xRodTop').Shape=xRodTop
		
		#Define shifts and move into place
		xShift = -gv.xRodLength/2
		yShift =  (gv.extruderNozzleStandoff 
 				- gv.zRodStandoff
 				- gv.xEndZRodHolderFaceThickness
 				- gv.xEndZRodHolderMaxNutFaceToFace/2
				- gv.xMotorMountPlateThickness
 				- gv.xRodClampThickness
 				- gv.xRodDiaMax/2
				)
		zShift = gv.xRodSpacing
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([App.ActiveDocument.xRodTop],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()		
		
		xrt = App.ActiveDocument.xRodTop
		if xrt not in gv.xAxisParts:
			gv.xAxisParts.append(xrt)
			
	def draw(self):
		try:
			##.getDocument('xRodTop')
			##.getDocument('xRodTop').resetEdit()
			App.getDocument('xRodTop').recompute()
			App.closeDocument("xRodTop")
			App.setActiveDocument("")
			App.ActiveDocument=None
			##.ActiveDocument=None
		except:
			pass

		#make document
		App.newDocument("xRodTop")
		App.setActiveDocument("xRodTop")
		App.ActiveDocument=App.getDocument("xRodTop")
		##.ActiveDocument=#.getDocument("xRodTop")

		#make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.500000,0.500000,0.500000,0.500000))
#		#.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n  position 87 0 0 \n  orientation 0.57735026 0.57735026 0.57735026  2.0943952 \n  nearDistance -112.887\n  farDistance 287.28699\n  aspectRatio 1\n  focalDistance 87\n  height 143.52005\n\n}')
#		#.activeDocument().setEdit('Sketch')
		App.ActiveDocument.Sketch.addGeometry(Part.Circle(App.Vector(50,50,0),App.Vector(0,0,1),gv.xRodDiaTop/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,3,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius',0,gv.xRodDiaTop/2)) 
		App.ActiveDocument.recompute()
#		#.getDocument('xRodTop').resetEdit()
		App.getDocument('xRodTop').recompute()

		#Pad sketch
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		##.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.xRodLength
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()
		
		#set view as axiometric
#		#.activeDocument().activeView().viewAxometric()
		

