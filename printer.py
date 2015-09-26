import os
import datetime
from log import Logging
log = Logging()

__author__ = 'Master'

class Printer(object):
    def __init__(self):
        self.name = "retr3d"
        self.freecadDir = "C:\\Program Files (x86)\\FreeCAD 0.15\\bin"
        self.printerDir = "C:\\Users\\Master\\Documents\\Printers\\"
        self.getPrinterDirectory()
        self.getPartsDirectory()
        self.getSTLDirectory()


    def getPrinterDirectory(self):
        # Make dateString and add it to the directory string
        date = datetime.date.today().strftime("%m_%d_%Y")

        # make the printer's directory if it doesn't exist
        self.printerDir = self.printerDir + "Printer_" + date + "\\"
        if not os.path.exists(self.printerDir):
            try:
                os.makedirs(self.printerDir)
            except OSError as e:
                import traceback
                log.critical("Failure to save files, check your configuration file.",
                         'Error making "printerDir" in saveAndClose: ' + str(e) + '\n' + traceback.format_exc(limit=1),
                         log.level, os.path.basename(__file__))
                raise StandardError
        return self.printerDir

    def getPartsDirectory(self):
        # make the Parts directory if it doesn't exist
        self.partsDir = self.printerDir + "Parts\\"
        if not os.path.exists(self.partsDir):
            os.makedirs(self.partsDir)
        return self.partsDir

    def getSTLDirectory(self):
        # make the STLs directory if it doesn't exist
        self.stlDir = self.printerDir + "STL_Files\\"
        if not os.path.exists(self.stlDir):
            os.makedirs(self.stlDir)
        return self.stlDir