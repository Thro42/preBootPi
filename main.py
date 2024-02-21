from PySide6.QtWidgets import QApplication
import sys
from src.mainwindow import MainWindow
from src.appsettings import AppSettings

class MyApplication(QApplication):
    def __init__(self, args):
        super().__init__(args)
        self.appSettings = AppSettings()

    def getAppSettings(self):
        return self.appSettings
    
    def quitApp(self):
        if self.appSettings.isModify():
            self.appSettings.save()
        self.quit()

def main():
    app = MyApplication(sys.argv)

    window = MainWindow(app)
    window.show()

    app.exec()

if __name__ == '__main__':
    main()