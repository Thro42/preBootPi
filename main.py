from PySide6.QtWidgets import QApplication
import sys
from src.mainwindow import MainWindow
from src.appsttings import AppSettings

class MyApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.appSettings = AppSettings()
        
    def getAppSettings(self):
        return self.appSettings

app = MyApplication(sys.argv)

window = MainWindow(app)
window.show()

app.exec()