from ConfigParser import SafeConfigParser

__author__ = 'Master'


class Part(object):
    def __init__(self):
        self.name = "Part"
        self.neededInputs = []

    def defineVariables(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        for input in self.neededInputs:
            exec ("self." + input[0] + "=" + parser.get(self.name, input[0]))
