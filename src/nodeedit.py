from PySide6.QtCore import (QCoreApplication, QDate, QDateTime, QLocale,
    QMetaObject, QObject, QPoint, QRect,
    QSize, QTime, QUrl, Qt, SIGNAL)
from PySide6.QtGui import (QBrush, QColor, QConicalGradient, QCursor,
    QFont, QFontDatabase, QGradient, QIcon,
    QImage, QKeySequence, QLinearGradient, QPainter,
    QPalette, QPixmap, QRadialGradient, QTransform)
from PySide6.QtWidgets import (QAbstractButton, QComboBox, 
    QDialogButtonBox, QFormLayout, QLabel, QLineEdit,QTableWidget, QTableWidgetItem,
    QSizePolicy, QWidget)
from PySide6.QtWidgets import QApplication, QDialog, QMainWindow, QPushButton

class NodeEditDlg(QDialog):
    def __init__(self, parent, model, title):
        super().__init__(parent)
        self.title = title
        self.model = model
        self.setWindowIcon(QIcon('images\pi_setup.png'))
#        self.resize(387, 196)
        self.resize(387, 346)
        self.buttonBox = QDialogButtonBox(self)
        self.buttonBox.setGeometry(QRect(290, 20, 81, 151))
        self.buttonBox.setOrientation(Qt.Vertical)
        self.buttonBox.setStandardButtons(QDialogButtonBox.Cancel|QDialogButtonBox.Ok)
        self.formLayoutWidget = QWidget(self)
