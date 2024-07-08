# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'anseblejDKSXB.ui'
##
## Created by: Qt User Interface Compiler version 6.7.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QApplication, QDialog, QDialogButtonBox,
    QHBoxLayout, QLabel, QLineEdit, QPushButton,QFileDialog,
    QRadioButton, QSizePolicy, QWidget)

class ansibleDlg(QDialog):
    def __init__(self, parent, appConfig):
        self.appConfig = appConfig
        self.parent = parent
        self.options = appConfig.getRaspbianOptions()
        print(self.options)
        super().__init__(parent)
        self.resize(495, 131)
        self.setWindowTitle(u"Ansible Settings")

        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(10, 90, 481, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)

#inventory_type = YAML
#inventory_path = inventory

        self.inventory_type = self.appConfig.getDefaultOption('inventory_type')
        self.inventory_path = self.appConfig.getDefaultOption('inventory_path')


        self.horizontalLayoutWidget = QWidget(self)
        self.horizontalLayoutWidget.setObjectName(u"horizontalLayoutWidget")
        self.horizontalLayoutWidget.setGeometry(QRect(10, 10, 481, 31))
        self.ivTypeLayout = QHBoxLayout(self.horizontalLayoutWidget)
        self.ivTypeLayout.setObjectName(u"ivTypeLayout")
        self.ivTypeLayout.setContentsMargins(0, 0, 0, 0)
        self.label = QLabel(self.horizontalLayoutWidget)
        self.label.setObjectName(u"label")
        self.label.setText(u"Inventory Type")

        self.ivTypeLayout.addWidget(self.label)

        self.rbYAMLFile = QRadioButton(self.horizontalLayoutWidget)
        self.rbYAMLFile.setObjectName(u"rbYAMLFile")
        self.rbYAMLFile.setText(u"YAML File")
        if(self.inventory_type == 'YAML'):
            self.rbYAMLFile.setChecked(True)
        else:
            self.rbYAMLFile.setChecked(False)

        self.ivTypeLayout.addWidget(self.rbYAMLFile)

        self.rbINIFile = QRadioButton(self.horizontalLayoutWidget)
        self.rbINIFile.setObjectName(u"rbINIFile")
        self.rbINIFile.setText(u"INI File")
        if(self.inventory_type == 'INI'):
            self.rbINIFile.setChecked(True)
        else:
            self.rbINIFile.setChecked(False)

        self.ivTypeLayout.addWidget(self.rbINIFile)

        self.horizontalLayoutWidget_2 = QWidget(self)
        self.horizontalLayoutWidget_2.setObjectName(u"horizontalLayoutWidget_2")
        self.horizontalLayoutWidget_2.setGeometry(QRect(10, 50, 481, 31))
        self.InvPathLayout = QHBoxLayout(self.horizontalLayoutWidget_2)
        self.InvPathLayout.setObjectName(u"InvPathLayout")
        self.InvPathLayout.setContentsMargins(0, 0, 0, 0)
        self.label_2 = QLabel(self.horizontalLayoutWidget_2)
        self.label_2.setObjectName(u"label_2")
        self.label_2.setText(u"Inventory Path")

        self.InvPathLayout.addWidget(self.label_2)

        self.lineEdit = QLineEdit(self.horizontalLayoutWidget_2)
        self.lineEdit.setObjectName(u"lineEdit")
        self.lineEdit.setText(self.inventory_path)

        self.InvPathLayout.addWidget(self.lineEdit)

        self.pushButton = QPushButton(self.horizontalLayoutWidget_2)
        self.pushButton.setObjectName(u"pushButton")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.pushButton.sizePolicy().hasHeightForWidth())
        self.pushButton.setSizePolicy(sizePolicy)
#        icon = QIcon(QIcon.fromTheme(QIcon.ThemeIcon.FolderOpen))
#        self.pushButton.setIcon(icon)
        icon = QIcon('src/images/folder.png')
#        icon.addFile("src\images\folder.png", QSize(), QIcon.Mode.Normal, QIcon.State.Off)
        self.pushButton.setIcon(icon)
        self.pushButton.setText("")
        self.pushButton.clicked.connect(self.selectPath)

        self.InvPathLayout.addWidget(self.pushButton)

        self.buttonBox.accepted.connect(self.confirmSettigs)
        self.buttonBox.rejected.connect(self.reject)

        QMetaObject.connectSlotsByName(self)
    # setupUi

    def confirmSettigs(self):
        if(self.rbYAMLFile.isChecked()):
            self.appConfig.setDefaultOption('inventory_type','YAML')
        if(self.rbINIFile.isChecked()):
            self.appConfig.setDefaultOption('inventory_type','INI')

        self.appConfig.setDefaultOption('inventory_path', str(self.lineEdit.text()))
        self.accept()

    def selectPath(self):
        dir_path = QFileDialog.getExistingDirectory(
            parent=self,
            caption="Select directory",
            dir = self.inventory_path,
            options=QFileDialog.Option.ShowDirsOnly,)
        print(dir_path)
        self.inventory_path = dir_path
        self.lineEdit.setText(self.inventory_path)
