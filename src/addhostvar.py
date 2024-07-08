# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'HostVarAddMvsxAZ.ui'
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
    QFormLayout, QLabel, QLineEdit, QSizePolicy, 
    QWidget)

class AddHostVarDlg(object):
    def setupUi(self, AddHostVarDlg):
        if not AddHostVarDlg.objectName():
            AddHostVarDlg.setObjectName(u"AddHostVarDlg")
        AddHostVarDlg.resize(376, 139)
#        AddHostVarDlg.resize(376, 346)
        self.buttonBox = QDialogButtonBox(AddHostVarDlg)
        self.buttonBox.setObjectName(u"buttonBox")
        self.buttonBox.setGeometry(QRect(30, 100, 341, 32))
        self.buttonBox.setOrientation(Qt.Orientation.Horizontal)
        self.buttonBox.setStandardButtons(QDialogButtonBox.StandardButton.Cancel|QDialogButtonBox.StandardButton.Ok)
        self.formLayoutWidget = QWidget(AddHostVarDlg)
        self.formLayoutWidget.setObjectName(u"formLayoutWidget")
        self.formLayoutWidget.setGeometry(QRect(10, 10, 361, 71))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setObjectName(u"formLayout")
        self.formLayout.setContentsMargins(0, 0, 0, 0)
        self.varKeyLbl = QLabel(self.formLayoutWidget)
        self.varKeyLbl.setObjectName(u"varKeyLbl")

        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.varKeyLbl)

        self.varKeyEdit = QLineEdit(self.formLayoutWidget)
        self.varKeyEdit.setObjectName(u"varKeyEdit")

        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.varKeyEdit)

        self.varValueEdit = QLineEdit(self.formLayoutWidget)
        self.varValueEdit.setObjectName(u"varValueEdit")

        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.varValueEdit)

        self.varValueLbl = QLabel(self.formLayoutWidget)
        self.varValueLbl.setObjectName(u"varValueLbl")

        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.varValueLbl)


        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.varTabe)

        self.retranslateUi(AddHostVarDlg)
        self.buttonBox.accepted.connect(AddHostVarDlg.accept)
        self.buttonBox.rejected.connect(AddHostVarDlg.reject)


        QMetaObject.connectSlotsByName(AddHostVarDlg)
    # setupUi

    def retranslateUi(self, AddHostVarDlg):
        AddHostVarDlg.setWindowTitle(QCoreApplication.translate("AddHostVarDlg", u"Add Host Var", None))
        self.varKeyLbl.setText(QCoreApplication.translate("AddHostVarDlg", u"Host Variable", None))
        self.varValueLbl.setText(QCoreApplication.translate("AddHostVarDlg", u"Value", None))
    # retranslateUi

