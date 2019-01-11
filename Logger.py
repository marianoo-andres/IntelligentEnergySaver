import logging

class Logger(object):
    # Here will be the instance stored.
    __instance = None

    @staticmethod
    def getInstance():
        """ Static access method. """
        if Logger.__instance == None:
            Logger()
        return Logger.__instance

    def __init__(self):
        self.__initialize()
        """ Virtually private constructor. """
        if Logger.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            Logger.__instance = self

    def __initialize(self, name='logger', level=logging.DEBUG):
        self.name = name
        self.logger = logging.getLogger(self.name)
        self.logger.setLevel(level)

        formatter = logging.Formatter("[%(asctime)s - %(levelname)s] %(message)s", "%Y-%m-%d %H:%M:%S")

        fh = logging.FileHandler('%s.log' % self.name, 'a')
        fh.setFormatter(formatter)
        self.logger.addHandler(fh)

        sh = logging.StreamHandler()
        sh.setFormatter(formatter)
        self.logger.addHandler(sh)

    def debug(self, msg):
        self.logger.debug(msg)

    def info(self, msg):
        self.logger.info(msg)

    def warning(self, msg):
        self.logger.warning(msg)

    def error(self, msg):
        self.logger.error(msg)

    def disable(self):
        self.logger.disabled = True

    def enable(self):
        self.logger.disabled = False