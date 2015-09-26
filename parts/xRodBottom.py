from __future__ import division  # allows floating point division from integers

import part

class xRodBottom(part.Part):
    def __init__(self):
        self.neededInputs = [["Length_of_Shorter_X_Rod", "400"], ["Diameter", "8"]]
        self.dependencies = False
        self.name = "xRodBottom"
        self.printed = True

    def draw(self):

        self.defineVariables()
        # import FreeCAD modules
        import FreeCAD as App
        import Part
        import Sketcher

        try:
            App.getDocument('xRodBottom').recompute()
            App.closeDocument("xRodBottom")
            App.setActiveDocument("")
            App.ActiveDocument = None
        except:
            pass

        # make document
        App.newDocument("xRodBottom")
        App.setActiveDocument("xRodBottom")
        App.ActiveDocument = App.getDocument("xRodBottom")

        # make sketch
        App.activeDocument().addObject('Sketcher::SketchObject', 'Sketch')
        App.activeDocument().Sketch.Placement = App.Placement(App.Vector(0.000000, 0.000000, 0.000000),
                                                              App.Rotation(0.500000, 0.500000, 0.500000, 0.500000))
        App.ActiveDocument.Sketch.addGeometry(
            Part.Circle(App.Vector(50, 50, 0), App.Vector(0, 0, 1), self.Diameter / 2))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Coincident', 0, 3, -1, 1))
        App.ActiveDocument.recompute()
        App.ActiveDocument.Sketch.addConstraint(Sketcher.Constraint('Radius', 0, self.Diameter / 2))
        App.ActiveDocument.recompute()
        App.getDocument('xRodBottom').recompute()

        # Pad sketch
        App.activeDocument().addObject("PartDesign::Pad", "Pad")
        App.activeDocument().Pad.Sketch = App.activeDocument().Sketch
        App.activeDocument().Pad.Length = 10.0
        App.ActiveDocument.recompute()
        App.ActiveDocument.Pad.Length = self.Length_of_Shorter_X_Rod
        App.ActiveDocument.Pad.Reversed = 0
        App.ActiveDocument.Pad.Midplane = 0
        App.ActiveDocument.Pad.Length2 = 100.000000
        App.ActiveDocument.Pad.Type = 0
        App.ActiveDocument.Pad.UpToFace = None
        App.ActiveDocument.recompute()


        # set view as axiometric

