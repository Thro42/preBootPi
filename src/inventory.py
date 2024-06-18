import os.path
import yaml
import configparser
from src.config import *

class Inventory:
    def __init__(self):
        self.filename = NODES_INVENTORY
        self.config = configparser.ConfigParser()
        self.isModify = False

    def generate(self, nodeArr):
        rolles = []
        for node in nodeArr:
            if not node['rolle'] in rolles:
                rolles.append(node['rolle'])
        print(rolles)
        for rolle in rolles:
            self.config[rolle] = {}
            rolleConf = self.config[rolle]
            for node in nodeArr:
                if node['rolle'] == rolle:
                    hostLine = node['name'] + ' ansible_host'
                    ipLine = node['ip']
                    rolleConf[hostLine]= ipLine

        with open(self.filename, 'w') as configfile:
            self.config.write(configfile)

    def generate_yaml(self, nodeArr):
        yml_file = NODES_INVENTORY_YAML
        yaml_out = {}
        rolles = []
        for node in nodeArr:
            if not node['rolle'] in rolles:
                rolles.append(node['rolle'])
        for rolle in rolles:
            yaml_out[rolle] = {}
            rolleConf = yaml_out[rolle]
            for node in nodeArr:
                if node['rolle'] == rolle:
                    hostLine = []
                    hostLine['ansible_host'] =  node['ip']
                    rolleConf[node['name']] = hostLine
        
        with open(yml_file, 'w', newline='\n') as yaml_file:
            yaml.dump(yaml_out, yaml_file)