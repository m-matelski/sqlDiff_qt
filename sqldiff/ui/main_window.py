from PyQt5 import QtCore
from PyQt5.QtWidgets import QMainWindow

from sqldiff.ui.connection_manager import ConnectionListViewManagerFactory
from sqldiff.ui.designer.ui_main_window import Ui_MainWindow
from sqldiff.ui.driver_form import DriverForm
# from sqldiff.ui.driver_manager import DriverManager
from sqldiff.ui.driver_manager import DriverListViewManagerFactory


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.driver_manager_window = None
        self.connection_manager_window = None
        self.setup_actions()

    def setup_actions(self):
        self.actionDriverManager.triggered.connect(self.open_driver_manager_window)
        self.actionConnectionManager.triggered.connect(self.open_connection_manager_window)

    def open_driver_manager_window(self):
        self.driver_manager_window = DriverListViewManagerFactory().create_listview_manager_window()
        self.driver_manager_window.show()

    def open_connection_manager_window(self):
        self.connection_manager_window = ConnectionListViewManagerFactory().create_listview_manager_window()
        self.connection_manager_window.show()
