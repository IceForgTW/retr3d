from ConfigParser import SafeConfigParser
import abc
__author__ = 'Master'


class Part(object):
    __metaclass__ = abc.ABCMeta

    @abc.abstractmethod
    def __init__(self):
        self.name = "Part"
        self.neededInputs = []

    @abc.abstractproperty
    def __author__(self):
        return

    @abc.abstractproperty
    def __version__ (self):
        return

    @abc.abstractproperty
    def __status__(self):
        return

    @abc.abstractproperty
    def __contact__(self):
        return

    @abc.abstractproperty
    def neededInputs(self):
        return

    @abc.abstractproperty
    def dependencies(self):
        return

    @abc.abstractproperty
    def printed(self):
        return

    def defineVariables(self):
        parser = SafeConfigParser()
        parser.read('config.ini')
        for input in self.neededInputs:
            exec ("self." + input[0] + "=" + parser.get(self.name, input[0]))

    @abc.abstractmethod
    def draw(self):
        pass

