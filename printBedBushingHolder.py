#import Math stuff
from __future__ import division # allows floating point division from integersimport math
import math
from itertools import product

#import FreeCAD modules
import FreeCAD as App
import FreeCADGui as Gui
import Part
import Sketcher
import Draft

#Specific to printer
import globalVars as gv
import utilityFunctions as Util

class PrintBedBushingHolder(object):
	def __init__(self,
				#The following attributes depend on which bushing holder is being made R or L
				name = "PBBH", 
				side = "Right",
				):
		self.name = name
		self.side = side
		
	def assemble(self):
		App.ActiveDocument=App.getDocument(self.name)
		shape = App.ActiveDocument.ActiveObject.Shape
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Gui.ActiveDocument=Gui.getDocument("PrinterAssembly")
		App.ActiveDocument.addObject('Part::Feature',self.name).Shape= shape
		
		#Color Part
		Gui.ActiveDocument.getObject(self.name).ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
		
		#Get the feature and move it into position
		objs = App.ActiveDocument.getObjectsByLabel(self.name)
		shape = objs[-1]		
		
		#Rotate into correct orientation
		rotateAngle = 180
		rotateCenter = App.Vector(0,0,0)
		rotateAxis = App.Vector(0,1,0)
		Draft.rotate([shape],rotateAngle,rotateCenter,axis = rotateAxis,copy=False)

		#Define shifts and move the left clamp into place
		if self.side =="Right":
			xShift = gv.yRodSpacing/2
		else:
			xShift = -gv.yRodSpacing/2
		yShift = -gv.yBushingNutSeparation/2
		zShift = gv.PBBHStandoff
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()

		if shape not in gv.yAxisParts:
			gv.yAxisParts.append(shape)		

		#Make a copy of the y bushing holder
		App.ActiveDocument.addObject('Part::Feature',self.name+"Rear").Shape= shape.Shape
		#Color Part
		Gui.ActiveDocument.getObject(self.name+"Rear").ShapeColor = (gv.printedR,gv.printedG,gv.printedB,gv.printedA)
		
		#Define shifts and move y bushing holder into place
		xShift = 0
		yShift = gv.yBushingNutSeparation
		zShift = 0
	
		App.ActiveDocument=App.getDocument("PrinterAssembly")
		Draft.move([shape],App.Vector(xShift, yShift, zShift),copy=False)
		App.ActiveDocument.recompute()
		
		if shape not in gv.yAxisParts:
			gv.yAxisParts.append(shape)
		
	def draw(self):
		if self.side == "Right":
			self.rodDia = gv.yRodDiaR
			self.bushingNutFaceToFace = gv.yBushingNutR[2]
			self.bushingNutThickness = gv.yBushingNutR[3]
		elif self.side == "Left":
			self.rodDia = gv.yRodDiaL
			self.bushingNutFaceToFace = gv.yBushingNutL[2]
			self.bushingNutThickness = gv.yBushingNutL[3]		

		#helper Variables
# 		gv.printBedBusingSupportWidth = (4*gv.slotPadding+
# 					2*gv.slotDia+
# 					2*gv.slotWidth+
# 					2*gv.bushingNutPadding+
# 					gv.PBBHMaxFaceToFace)
		
		columnWidth = gv.PBBHMaxFaceToFace/math.cos(math.pi/6)+2*gv.bushingNutPadding
		
		
		#Make file and build part
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

		#Create Document
		App.newDocument(self.name)
		App.setActiveDocument(self.name)
		App.ActiveDocument=App.getDocument(self.name)
		Gui.ActiveDocument=Gui.getDocument(self.name)
		
		#Make base
		#Sketch points
		p1x = -gv.printBedBusingSupportWidth/2
		p1y = -gv.PBBHDepth/2
		p2x = -gv.printBedBusingSupportWidth/2
		p2y = gv.PBBHDepth/2
		p3x = gv.printBedBusingSupportWidth/2
		p3y = gv.PBBHDepth/2
		p4x = gv.printBedBusingSupportWidth/2
		p4y = -gv.PBBHDepth/2
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch')
		App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000,0.000000,0.000000),App.Rotation(0.000000,0.000000,0.000000,1.000000))
		Gui.activeDocument().activeView().setCamera('#Inventor V2.1 ascii \n OrthographicCamera {\n viewportMapping ADJUST_CAMERA \n position 0 0 87 \n orientation 0 0 1  0 \n nearDistance -112.88701 \n farDistance 287.28702 \n aspectRatio 1 \n focalDistance 87 \n height 143.52005 }')
