import os.path
import json
from PySide6.QtCore import QCryptographicHash
from PySide6.QtNetwork import QPasswordDigestor
from src.config import *

class NodeModel:
    def __init__(self, filename):
        self.filename = filename
        self.model = []
        self.isModify = False

    def Load(self):
        if os.path.isfile(self.filename):
             fname = self.filename
        else:
             fname = NODES_SAMPLE

        with open(fname) as file_object:
                # store file data in object
                self.model = json.load(file_object)        
    
    def Save(self):
        try:
            with open(self.filename, "w") as file_write:
            # write json data into file
                json.dump(self.model, file_write)
                self.isModify = False
        except:
            print("Something went wrong")
   
    def getModel(self):
         return self.model

    def setModel(self, model):
         self.model = model
    
    def getNodeArry(self):
         return self.model['nodes']
    
    def addNode(self,node):
         self.isModify = True
         self.model['nodes'].append(node)

    def removeNode(self,node):
         self.isModify = True
         self.model['nodes'].remove(node)

    def getSettings(self):
         return self.model['settings']
    
    def getNodeByName(self, name):
        for node in self.model['nodes']:
            if node['name'] == name:
                 return node
     
    def setWifi(self,newSSID, newPassw):
         self.model['settings']['access_point'] = newSSID
         self.model['settings']['access_passwd_clear'] = newPassw
         passwArr = bytearray(newPassw.encode('utf-8'))
         ssidArr = bytearray(newSSID.encode('utf-8'))
         savedPassW = QPasswordDigestor.deriveKeyPbkdf2(QCryptographicHash.Algorithm.Sha1, passwArr, ssidArr, 4096, 32).toHex().toStdString()
         self.model['settings']['access_passwd'] = savedPassW

    def getOsList(self):
          osList = []
          osList.append("ubuntu")
          osList.append("bullseye")
          osList.append("bookworm")
#          osList.append("dietpi") # Not yet implementetd
          return osList

    def getTypeList(self):
         typeList = []
         typeList.append("rp3")
         typeList.append("rp4")
         typeList.append("rp5")
         typeList.append("cm4")
         typeList.append("cm5")
         return typeList
