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
            self.setDefaultOption('COUNTRY_CODE', 'DE')
            self.setDefaultOption('TIMEZONE', 'Europe/Berlin')
            self.setDefaultOption('KEYBOARD_LAYOUT', 'de')
            self.setDefaultOption('NODES_BASE_DIR', 'nodes/')
    
    def save(self):
        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def isModify(self):
        return self._isModify
    
    def getAppConfig(self):
        return self.config
    
    def setOption(self,section,option,value):
        if self.config.has_section(section) != True:
            self.config.add_section(section)
        self.config.set(section, option, value)
        self._isModify = True
        print('Set: ' + section +'-' + option +'-' +  value)

    def getOption(self,section,option):
        if self.config.has_option(section, option):
            return self.config.get(section, option)
    
    def setDefaultOption(self, option,value):
        self.setOption('DEFAULTS', option, value)

    def getDefaultOption(self,option):
        return self.getOption('DEFAULTS', option)
        #return self.config.get('DEFAULTS', option)
    
    def getOptionList(self,section):
        if self.config.has_section(section) != True:
            return {}
        else:
            items = self.config.items(section)
            list = {}
            for key, value in items:
                list[key] = value
            return list

    def setOptionList(self, section, options):
        if self.config.has_section(section) != True:
            self.config.add_section(section)
        print(options)
        for key, value in options.items():
            self.setOption(section, key, value)
            #self.config.set(section, key, value)

    def getRaspbianOptions(self):
        return self.getOptionList('raspbian')

    def setRaspbianOptions(self, options):
        self.setOptionList('raspbian',options)

    def getUbuntuOptions(self):
        return self.getOptionList('ubuntu')

    def setUbuntuOptions(self, options):
        self.setOptionList('ubuntu',options)
