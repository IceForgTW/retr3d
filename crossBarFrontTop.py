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
import utilityFunctions as uf

class CrossBarFrontTop(object):
	def __init__(self):
		self.name = "crossBarFrontTop"
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		#.ActiveDocument=#.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
		#.ActiveDocument.getObject(self.name).ShapeColor = (gv.frameR,gv.frameG,gv.frameB,gv.frameA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
# 		#Rotate into correct orientation
# 		rotateAngle = 0
# 		rotateCenter = App.Vector(0,0,0)
# 		rotateAxis = App.Vector(1,0,0)
# 		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		xShift = -gv.crossBarLength/2
		yShift = -gv.yRodLength/2 + gv.frameWidth/2
		zShift = -gv.yRodStandoff - gv.frameHeight/2
		
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()


	def draw(self):
		try:
			#.getDocument(self.name)
			#.getDocument(self.name).resetEdit()
			App.getDocument(self.name).recompute()
			App.closeDocument(self.name)
			App.setActiveDocument("")
			App.ActiveDocument=None
			#.ActiveDocument=None	
		except:
			pass

		#make document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)
		#.ActiveDocument=#.getDocument(self.name)
		
		#extrude crossBarTop
		uf.extrudeFrameMember(self.name, gv.crossBarLength)
		
		#Make Holes for zMotorMount plates
		#Sketch points
		p1x = 0
		p1y = 0
		p2x = p1x
		p2y = (gv.crossBarLength - gv.yRodSpacing - gv.yRodSupportMountHoleSpacing)/2
		p3x = p1x
		p3y = (gv.crossBarLength - gv.yRodSpacing + gv.yRodSupportMountHoleSpacing)/2
		p4x = p1x
		p4y = (gv.crossBarLength + gv.yRodSpacing - gv.yRodSupportMountHoleSpacing)/2
		p5x = p1x
		p5y = (gv.crossBarLength + gv.yRodSpacing + gv.yRodSupportMountHoleSpacing)/2
		p6x = p1x
		p6y = gv.crossBarLength
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = uf.getFace(App.ActiveDocument.Pad,
														 gv.crossBarLength/2, 0,
														 None, None,
														 gv.frameHeight/2, 0)
		App.activeDocument().recompute()
#		#.activeDocument().setEdit('Sketch001')
		App.ActiveDocument.Sketch001.addExternal("Pad",uf.getEdge(App.ActiveDocument.Pad,
																 gv.crossBarLength, 0,
																 None, None, 
																 gv.frameHeight/2, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Vertical',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',4,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.toggleConstruction(0) 
		App.ActiveDocument.Sketch001.toggleConstruction(1) 
		App.ActiveDocument.Sketch001.toggleConstruction(2) 
		App.ActiveDocument.Sketch001.toggleConstruction(3) 
		App.ActiveDocument.Sketch001.toggleConstruction(4) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',5,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',6,3,1,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p4x,p4y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',7,3,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Circle(App.Vector(p5x,p5y,0),App.Vector(0,0,1),gv.mountToFrameDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',8,3,3,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',8,7)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',7,6)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',6,5)) 
		App.ActiveDocument.recompute()
		
		#Add Dimensions
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',8,gv.mountToFrameDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',3,gv.yRodSupportMountHoleSpacing)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceY',4,p2y)) 
		App.ActiveDocument.recompute()
#		#.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut holes through All
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		#.activeDocument().hide("Sketch001")
		#.activeDocument().hide("Pad")
#		#.ActiveDocument.Pocket.ShapeColor=#.ActiveDocument.Pad.ShapeColor
#		#.ActiveDocument.Pocket.LineColor=#.ActiveDocument.Pad.LineColor
#		#.ActiveDocument.Pocket.PointColor=#.ActiveDocument.Pad.PointColor
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()
		
		#Make hole for yBeltIdler
		#Sketch Points
		p1x = 0
		p1y = 0
		p2x = p1x
		p2y = gv.crossBarLength/2
		p3x = p1x
		p3y = gv.crossBarLength
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = uf.getFace(App.ActiveDocument.Pocket,
														 gv.crossBarLength/2, 0,
														 None, None,
														 gv.frameHeight/2, 0)
		App.activeDocument().recompute()
#		#.activeDocument().setEdit('Sketch002')
		App.ActiveDocument.Sketch002.addExternal("Pocket",uf.getEdge(App.ActiveDocument.Pocket,
																 gv.crossBarLength, 0,
																 None, None, 
																 gv.frameHeight/2, 0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',-1,1,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',1,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',1,0)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.toggleConstruction(1) 
		App.ActiveDocument.Sketch002.toggleConstruction(0) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),gv.yBeltIdlerHoleDia/2))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,3,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.movePoint(1,0,App.Vector(0.000000,0.000000,0),1)
		App.ActiveDocument.recompute()
		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',2,gv.yBeltIdlerHoleDia/2)) 
		App.ActiveDocument.recompute()
#		#.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut hole through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket001")
		App.activeDocument().Pocket001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pocket001.Length = 5.0
		App.ActiveDocument.recompute()
		#.activeDocument().hide("Sketch002")
		#.activeDocument().hide("Pocket")
#		#.ActiveDocument.Pocket001.ShapeColor=#.ActiveDocument.Pocket.ShapeColor
#		#.ActiveDocument.Pocket001.LineColor=#.ActiveDocument.Pocket.LineColor
#		#.ActiveDocument.Pocket001.PointColor=#.ActiveDocument.Pocket.PointColor
		App.ActiveDocument.Pocket001.Length = 5.000000
		App.ActiveDocument.Pocket001.Type = 1
		App.ActiveDocument.Pocket001.UpToFace = None
		App.ActiveDocument.recompute()
#		#.activeDocument().resetEdit()

		