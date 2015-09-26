import log
import ConfigParser
import importlib
from os import walk


class Controller(object):
    def __init__(self):
        self.freecadDir = "C:\\Program Files (x86)\\FreeCAD 0.15\\bin"
        self.printerDir = ""
        self.reloadClasses = False

    def start(self):
        log.header("______     _       _____     _           _____     __      _____ ", False)
        log.header("| ___ \   | |     |____ |   | |         |  _  |   /  |    |  _  |", False)
        log.header("| |_/ /___| |_ _ __   / / __| |  __   __| |/' |   `| |    | |/' |", False)
        log.header("|    // _ \ __| '__|  \ \/ _` |  \ \ / /|  /| |    | |    |  /| |", False)
        log.header("| |\ \  __/ |_| | .___/ / (_| |   \ V / \ |_/ / _ _| |_ _ \ |_/ /", False)
        log.header("\_| \_\___|\__|_| \____/ \__,_|    \_/   \___/ (_)\___/(_) \___/ ", False)
        log.bold("Version: 0.2.0 ", False)
        log.bold("If you encounter any issues, please let us know at https://github.com/maaphoo/retr3d/issues", False)
        self.generateConfig()
        self.drawParts()

    def getParts(self):
        x=[]
        Parts = []
        for (dirpath, dirnames, filenames) in walk('parts'):
            Parts.extend(filenames)
            break
        i=0
        for name in Parts:
            if ".py" in name and ".pyc" not in name and "__init__" not in name:
                Parts[i] = Parts[i].replace(".py", "")
            else:
                x.append(i)
            i= 1+i
        for num in list(reversed(x)):
            del Parts[num]
        return Parts

    def sortParts(self):
        parts = self.getParts()

        i=0
        x = []
        for part in parts:
            mod = importlib.import_module("parts."+part)
            Part = eval("mod."+parts[i]+"()")
            if Part.dependencies == False:
                x.append(i)
            i=i+1
        staticParts = []
        for num in list(reversed(x)):
            staticParts.append(parts[num])
            del parts[num]

        dynamicParts = []
        while(True):
            i=0
            x=[]
            for part in parts:
                for dynamicPart in dynamicParts:
                    i=0
                    if part == dynamicPart:
                        x.append(i)
                        i=i+1
            for num in list(reversed(x)):
                del parts[num]
            if parts == []:
                break
            for part in parts:
                mod = importlib.import_module("parts."+part)
                Part = eval("mod."+parts[i]+"()")
                i=i+1
                for depend in Part.dependencies:
                    if depend in staticParts:
                        dynamicParts.append(part)
                    elif depend in dynamicParts:
                        dynamicParts.append(part)
        return [staticParts, dynamicParts]




    def generateConfig(self):
        parts = self.getParts()

        parser = ConfigParser.SafeConfigParser()

        parser.add_section("File Paths")
        parser.set("File Paths", "FreeCAD Directory", "C:\\Program Files (x86)\\FreeCAD 0.15\\bin")
        parser.set("File Paths", "Printer Files Directory", "C:\\Users\\Public\\Documents\\Printers\\")

        i=0
        for part in parts:
            mod = importlib.import_module("parts."+part)
            Part = eval("mod."+parts[i]+"()")
            if Part.neededInputs:
                parser.add_section(part)
                for input in Part.neededInputs:
                    parser.set(part, input[0], input[1])
            i=i+1
        config = open('config.ini', 'w')
        parser.write(config)
        config.close()

    def drawParts(self):
        parts = self.sortParts()[0]
        i=0
        for part in parts:
            mod = importlib.import_module("parts."+part)
            Part = eval("mod."+parts[i]+"()")
            Part.draw()
            i = i+1