#        self.formLayoutWidget.setGeometry(QRect(9, 9, 271, 176))
        self.formLayoutWidget.setGeometry(QRect(9, 9, 278, 331))
        self.formLayout = QFormLayout(self.formLayoutWidget)
        self.formLayout.setContentsMargins(0, 0, 0, 0)

        self.nameLbl = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.LabelRole, self.nameLbl)
        self.nameLbl.setText("Name")
        self.nameEdit = QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(0, QFormLayout.FieldRole, self.nameEdit)

        self.label_2 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(1, QFormLayout.LabelRole, self.label_2)
        self.label_2.setText("IP Addr.")
        self.ipEdit = QLineEdit(self.formLayoutWidget)
        self.formLayout.setWidget(1, QFormLayout.FieldRole, self.ipEdit)

        self.label_3 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(2, QFormLayout.LabelRole, self.label_3)
        self.label_3.setText("Network")

        self.networkCB = QComboBox(self.formLayoutWidget)
        self.networkCB.addItem("eth","eth")
        self.networkCB.addItem("wifi","wifi")
        self.formLayout.setWidget(2, QFormLayout.FieldRole, self.networkCB)

        self.label_4 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(3, QFormLayout.LabelRole, self.label_4)

        self.osCB = QComboBox(self.formLayoutWidget)
        for os in self.model.getOsList():
            self.osCB.addItem(os,os)
        self.formLayout.setWidget(3, QFormLayout.FieldRole, self.osCB)

        self.label_5 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(4, QFormLayout.LabelRole, self.label_5)

        self.typeCB = QComboBox(self.formLayoutWidget)
        for ctype in self.model.getTypeList():
            self.typeCB.addItem(ctype,ctype)
        self.formLayout.setWidget(4, QFormLayout.FieldRole, self.typeCB)

        self.label_6 = QLabel(self.formLayoutWidget)
        self.formLayout.setWidget(5, QFormLayout.LabelRole, self.label_6)

        self.roleCB = QComboBox(self.formLayoutWidget)
        for role in self.model.getRoleList():
            self.roleCB.addItem(role,role)
       
        self.formLayout.setWidget(5, QFormLayout.FieldRole, self.roleCB)
        self.varsLbl = QLabel(self.formLayoutWidget)
        self.varsLbl.setObjectName(u"varsLbl")

        self.formLayout.setWidget(6, QFormLayout.LabelRole, self.varsLbl)
        self.varsLbl.setText( u"Vars")

        self.varTabe = QTableWidget(self.formLayoutWidget)
        if (self.varTabe.columnCount() < 2):
            self.varTabe.setColumnCount(2)

        __qtablewidgetitem = QTableWidgetItem()
        __qtablewidgetitem.setText( u"Var Key")
        self.varTabe.setHorizontalHeaderItem(0, __qtablewidgetitem)
        __qtablewidgetitem1 = QTableWidgetItem()
        __qtablewidgetitem1.setText( u"Value")
        self.varTabe.setHorizontalHeaderItem(1, __qtablewidgetitem1)

        self.varTabe.setObjectName(u"varTabe")
        self.varTabe.setColumnCount(2)
        self.formLayout.setWidget(6, QFormLayout.FieldRole, self.varTabe)
        self.connect(self.varTabe, SIGNAL("cellChanged(int, int)"), self.tabCellChanged)

        self.setWindowTitle(self.title)
        self.label_4.setText("Os")
        self.label_5.setText("typ")
        self.label_6.setText("rolle")
        self.buttonBox.accepted.connect(self.addNewNode)
        self.buttonBox.rejected.connect(self.reject)
        self.buttonBox.accepted.connect(self.buttonBox.close)
       
        self.oldName = ''
        self.hostvars = []
        self.addBtn = QPushButton(self.formLayoutWidget)
        self.addBtn.setObjectName(u"addBtn")

        self.formLayout.setWidget(8, QFormLayout.LabelRole, self.addBtn)
        self.addBtn.setText(u"add")
        self.addBtn.clicked.connect(self.addButtonClick)
        self.addBtn.pressed.connect(self.addButtonPressed)

    def addButtonClick(self):
        var = {}
        var["key"] = ""
        var["value"] = ""
        self.hostvars.append(var)
        rowcnt = len(self.hostvars)
        self.varTabe.setRowCount(rowcnt)
        keyItem = QTableWidgetItem(str(var["key"]))
        valItem = QTableWidgetItem(str(var["value"]))
        self.varTabe.setItem(rowcnt, 0, keyItem)
        self.varTabe.setItem(rowcnt, 1, valItem)

    def addButtonPressed(self):
        var = {}
        var["key"] = ""
        var["value"] = ""

    def tabCellChanged(self, row:int, col:int ):
        print("row=",row,"col=",col)
        if self.hostvars:
            for i in range(self.varTabe.rowCount()):
                for j in range(self.varTabe.columnCount()):
                    celItem = self.varTabe.item(i, j)
                    cellVal = celItem.text()
                    print(i,j,cellVal)

            celItem = self.varTabe.item(row, col)
            cellVal = celItem.text()
            print("cellVal=",cellVal)
            varCol = self.hostvars[row]
            print(varCol)
            if(col == 0):
                print(varCol['key'],"->",cellVal)
                varCol['key'] = cellVal
            if(col == 1):
                print(varCol['value'],"->",cellVal)
                varCol['value'] = cellVal
            self.hostvars[row] = varCol



    def addNewNode(self):
        newName = self.nameEdit.text()
        newNodeJson = {"name": self.nameEdit.text(), "ip": self.ipEdit.text(),"network": str(self.networkCB.currentText()),"os": str(self.osCB.currentText()),"typ": str(self.typeCB.currentText()),"rolle": str(self.roleCB.currentText())}
        if self.hostvars:
            print(self.hostvars)
            newNodeJson["hostvars"] = self.hostvars

        node = self.model.getNodeByName(self.oldName)
        if node:
            self.model.removeNode(node)
        self.model.addNode(newNodeJson)
        self.accept()

    def fillNode(self, node):
        self.ackNode = node
        self.oldName = node['name']
        self.nameEdit.setText(node['name'])
        self.ipEdit.setText(node['ip'])
        self.networkCB.setCurrentText(node['network'])
        self.osCB.setCurrentText(node['os'])
        idx = self.model.getOsList().index(node['os'])
        self.osCB.setCurrentIndex(idx)

        self.typeCB.setCurrentText(node['typ'])
        idx = self.model.getTypeList().index(node['typ'])
        self.typeCB.setCurrentIndex(idx)

        idx = self.model.getRoleList().index(node['rolle'])
        self.roleCB.setCurrentText(node['rolle'])
        self.roleCB.setCurrentIndex(idx)
    
    def fillVars(self, node):
        self.ackNode = node
        self.hostvars = node['hostvars']
        varcnt = 0
        if self.hostvars:
            rowcnt = len(self.hostvars)
            self.varTabe.setRowCount(rowcnt)
            for var in self.hostvars:
                keyItem = QTableWidgetItem(str(var["key"]))
                valItem = QTableWidgetItem(str(var["value"]))
                print(keyItem.text(),valItem.text() )
                self.varTabe.setItem(varcnt, 0, keyItem)
                self.varTabe.setItem(varcnt, 1, valItem)
                varcnt = varcnt + 1
