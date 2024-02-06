import os, string
from ctypes import windll
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QSize, QTime, QUrl, Qt)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,QCheckBox,
    QDialogButtonBox, QFormLayout, QLabel, QSizePolicy,QMessageBox,
    QWidget)
from src.ubuntu import UbuntuSettings
from src.raspbian import RaspbianSettings
from src.dietpi import DietPiSettings
from src.config import *

class PreBootOut(QDialog):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.resize(292, 166)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 120, 271, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setGeometry(QRect(10, 20, 261, 91))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.driveLbl = QLabel(self.formLayoutWidget)

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.driveLbl)

        self.driveCB = QComboBox(self.formLayoutWidget)

        bitmask = windll.kernel32.GetLogicalDrives()
        print(bitmask)
        letter = ord('A')
        while bitmask > 0:
            if bitmask & 1:
                if chr(letter) != 'C':
                    print(letter)
                    drv = chr(letter) + ':\\'
                    self.driveCB.addItem(drv,drv)
            bitmask >>= 1
            letter += 1

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.driveCB)

        self.label = QLabel(self.formLayoutWidget)

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.label)

        self.comboBox = QComboBox(self.formLayoutWidget)
        nodeArr = self.model.getNodeArry()
        for node in nodeArr:
            self.comboBox.addItem(node['name'],node['name'])

        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.comboBox)

        self.cbNetwork = QCheckBox(self.formLayoutWidget)
        self.cbNetwork.setText(u"Network Data")
        self.cbNetwork.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.cbNetwork)

        self.cbUser = QCheckBox(self.formLayoutWidget)
        self.cbUser.setText(u"User Data")
        self.cbUser.setChecked(True)

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.cbUser)
        self.buttonBox.accepted.connect(self.acceptSelection)
        self.buttonBox.rejected.connect(self.reject)

    def acceptSelection(self):
        theDrive = self.driveCB.currentText()
        theNode =  self.comboBox.currentText()
        nodeArr = self.model.getNodeArry()
        for node in nodeArr:
            if node['name'] == theNode:
                 self.prepBootFiles(theDrive, node)
        self.accept()

    def selectNode(self, node):
        self.comboBox.setCurrentText(node['name'])
        
    def prepBootFiles(self, drive, node):
        print("Drive: ", drive)
        print("Node: ", node['name'])
        print(" OS: ", node['os'])
        if node['os'] == "ubuntu":
            self.prepareUbuntu(drive, node)
        elif node['os'] == "bullseye":
            print("Perpare firstrun.sh")
            self.prepareRaspbian(drive, node)
        elif node['os'] == "bookworm":
            print("Perpare interfaces")
            self.prepareRaspbian(drive, node)
        elif node['os'] == "dietpi":
            self.prepareDietpi(drive, node)

    def prepareDietpi(self, drive, node):
        print("Perpare Dietpi")
        settings = self.model.getSettings()
        dietpi = DietPiSettings(self, settings,drive,node)
        if dietpi.check_sd_os() != True:
            QMessageBox.critical(self, 'Wrong SD-Card', 'SD-Card is not for ' + node['os'])
        else:
            dietpi.save_dietpi()

    def prepareUbuntu(self, drive, node):
        print("Perpare ubuntu")
        settings = self.model.getSettings()
        ubuntu = UbuntuSettings(settings,drive,node)
        if ubuntu.check_sd_os() != True:
            QMessageBox.critical(self, 'Wrong SD-Card', 'SD-Card is not for ' + node['os'])
        else:
            if self.cbUser.isChecked() == True:
                print("Perpare user-data")
                ubuntu.save_user_data()
            if self.cbNetwork.isChecked() == True:
                print("Perpare network-config")
                ubuntu.save_net_config()
                print("set IP to:", node['ip'])
            QMessageBox.information(self, 'SD-Card pepard', 'SD-Card pepard for '+ node['os'])

    def prepareRaspbian(self, drive, node):
        print("Perpare Raspbian")
        settings = self.model.getSettings()
        raspbian = RaspbianSettings(self, settings,drive,node)
        if raspbian.check_sd_os() != True:
            QMessageBox.critical(self, 'Wrong SD-Card', 'SD-Card is not for ' + node['os'])
        else:
            if self.cbUser.isChecked() == True:
                raspbian.save_firstrun()
            if self.cbNetwork.isChecked() == True:
                if node['os'] == "bookworm":
                    raspbian.save_interface()
                elif node['os'] == "bullseye":
                    raspbian.save_dhcpcd_conf()
                else:
                    QMessageBox.critical(self, 'Wrong OS', 'OS ' + node['os'] + ' is not supported')
                
            QMessageBox.information(self, 'SD-Card pepard', 'SD-Card pepard for '+ node['os'])
