from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect, QCryptographicHash,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QCheckBox, QDialog,
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,
    QSizePolicy, QWidget)
from PySide6.QtNetwork import QPasswordDigestor
from src.nodemodel import NodeModel
from src.config import *

class WifiSettingDlg(QDialog):
    def __init__(self, parent, model):
        super().__init__(parent)
        self.model = model
        self.resize(332, 148)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 110, 311, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 311, 101))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        settings = self.model.getSettings()

        self.ssidLbl = QLabel(self.formLayoutWidget)
        self.ssidLbl.setObjectName(u"ssidLbl")
        self.ssidLbl.setText(u"Wifi SSID")

        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.ssidLbl)

        self.ssidEdit = QLineEdit(self.formLayoutWidget)
        self.ssidEdit.setObjectName(u"ssidEdit")        
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.ssidEdit)
        self.ssidEdit.setText( settings['access_point'])

        self.passwLbl = QLabel(self.formLayoutWidget)
        self.passwLbl.setObjectName(u"passwLbl")
        self.passwLbl.setText(u"Wifi Password")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.passwLbl)

        self.passwEdit = QLineEdit(self.formLayoutWidget)
        self.passwEdit.setObjectName(u"passwEdit")
        self.passwEdit.setEchoMode(QLineEdit.Password)

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.passwEdit)
        passwArr = bytearray(settings['access_passwd_clear'].encode('utf-8'))
        ssidArr = bytearray(settings['access_point'].encode('utf-8'))
        savedPassW = QPasswordDigestor.deriveKeyPbkdf2(QCryptographicHash.Algorithm.Sha1, passwArr, ssidArr, 4096, 32).toHex().toStdString()
        print(savedPassW)
        self.passwEdit.setText( settings['access_passwd_clear'] )

        self.showPwCB = QCheckBox(self.formLayoutWidget)
        self.showPwCB.setObjectName(u"showPwCB")
        self.showPwCB.setText(u"show Password")
        self.showPwCB.stateChanged.connect(self.toglePasswShow)

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.showPwCB)


        self.setWindowTitle('Wifi Setup')
        self.buttonBox.accepted.connect(self.acceptSettings)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)

    def acceptSettings(self):
        self.accept()
    
    def toglePasswShow(self, state):
        state = self.showPwCB.checkState()
        if state == Qt.CheckState.Checked:
            self.passwEdit.setEchoMode(QLineEdit.EchoMode.Normal)
        else:
            self.passwEdit.setEchoMode(QLineEdit.EchoMode.Password)
