from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from sqldiff.ui.designer.ui_main_window import Ui_MainWindow
from sqldiff.ui.driver_form import DriverForm
from sqldiff.ui.driver_manager import DriverManager


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.driver_manager_window = None
        self.setup_actions()

    def setup_actions(self):
        self.actionDriverManager.triggered.connect(self.open_driver_manager_window)

    def open_driver_manager_window(self):
        self.driver_manager_window = DriverManager()
        self.driver_manager_window.show()
