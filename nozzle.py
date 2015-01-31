#import Math stuff
from __future__ import division # allows floating point division from integersimport math
import math
from itertools import product
import time

#import FreeCAD modules
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv
import utilityFunctions as uf

class Nozzle(object):
	def __init__(self):
		self.name = "nozzle"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
#		Gui.ActiveDocument.getObject(self.name).ShapeColor = (gv.frameR,gv.frameG,gv.frameB,gv.frameA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = -90
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,0,1)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.xCarriageWidth/2
		yShift = 0
		zShift = (-gv.xCarriageBushingHolderOR
				 + gv.xCarriageMountHoleVertOffset
				 - (gv.extruderMountAngleWidth-gv.extruderMountAngleThickness)/2
				 + gv.extruderMountAngleWidth
				 - gv.extruderBarrelLength
				 - gv.nozzleLength)

	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.xAxisParts:
			gv.xAxisParts.append(shape)

	def draw(self):
		try:
			Gui.getDocument(self.name)
			Gui.getDocument(self.name).resetEdit()
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
			Gui.ActiveDocument=None	
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)
		Gui.ActiveDocument=Gui.getDocument(self.name)
		
		#Revolve tip of nozzle
		#Sketch Points
		p1x = gv.nozzleDia/2
		p1y = 0
		p2x = gv.nozzleTipDia/2
		p2y = p1y
		p3x = gv.nozzleBaseDia/2
		p3y = (gv.nozzleBaseDia/2-gv.nozzleTipDia/2)
		p4x = p3x
		p4y = gv.nozzleLength
		p5x = gv.extruderBarrelLinerDia/2
		p5y = p4y
		p6x = p5x
		p6y = p3y
		p7x = gv.nozzleStepDia/2
		p7y = p6y-(p6x-p7x)/math.tan(math.pi/180*gv.nozzleDrillAngle/2)
		p8x = p7x
		p8y = gv.nozzleStepOffset+(p7x-p1x)/math.tan(math.pi/180*gv.nozzleDrillAngle/2)
		p9x = gv.nozzleDia/2
		p9y = gv.nozzleStepOffset
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(-0.707107,0.000000,0.000000,-0.707107))
		Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA\n  position 0 -87 0 \n  orientation -1 0 0  4.712389\n  nearDistance -112.88701\n  farDistance 287.28702\n  aspectRatio 1\n  focalDistance 87\n  height 143.52005\n\n}')
#		Gui.activeDocument().setEdit('Sketch')
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p7x,p7y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p7x,p7y,0),App.Vector(p8x,p8y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',5,2,6,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p8x,p8y,0),App.Vector(p9x,p9y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',6,2,7,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p9x,p9y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',7,2,8,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',8,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',8)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',6))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',9,1,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',9,2,4,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.toggleConstruction(9) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',9)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',-1,1,3,2,gv.nozzleLength)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,1,gv.nozzleDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,1,2,gv.nozzleBaseDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,5,2,gv.nozzleStepDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',8,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Angle',4,2,5,1,math.pi/180*(180-.5*gv.nozzleDrillAngle))) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Angle',6,2,7,1,math.pi/180*(180-.5*gv.nozzleDrillAngle))) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,0,2,gv.nozzleTipDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Angle',2,1,1,2,3*math.pi/4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',-1,1,3,2,gv.extruderBarrelLinerDia/2)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Revolve Sketch
		App.activeDocument().addObject("PartDesign::Revolution","Revolution")
		App.activeDocument().Revolution.Sketch = App.activeDocument().Sketch
		App.activeDocument().Revolution.ReferenceAxis = (App.activeDocument().Sketch,['V_Axis'])
		App.activeDocument().Revolution.Angle = 360.0
		App.activeDocument().Revolution.Reversed = 1
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch")
		App.ActiveDocument.Revolution.Angle = 360.000000
		App.ActiveDocument.Revolution.ReferenceAxis = (App.ActiveDocument.Sketch,['V_Axis'])
		App.ActiveDocument.Revolution.Midplane = 0
		App.ActiveDocument.Revolution.Reversed = 1
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()

		#make heater block
		#Sketch Points
		p1x = -gv.nozzleBodyDepth/2
		p1y = -gv.nozzleBodyDepth/2
		p2x = p1x
		p2y = -p1y
		p3x = gv.nozzleBodyWidth-gv.nozzleBodyDepth/2
		p3y = -p1y
		p4x = p3x
		p4y = p1y

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = (App.ActiveDocument.Revolution,["Face4"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch001')
		App.ActiveDocument.Sketch001.addExternal("Revolution","Edge7")		
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Symmetric',2,2,0,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,0,0),App.Vector(0,0,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(0,0,0),App.Vector(0,p1y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',5,2,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',5)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(5) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',5,4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(0,0,0),App.Vector(0,0,1),gv.extruderBarrelLinerDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,3,-1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,-3)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',0,gv.nozzleBodyWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',1,gv.nozzleBodyDepth)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
#		App.getDocument(self.name).recompute()
		
		#Extrude Block
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch001
		App.ActiveDocument.Pad.Reversed = 1
		App.ActiveDocument.Pad.Length = gv.nozzleBodyHeight
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch001")
		Gui.activeDocument().hide("Revolution")
