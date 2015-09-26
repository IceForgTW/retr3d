import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import logging
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import platform
import __main__

class Logging(object):
    def __init__(self):
        if not os.path.exists(os.path.dirname(os.path.abspath(__file__)) + '/logs/'):
            os.makedirs(os.path.dirname(os.path.abspath(__file__)) + '/logs/')

        q = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs")
        LOG_FILENAME = os.path.join(q, "retr3d.log")
        logging.basicConfig(filename=LOG_FILENAME, level=logging.DEBUG, filemode='w')

        logging.info('Retr3d Log File')
        logging.info('Version 0.2.0')

        self.level = 5

    def log(self, msg, level, source):
        eval('logging.getLogger(source).' + level + '(msg)')

    def bold(self, msg, log):
        if log:
            logging.info(msg)
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[1m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('1')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            print msg


    def underline(msg, log):
        if log:
            logging.info(msg)
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[4m' + msg + '\x1b[0m'
        else:
            print msg


    def header(self, msg, log):
        if log:
            logging.info(msg)
        if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            print '\033[95m' + msg + '\x1b[0m'
        elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
            attr = []
            attr.append('35')
            attr.append('1')
            print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
        else:
            print msg


    def critical(self, msg, log, level, source):
        logging.getLogger(source).critical(log)
        if level <= 5:
            if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print '\033[1m\033[31m' + msg + '\x1b[0m'
            elif platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                attr = []
                attr.append('1')
                attr.append('31')
                print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
            else:
                if os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                    print msg
                else:
                    try:
                        from PySide import QtGui
                        QtGui.QMessageBox.critical(None, "Retr3d: Error", msg)
                    except:
                        pass


    def error(self, msg, log, level, source):
        logging.getLogger(source).error(log)
        if level <= 4:
            if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print '\033[91m' + msg + '\x1b[0m'
            elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                attr = []
                attr.append('31')
                print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
            else:
                print msg


    def warning(self, msg, log, level, source):
        logging.getLogger(source).warning(log)
        if level <= 3:
            if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print '\033[93m' + msg + '\x1b[0m'
            elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                attr = []
                attr.append('33')
                print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
            else:
                print msg


    def info(self, msg, log, level, source):
        logging.getLogger(source).info(log)
        if level <= 2:
            if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print '\033[92m' + msg + '\x1b[0m'
            elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                attr = []
                attr.append('32')
                print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
            else:
                print msg


    def debug(self, msg, log, level, source):
        logging.getLogger(source).debug(log)
        if level <= 1:
            if not platform.system() == 'Windows' and os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                print '\033[94m' + msg + '\x1b[0m'
            elif os.getcwd() == os.path.dirname(os.path.abspath(__file__)):
                attr = []
                attr.append('34')
                print '\x1b[%sm%s\x1b[0m' % (';'.join(attr), msg)
            else:
                print msg