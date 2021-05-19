from PyQt5 import QtGui
from PyQt5.QtWidgets import QMainWindow

from sqldiff.ui.connection_manager import ConnectionListViewManagerFactory
from sqldiff.ui.designer.ui_main_window import Ui_MainWindow
# from sqldiff.ui.driver_manager import DriverManager
from sqldiff.ui.driver_manager import DriverListViewManagerFactory
from sqldiff.ui.widgets.editor.sql_editor import SqlEditorWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.show()
        self.driver_manager_window = None
        self.connection_manager_window = None
        self.setup_actions()

        self.sqlEditorTabWidget.tabCloseRequested.connect(self.close_sql_editor_tab)

    def setup_actions(self):
        self.actionDriverManager.triggered.connect(self.open_driver_manager_window)
        self.actionConnectionManager.triggered.connect(self.open_connection_manager_window)

        self.actionNewSqlEditor.triggered.connect(self.create_new_sql_editor)

    def open_driver_manager_window(self):
        self.driver_manager_window = DriverListViewManagerFactory().create_listview_manager_window()
        self.driver_manager_window.show()

    def open_connection_manager_window(self):
        self.connection_manager_window = ConnectionListViewManagerFactory().create_listview_manager_window()
        self.connection_manager_window.show()

    def create_new_sql_editor(self):
        editor = SqlEditorWidget()
        icon = QtGui.QIcon(':/resources_data/app_icon/sql_new.svg')
        self.sqlEditorTabWidget.addTab(editor, icon, 'labl1')

    def close_sql_editor_tab(self, idx):
        self.sqlEditorTabWidget.removeTab(idx)




