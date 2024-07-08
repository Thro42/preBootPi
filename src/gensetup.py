import os.path
import json
from src.config import *

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QComboBox, QDialog,
    QDialogButtonBox, QFormLayout, QGridLayout, QLabel,
    QLineEdit, QPushButton, QSizePolicy, QWidget)

class genSetupDlg(QDialog):
    def __init__(self, parent, appConfig):
        self.appConfig = appConfig
        self.parent = parent
        self.options = appConfig.getRaspbianOptions()
        print(self.options)
        super().__init__(parent)
        self.resize(422, 122)
        self.setWindowTitle(u"General Setup")

        self.countryCode = self.appConfig.getDefaultOption('country_code')
        self.timeZone = self.appConfig.getDefaultOption('timezone')
        self.keyLayout = self.appConfig.getDefaultOption('keyboard_layout')


        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 80, 401, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)


        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(9, 9, 401, 23))
        self.ContryCodeLayout = QFormLayout(self.formLayoutWidget)
        self.ContryCodeLayout.setObjectName(u"ContryCodeLayout")
        self.ContryCodeLayout.setContentsMargins(0, 0, 0, 0)
        self.contryCodeLbl = QLabel(self.formLayoutWidget)
        self.contryCodeLbl.setObjectName(u"contryCodeLbl")
        self.contryCodeLbl.setMinimumSize(QSize(90, 0))
        self.contryCodeLbl.setText( u"Contry Code    ")

        self.ContryCodeLayout.setWidget(0, QFormLayout.LabelRole, self.contryCodeLbl)

        self.contryCodeCB = QComboBox(self.formLayoutWidget)
        self.contryCodeCB.setObjectName(u"contryCodeCB")
        self.fill_contryCodeCB()
        self.ContryCodeLayout.setWidget(0, QFormLayout.FieldRole, self.contryCodeCB)

        self.formLayoutWidget_2 = QWidget(self)
        self.formLayoutWidget_2.setObjectName(u"formLayoutWidget_2")
        self.formLayoutWidget_2.setGeometry(QRect(10, 30, 401, 23))
        self.TimeZoneForm = QFormLayout(self.formLayoutWidget_2)
        self.TimeZoneForm.setObjectName(u"TimeZoneForm")
        self.TimeZoneForm.setContentsMargins(0, 0, 0, 0)
        self.timeZoneLbl = QLabel(self.formLayoutWidget_2)
        self.timeZoneLbl.setObjectName(u"timeZoneLbl")
        self.timeZoneLbl.setMinimumSize(QSize(80, 0))

        self.TimeZoneForm.setWidget(0, QFormLayout.LabelRole, self.timeZoneLbl)

        self.TimeZoneCB = QComboBox(self.formLayoutWidget_2)
        self.TimeZoneCB.setObjectName(u"TimeZoneCB")

        self.TimeZoneForm.setWidget(0, QFormLayout.FieldRole, self.TimeZoneCB)
        self.TimeZoneCB.setObjectName(u"TimeZoneCB")
        self.fill_TimeZoneCB()

        self.TimeZoneForm.setWidget(0, QFormLayout.FieldRole, self.TimeZoneCB)

        self.formLayoutWidget_3 = QWidget(self)
        self.formLayoutWidget_3.setObjectName(u"formLayoutWidget_3")
        self.formLayoutWidget_3.setGeometry(QRect(10, 50, 401, 23))
        self.KeyLayoutForm = QFormLayout(self.formLayoutWidget_3)
        self.KeyLayoutForm.setObjectName(u"KeyLayoutForm")
        self.KeyLayoutForm.setContentsMargins(0, 0, 0, 0)
        self.KeyLayoutCB = QComboBox(self.formLayoutWidget_3)
        self.KeyLayoutCB.setObjectName(u"KeyLayoutCB")

        self.KeyLayoutForm.setWidget(0, QFormLayout.FieldRole, self.KeyLayoutCB)

        self.KeyLayoutLbl = QLabel(self.formLayoutWidget_3)
        self.KeyLayoutLbl.setObjectName(u"KeyLayoutLbl")
        self.KeyLayoutLbl.setMinimumSize(QSize(90, 0))

        self.KeyLayoutForm.setWidget(0, QFormLayout.LabelRole, self.KeyLayoutLbl)

        self.fill_KeyLayoutCB()

        self.retranslateUi(self)
        self.buttonBox.accepted.connect(self.do_accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)
    # setupUi
    def do_accept(self):
#        self.appConfig.setRaspbianOptions(self.options)
        self.appConfig.setDefaultOption('country_code',str(self.contryCodeCB.currentText()))
        self.appConfig.setDefaultOption('timezone',str(self.TimeZoneCB.currentText()))
        self.appConfig.setDefaultOption('keyboard_layout',str(self.KeyLayoutCB.currentText()))
        self.accept()

    def retranslateUi(self, genSetup):
        self.contryCodeLbl.setText( u"Contry Code    ")
        self.timeZoneLbl.setText(u"Time Zone      ")
        self.KeyLayoutLbl.setText( u"Keybord Layout  ")
    # retranslateUi
    
    def fill_contryCodeCB(self):
        fname = COUNTRY_LIST
        idx = 0
        contry_idx = 0
        countryList = []
        with open(fname) as file_object:
            countryList = json.load(file_object)
        for country in countryList:
            self.contryCodeCB.addItem(country["name"],country["code"])
            if(country["code"] == self.countryCode):
                contry_idx = idx
            idx = idx + 1
        self.contryCodeCB.setCurrentIndex(contry_idx)

    def fill_TimeZoneCB(self):
        idx = 0
        zone_idx = 0
        file = open(TIMEZONE_FILE, "r")
        while True:
            content=file.readline()
            if not content:
                break
            content = content .strip()
            self.TimeZoneCB.addItem(content,content)
            if(content == self.timeZone):
                zone_idx = idx
            idx = idx + 1
        file.close()
        print("zone_idx", zone_idx)
        self.TimeZoneCB.setCurrentIndex(zone_idx)
    
    def fill_KeyLayoutCB(self):
        idx = 0
        key_idx = 0
        fname = KEMAP_FILE
        kemapList = []
        with open(fname) as file_object:
            kemapList = json.load(file_object)
        for map in kemapList:
            self.KeyLayoutCB.addItem(map["layout"],map["layout"])
            if(map["layout"] == self.keyLayout):
                key_idx = idx
            idx = idx + 1
        self.KeyLayoutCB.setCurrentIndex(key_idx)