#		Gui.ActiveDocument.Pad.ShapeColor=Gui.ActiveDocument.Revolution.ShapeColor
#		Gui.ActiveDocument.Pad.LineColor=Gui.ActiveDocument.Revolution.LineColor
#		Gui.ActiveDocument.Pad.PointColor=Gui.ActiveDocument.Revolution.PointColor
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Refine Shape
		App.ActiveDocument.addObject('Part::Feature','Pad').Shape=App.ActiveDocument.Pad.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad.Label
#		Gui.ActiveDocument.Pad.hide()
		Gui.ActiveDocument.Pad.Visibility = False
#		Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Pad.ShapeColor
#		Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Pad.LineColor
#		Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Pad.PointColor
		App.ActiveDocument.recompute()

		#Make Resistor Hole
		#Sketch Points
		p1x = -gv.nozzleBodyWidth+gv.nozzleBodyDepth/2
		p1y = gv.nozzleLength-gv.nozzleBodyHeight/2
		p2x = p1x + gv.nozzleResistorInset
		p2y = -p1y

		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = (App.ActiveDocument.Pad001,["Face12"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch002')
		App.ActiveDocument.Sketch002.addExternal("Pad001","Edge24")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',-3,2,-3,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.nozzleResistorDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('DistanceX',0,gv.nozzleResistorInset)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',1,gv.nozzleResistorDia/2)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut resistor hole through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch002")
		Gui.activeDocument().hide("Pad001")
#		Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Pad001.ShapeColor
#		Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Pad001.LineColor
#		Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Pad001.PointColor
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Make hole for thermistor
		#Sketch Points
		p1x = 0
		p1y = gv.nozzleLength - gv.nozzleBodyHeight
		p2x = p1x
		p2y = gv.nozzleLength - gv.nozzleBodyHeight + gv.nozzleThermistorHoleVertOffset
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = (App.ActiveDocument.Pocket,["Face10"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch003')
		App.ActiveDocument.Sketch003.addExternal("Pocket","Edge14")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,2,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-2)) 
		App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.nozzleThermistorDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('DistanceY',0,gv.nozzleThermistorHoleVertOffset)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Radius',1,gv.nozzleThermistorDia/2)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut hole
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch003")
		Gui.activeDocument().hide("Pocket")
#		Gui.ActiveDocument.Pocket001.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#		Gui.ActiveDocument.Pocket001.LineColor=Gui.ActiveDocument.Pocket.LineColor
#		Gui.ActiveDocument.Pocket001.PointColor=Gui.ActiveDocument.Pocket.PointColor
		App.ActiveDocument.Pocket001.Length = gv.nozzleThermistorDepth
		App.ActiveDocument.Pocket001.Type = 0
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()	
		
		#Make Thermistor retainer hole
		#Sketch Points
		p1x = -gv.nozzleBodyWidth/2
		p1y = gv.nozzleLength - gv.nozzleBodyHeight/2
		p2x = -gv.nozzleBodyWidth/2 + gv.nozzleThermistorRetainerHorizOffset
		p2y = gv.nozzleLength - gv.nozzleBodyHeight/2
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch004')
		App.activeDocument().Sketch004.Support = (App.ActiveDocument.Pocket001,["Face10"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch004')
		App.ActiveDocument.Sketch004.addExternal("Pocket001","Edge23")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Symmetric',-3,2,-3,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.nozzleThermistorRetainerDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Coincident',1,3,0,2)) 
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('DistanceX',0,gv.nozzleThermistorRetainerHorizOffset)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch004.addConstraint(Sketcher.Constraint('Radius',1,gv.nozzleThermistorRetainerDia/2)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut Hole
		App.activeDocument().addObject("PartDesign::Pocket","Pocket002")
		App.activeDocument().Pocket002.Sketch = App.activeDocument().Sketch004
		App.activeDocument().Pocket002.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch004")
		Gui.activeDocument().hide("Pocket001")
#		Gui.ActiveDocument.Pocket002.ShapeColor=Gui.ActiveDocument.Pocket001.ShapeColor
#		Gui.ActiveDocument.Pocket002.LineColor=Gui.ActiveDocument.Pocket001.LineColor
#		Gui.ActiveDocument.Pocket002.PointColor=Gui.ActiveDocument.Pocket001.PointColor
		App.ActiveDocument.Pocket002.Length = gv.nozzleThermistorRetainerDepth
		App.ActiveDocument.Pocket002.Type = 0
		App.ActiveDocument.Pocket002.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		#Set View
#		Gui.activeDocument().activeView().viewAxometric()