#		Gui.activeDocument().setEdit('Sketch')
		
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.Sketch.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',0)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',1)) 
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Vertical',3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Symmetric',1,2,0,1,-1,1)) 
		App.ActiveDocument.recompute()
		
		#add dimensions
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceY',1,gv.PBBHDepth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('DistanceX',0,gv.printBedBusingSupportWidth)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Pad base
		App.activeDocument().addObject("PartDesign::Pad","Pad")
		App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
		App.activeDocument().Pad.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch")
		App.ActiveDocument.Pad.Length = gv.tabThickness
		App.ActiveDocument.Pad.Reversed = 0
		App.ActiveDocument.Pad.Midplane = 0
		App.ActiveDocument.Pad.Length2 = 100.000000
		App.ActiveDocument.Pad.Type = 0
		App.ActiveDocument.Pad.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		
		#Cut slot on right side
		#Sketch points
		p1x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p1y = 0
		p2x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p2y = 0
		p3x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p3y = -gv.slotDia/2
		p4x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2-gv.slotWidth
		p4y = gv.slotDia/2
		p5x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p5y = gv.slotDia/2
		p6x = gv.printBedBusingSupportWidth/2-gv.slotPadding-gv.slotDia/2
		p6y = -gv.slotDia/2
		p7x = gv.printBedBusingSupportWidth/2-gv.slotPadding
		p7y = 0
		
		#Make sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch001')
		App.activeDocument().Sketch001.Support = (App.ActiveDocument.Pad,["Face6"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch001')
		App.ActiveDocument.Sketch001.addExternal("Pad","Edge7")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p1x,p1y,0),App.Vector(0,0,1),4.217310),math.pi/2,-math.pi/2))
		App.ActiveDocument.Sketch001.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p2x,p2y,0),App.Vector(0,0,1),4.217310),-math.pi/2,math.pi/2))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch001.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',0,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',0,3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',1,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Tangent',1,3)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,1,3,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',0,2,2,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',2,2,1,1)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Coincident',3,2,1,2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Horizontal',2)) 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',0,3,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addGeometry(Part.Point(App.Vector(32.724319,-0.106919,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,-1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('PointOnObject',4,1,1))
		
		#add dimensions 
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('DistanceX',2,gv.slotWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Radius',1,gv.slotDia/2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch001.addConstraint(Sketcher.Constraint('Distance',4,1,-3,gv.slotPadding)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		#Cut slot through all
		App.activeDocument().addObject("PartDesign::Pocket","Pocket")
		App.activeDocument().Pocket.Sketch = App.activeDocument().Sketch001
		App.activeDocument().Pocket.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch001")
		Gui.activeDocument().hide("Pad")
#		Gui.ActiveDocument.Pocket.ShapeColor=Gui.ActiveDocument.Pad.ShapeColor
#		Gui.ActiveDocument.Pocket.LineColor=Gui.ActiveDocument.Pad.LineColor
#		Gui.ActiveDocument.Pocket.PointColor=Gui.ActiveDocument.Pad.PointColor
		App.ActiveDocument.Pocket.Length = 5.000000
		App.ActiveDocument.Pocket.Type = 1
		App.ActiveDocument.Pocket.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
	
		#Mirror the slot
		App.activeDocument().addObject("PartDesign::Mirrored","Mirrored")
		App.ActiveDocument.recompute()
		App.activeDocument().Mirrored.Originals = [App.activeDocument().Pocket,]
		App.activeDocument().Mirrored.MirrorPlane = (App.activeDocument().Sketch001, ["V_Axis"])
		Gui.activeDocument().Pocket.Visibility=False
#		Gui.activeDocument().setEdit('Mirrored')
#		Gui.ActiveDocument.Mirrored.ShapeColor=Gui.ActiveDocument.Pocket.ShapeColor
#		Gui.ActiveDocument.Mirrored.DisplayMode=Gui.ActiveDocument.Pocket.DisplayMode
		App.ActiveDocument.Mirrored.Originals = [App.ActiveDocument.Pocket,]
		App.ActiveDocument.Mirrored.MirrorPlane = (App.ActiveDocument.Sketch001,["V_Axis"])
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()

		#Make bushing holder column
		#Sketch Points
		p1x = -columnWidth/2
		p1y = gv.tabThickness
		p2x = -columnWidth/2
		p2y = gv.PBBHStandoff
		p3x = 0
		p3y = gv.PBBHStandoff
		p4x = columnWidth/2
		p4y = gv.PBBHStandoff
		p5x = columnWidth/2
		p5y = gv.tabThickness
		
		#Make Sketch
		App.activeDocument().addObject('Sketcher::SketchObject','Sketch002')
		App.activeDocument().Sketch002.Support = (App.ActiveDocument.Mirrored,["Face1"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch002')
		App.ActiveDocument.Sketch002.addExternal("Mirrored","Edge4")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',0,1,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',0))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.ArcOfCircle(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),self.rodDia/2+gv.bushingNutRodGap),0,math.pi))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',1,3,-2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',1,2,0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',2,1,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('PointOnObject',2,2,-3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Vertical',2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,1,2,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',3,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Equal',0,2)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Symmetric',1,1,0,2,1,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addGeometry(Part.Circle(App.Vector(p3x,p3y,0),App.Vector(0,0,1),self.rodDia/2+gv.bushingNutRodGap))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Coincident',4,3,1,3)) 
		App.ActiveDocument.recompute()
		
		
		#Add dimensions
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',0,1,2,2,columnWidth)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Distance',-1,1,1,3,gv.PBBHStandoff)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch002.addConstraint(Sketcher.Constraint('Radius',4,self.rodDia/2+gv.bushingNutRodGap)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()
		
		
		#Extrude column
		App.activeDocument().addObject("PartDesign::Pad","Pad001")
		App.activeDocument().Pad001.Sketch = App.activeDocument().Sketch002
		App.activeDocument().Pad001.Length = 10.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch002")
		Gui.activeDocument().hide("Mirrored")
#		Gui.ActiveDocument.Pad001.ShapeColor=Gui.ActiveDocument.Mirrored.ShapeColor
#		Gui.ActiveDocument.Pad001.LineColor=Gui.ActiveDocument.Mirrored.LineColor
#		Gui.ActiveDocument.Pad001.PointColor=Gui.ActiveDocument.Mirrored.PointColor
		App.ActiveDocument.Pad001.Length = gv.PBBHDepth
		App.ActiveDocument.Pad001.Reversed = 1
		App.ActiveDocument.Pad001.Midplane = 0
		App.ActiveDocument.Pad001.Length2 = 100.000000
		App.ActiveDocument.Pad001.Type = 0
		App.ActiveDocument.Pad001.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
#		Gui.activeDocument().activeView().viewAxometric()

		#Refine shape
		App.ActiveDocument.addObject('Part::Feature','Pad002').Shape=App.ActiveDocument.Pad001.Shape.removeSplitter()
		App.ActiveDocument.ActiveObject.Label=App.ActiveDocument.Pad001.Label
		Gui.ActiveDocument.Pad001.hide()
#		Gui.ActiveDocument.ActiveObject.ShapeColor=Gui.ActiveDocument.Pad001.ShapeColor
#		Gui.ActiveDocument.ActiveObject.LineColor=Gui.ActiveDocument.Pad001.LineColor
#		Gui.ActiveDocument.ActiveObject.PointColor=Gui.ActiveDocument.Pad001.PointColor
		App.ActiveDocument.recompute()
		
		#make bushing nut trap
		#Sketch Points
		mat = Util.hexagonPoints(0,
							gv.PBBHStandoff,
							self.bushingNutFaceToFace,
							0)

		p1x = mat[0][0] 
		p1y = mat[0][1]
		p2x = mat[1][0]
		p2y = mat[1][1]
		p3x = mat[2][0]
		p3y = mat[2][1]
		p4x = mat[3][0]
		p4y = mat[3][1]
		p5x = mat[4][0]
		p5y = mat[4][1]
		p6x = mat[5][0]
		p6y = mat[5][1]
		p7x = mat[6][0]
		p7y = mat[6][1]
		hexRadius = mat[7][0]

		App.activeDocument().addObject('Sketcher::SketchObject','Sketch003')
		App.activeDocument().Sketch003.Support = (App.ActiveDocument.Pad002,["Face17"])
		App.activeDocument().recompute()
#		Gui.activeDocument().setEdit('Sketch003')
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p1x,p1y,0),App.Vector(p2x,p2y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p2x,p2y,0),App.Vector(p3x,p3y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',0,2,1,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p3x,p3y,0),App.Vector(p4x,p4y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',1,2,2,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p4x,p4y,0),App.Vector(p5x,p5y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',2,2,3,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p5x,p5y,0),App.Vector(p6x,p6y,0)))
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',3,2,4,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Line(App.Vector(p6x,p6y,0),App.Vector(p1x,p1y,0)))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',4,2,5,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',5,2,0,1)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addGeometry(Part.Circle(App.Vector(p7x,p7y,0),App.Vector(0,0,1),hexRadius))
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,1,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',0,2,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',1,2,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',2,2,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',3,2,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('PointOnObject',4,2,6)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',5,0)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',0,1)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',1,2)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',2,3)) 
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Equal',3,4)) 
		App.ActiveDocument.Sketch003.toggleConstruction(6) 
		App.ActiveDocument.Sketch003.addExternal("Pad002","Edge49")
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Coincident',-3,3,6,3)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Horizontal',4)) 
		App.ActiveDocument.recompute()
		App.ActiveDocument.Sketch003.addConstraint(Sketcher.Constraint('Distance',0,2,4,self.bushingNutFaceToFace)) 
		App.ActiveDocument.recompute()
#		Gui.getDocument(self.name).resetEdit()
		App.getDocument(self.name).recompute()

		#cut nut trap out
		App.activeDocument().addObject("PartDesign::Pocket","Pad003")
		App.activeDocument().Pad003.Sketch = App.activeDocument().Sketch003
		App.activeDocument().Pad003.Length = 5.0
		App.ActiveDocument.recompute()
		Gui.activeDocument().hide("Sketch003")
		Gui.activeDocument().hide("Pad002")
#		Gui.ActiveDocument.Pad003.ShapeColor=Gui.ActiveDocument.Pad001.ShapeColor
#		Gui.ActiveDocument.Pad003.LineColor=Gui.ActiveDocument.Pad001.LineColor
#		Gui.ActiveDocument.Pad003.PointColor=Gui.ActiveDocument.Pad001.PointColor
		App.ActiveDocument.Pad003.Length = gv.yBushingNutR[3]
		App.ActiveDocument.Pad003.Type = 0
		App.ActiveDocument.Pad003.UpToFace = None
		App.ActiveDocument.recompute()
#		Gui.activeDocument().resetEdit()
		

		#Make view axiometric
#		Gui.activeDocument().activeView().viewAxometric()
