import yaml
import os.path
from PySide6.QtCore import QSize
from PySide6.QtGui import QAction,QIcon
from PySide6.QtWidgets import QMainWindow,QToolBar,QPushButton,QStatusBar,QMessageBox, QFileDialog
from src.nodetree import NodeTree
from src.nodeedit import NodeEditDlg
from src.prebootout import PreBootOut
from src.settings import SettingDlg
from src.wifi import WifiSettingDlg
from src.inventory import Inventory
from src.raspiSettings import RaspiSettingsDlg

class MainWindow(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.app = app #declare an app member
        self.setWindowTitle("preBootPi Pi Setup")
        self.setWindowIcon(QIcon('src\images\pi_setup.png'))
        self.resize(800,600)
        #Menubar and menus
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("File")

        save_action = file_menu.addAction("Open Node-base")
        save_action.triggered.connect(self.open_node_base)

        file_menu.addSeparator()
        save_action = file_menu.addAction("Preboot output")
        save_action.triggered.connect(self.preboot_out)

        setup_menu = file_menu.addMenu("Setup")

        save_action = setup_menu.addAction("Raspberry OS")
        save_action.triggered.connect(self.raspbian_setup)

        save_action = setup_menu.addAction("Wifi Setup")
        save_action.triggered.connect(self.wifi_setup)

        save_action = setup_menu.addAction("Node Settings")
        save_action.triggered.connect(self.edit_setting)


        save_action = file_menu.addAction("Generate Inventory")
        save_action.triggered.connect(self.save_inventory)

        file_menu.addSeparator()
        save_action = file_menu.addAction("Save")
        save_action.triggered.connect(self.save_date)
        file_menu.addSeparator()

        quit_action = file_menu.addAction("Quit")
        quit_action.triggered.connect(self.quit_app)
        # Import menu
        import_menu = menu_bar.addMenu("Inport")
        ubuntu_menu = import_menu.addMenu("Ubuntu")
        user_action = ubuntu_menu.addAction("Import user-data")
        user_action.triggered.connect(self.ubuntu_import_user_data)
        net_action = ubuntu_menu.addAction("Import network-config")
        net_action.triggered.connect(self.ubuntu_import_net_data)
        # Node menu
        edit_menu =menu_bar.addMenu("Node")
        add_action = edit_menu.addAction("Add")
        add_action.triggered.connect(self.add_node)

        #Working with toolbars
        toolbar = QToolBar("toolbar")
        toolbar.setIconSize(QSize(16, 16))
        self.addToolBar(toolbar)

        #Add the quit action to the toolbar
        toolbar.addAction(quit_action)
        # Working with status bars
        self.setStatusBar(QStatusBar(self))

        self.nodeTree = NodeTree(self)
        # Check if node-Base is set
        baseName = self.app.appSettings.getDefaultOption('NODES_BASE')
        if baseName:
            if os.path.isfile(baseName):
                self.nodeTree.setNodeBase(baseName)
            else:
                self.open_node_base()
        else:
            self.open_node_base()
        # self.nodeTree.loadTree()
        self.setCentralWidget(self.nodeTree)
        
    def quit_app(self):
        self.app.quitApp()

    def getAppConfig(self):
        return self.app.getAppConfig()
    
    def add_node(self):
        model = self.nodeTree.getTreeModel()
        dlg =  NodeEditDlg(self, model, "Add Node")
        dlg.exec()
        self.nodeTree.reloadTree()

    def save_date(self):
        model = self.nodeTree.getTreeModel()
        model.Save()

    def preboot_out(self):
        model = self.nodeTree.getTreeModel()
        dlg = PreBootOut(self,model)
        dlg.exec()

    def edit_setting(self):
        model = self.nodeTree.getTreeModel()
        dlg = SettingDlg(self, model)
        dlg.exec()

    def wifi_setup(self):
        model = self.nodeTree.getTreeModel()
        dlg = WifiSettingDlg(self,model)
        dlg.exec()

    def save_inventory(self):
        model = self.nodeTree.getTreeModel()
        nodeArr = model.getNodeArry()
        inventory = Inventory()
        inventory.generate(nodeArr)
        QMessageBox.information(self, 'Save Inventory', 'Inventory generated')

    def ubuntu_import_user_data(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Open user_data", "", "user-data")
        #print(fileName)
        if os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                imp_userdata = yaml.safe_load(file)
            if imp_userdata:
                model = self.nodeTree.getTreeModel()
                settings = model.getSettings()
                settings['firstuser'] = imp_userdata['users'][0]['name'] 
                settings['passwd'] = imp_userdata['users'][0]['passwd']
                #rsa = 'ssh-rsa ' + self.settings['ssh_rsa']
                rsa = imp_userdata['users'][0]['ssh_authorized_keys'][0]
                keylist = rsa.split('-rsa ')
                if keylist.len > 1:
                    settings['ssh_rsa']=keylist[1]

    def ubuntu_import_net_data(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Open network-config", "", "network-config")
        if os.path.isfile(fileName):
            with open(fileName, 'r') as file:
                imp_netdata = yaml.safe_load(file)
            if imp_netdata:
                model = self.nodeTree.getTreeModel()
                settings = model.getSettings()
                if imp_netdata['wifis']:
                    aps = imp_netdata['wifis']['wlan0']['access-points']
                    apName = list(aps.keys())[0]
                    # print(list(aps.keys())[0])
                    settings['access_point'] = apName
                    #print(imp_netdata['wifis']['wlan0']['access-points'][apName]['password'])
                    settings['access_passwd'] = imp_netdata['wifis']['wlan0']['access-points'][apName]['password']

    def raspbian_setup(self):
        appConfig = self.app.getAppSettings()
        dlg = RaspiSettingsDlg(self,appConfig)
        dlg.exec()

    def open_node_base(self):
        fileName, ok = QFileDialog.getOpenFileName(self, "Node Base", "", "*.json")
        #print(fileName)
        if os.path.isfile(fileName):
            self.nodeTree.setNodeBase(fileName)
            self.app.appSettings.setDefaultOption('NODES_BASE',fileName)