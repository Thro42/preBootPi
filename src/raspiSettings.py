import os.path
from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,QFileDialog,
    QGridLayout, QLabel, QLineEdit, QSizePolicy,
    QToolButton, QWidget)

class RaspiSettingsDlg(QDialog):
    def __init__(self, parent, appConfig):
        self.appConfig = appConfig
        self.parent = parent
        self.options = appConfig.getRaspbianOptions()
        print(self.options)
        super().__init__(parent)
        self.resize(630, 181)
        self.setWindowTitle(u"Raspberry OS Settings")
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(10, 140, 611, 32))
        self.buttonBox.setOrientation(Qt.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.gridLayoutWidget = QWidget(self)
        self.gridLayoutWidget.setGeometry(QRect(9, 9, 611, 121))
        self.gridLayout = QGridLayout(self.gridLayoutWidget)
        self.gridLayout.setContentsMargins(0, 0, 0, 0)

        self.interfaceLbl = QLabel(self.gridLayoutWidget)
        self.interfaceLbl.setText(u"Interfaces Template")
        self.gridLayout.addWidget(self.interfaceLbl, 1, 0, 1, 1)
        self.InterfaceEdit = QLineEdit(self.gridLayoutWidget)
        if 'interface' in self.options:
            interface = self.options['interface']
        else:
            interface = 'interfaces.net'
            self.options['interface'] = interface
        self.InterfaceEdit.setText(interface)

        self.gridLayout.addWidget(self.InterfaceEdit, 1, 2, 1, 1)
        self.InterfaceBtn = QToolButton(self.gridLayoutWidget)
        self.InterfaceBtn.setText(u"...")
        self.InterfaceBtn.clicked.connect(self.SelInterfaceFile)
        self.gridLayout.addWidget(self.InterfaceBtn, 1, 3, 1, 1)

        self.firstrunEdit = QLineEdit(self.gridLayoutWidget)
        if 'firstrun' in self.options:
            firstrun = self.options['firstrun']
        else:
            firstrun = 'firstrun.sh'
            self.options['firstrun'] = firstrun
        self.firstrunEdit.setText(firstrun)
        self.gridLayout.addWidget(self.firstrunEdit, 0, 2, 1, 1)

        self.firstRunBtn = QToolButton(self.gridLayoutWidget)
        self.firstRunBtn.setText(u"...")
        self.firstRunBtn.clicked.connect(self.SelfirstRunFile)
        self.gridLayout.addWidget(self.firstRunBtn, 0, 3, 1, 1)
        self.firstrunLbl = QLabel(self.gridLayoutWidget)
        self.firstrunLbl.setText(u"Firstrun Template")
        self.gridLayout.addWidget(self.firstrunLbl, 0, 0, 1, 1)

        self.dhcpcdEdit = QLineEdit(self.gridLayoutWidget)

        if 'dhcpcd' in self.options:
            dhcpcd = self.options['dhcpcd']
        else:
            dhcpcd = 'dhcpcd.conf'
            self.options['dhcpcd'] = dhcpcd
        self.dhcpcdEdit.setText(dhcpcd)

        self.gridLayout.addWidget(self.dhcpcdEdit, 2, 2, 1, 1)
        self.dhcpcdBtn = QToolButton(self.gridLayoutWidget)
        self.dhcpcdBtn.setText(u"...")
        self.dhcpcdBtn.clicked.connect(self.SelDhcpcdFile)
        self.gridLayout.addWidget(self.dhcpcdBtn, 2, 3, 1, 1)
        self.dhcpcdLbl = QLabel(self.gridLayoutWidget)
        self.dhcpcdLbl.setText(u"Dhcpcd Template")
        self.gridLayout.addWidget(self.dhcpcdLbl, 2, 0, 1, 1)


        self.buttonBox.accepted.connect(self.do_accept)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)

    def SelfirstRunFile(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Open Firstrun Template", "", "firstrun.sh")
        if os.path.isfile(fileName):
            self.options['firstrun'] = fileName
            self.firstrunEdit.setText(fileName)

    def do_accept(self):
        self.appConfig.setRaspbianOptions(self.options)
        self.accept()

    def SelInterfaceFile(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Open Interface Template", "", "interfaces.net")
        if os.path.isfile(fileName):
            self.options['interface'] = fileName
            self.InterfaceEdit.setText(fileName)

    def SelDhcpcdFile(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Open Dhcpcd Template", "", "dhcpcd.conf")
        if os.path.isfile(fileName):
            self.options['dhcpcd'] = fileName
            self.dhcpcdEdit.setText(fileName)
