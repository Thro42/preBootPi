import os.path
import configparser
from src.config import *

class AppSettings:
    def __init__(self):
        self.filename = INI_FILE
        self._isModify = False
        self.config = configparser.ConfigParser()
        if os.path.isfile(self.filename):
            self.config.read(self.filename)
        else:
            self._isModify = True
            self.config.set('DEFAULTS','COUNTRY_CODE', 'DE')
            self.config.set('DEFAULTS','TIMEZONE', 'Europe/Berlin')
            self.config.set('DEFAULTS','KEYBOARD_LAYOUT', 'de')
    
    def isModify(self):
        return self._isModify
    
    def getAppConfig(self):
        return self.config
    
    def setOption(self,section,option,value):
        if self.config.has_section(section) != True:
            self.config.add_section(section)
        self.config.set(section, option, value)
        self._isModify = True

    def getDefaultOption(self,section,option):
        return self.config.get(section, option)
    
    def setDefaultOption(self, option,value):
        self.config.set('DEFAULTS', option, value)
        self._isModify = True

    def getDefaultOption(self,option):
        return self.config.get('DEFAULTS', option)
    