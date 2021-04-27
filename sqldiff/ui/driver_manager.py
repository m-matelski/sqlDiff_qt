from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from sqldiff.appdata.crud import get_drivers, delete_drivers, delete_driver
from sqldiff.ui.designer.ui_driver_manager import Ui_DriverManager

from sqldiff.ui.driver_form import DriverForm
from sqldiff.appdata import schemas

from sqldiff.appdata.dbconf import db


class DriverModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(DriverModel, self).__init__(*args, **kwargs)
        self.drivers = get_drivers()
        self.db_icons = {
            d.driver_type.name: QtGui.QPixmap(str(d.driver_type.icon_file_path)).scaledToWidth(64) for d in self.drivers
        }

    def data(self, index, role=None):
        driver_name = self.drivers[index.row()].name
        driver_type_name = self.drivers[index.row()].driver_type.name
        driver_icon = self.db_icons[driver_type_name]
        if role == Qt.DisplayRole:
            return driver_name

        if role == Qt.DecorationRole:
            return driver_icon

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.drivers)

    def refresh(self):
        self.drivers = get_drivers()


class DriverManager(QWidget, Ui_DriverManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        #
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.driver_from_window = None
        # Setup list view
        self.drivers = get_drivers()
        self.model = DriverModel()
        self.listView.setModel(self.model)
        self.listView.selectionModel().currentChanged.connect(self.driver_list_view_selection_changed)
        self.current_selected_driver_on_view = None
        # Setup button actions
        self.newButton.clicked.connect(self.new_driver)
        self.editButton.clicked.connect(self.edit_driver)
        self.deleteButton.clicked.connect(self.delete_driver)
        self.okButton.clicked.connect(self.save_changes)
        self.cancelButton.clicked.connect(self.close)

        #
        self.drivers_to_remove = []
        self.modified = False

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.accept()

    def save_changes(self):
        delete_drivers(self.drivers_to_remove)
        self.modified = False
        # callback()
        self.close()

    def driver_list_view_selection_changed(self, indexes):
        self.current_selected_driver_on_view = self.model.drivers[indexes.row()]
        if self.current_selected_driver_on_view.is_predefined:
            self.deleteButton.setEnabled(False)
        else:
            self.deleteButton.setEnabled(True)

    def get_selected_driver_index(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            return index

    def get_selected_driver(self):
        index = self.get_selected_driver_index()
        if index:
            return self.model.drivers[index]

    def new_driver(self):
        self.open_driver_form()

    def edit_driver(self):
        driver = self.get_selected_driver()
        if driver:
            driver_schema = schemas.BaseDriver.from_orm(driver)
            self.open_driver_form(driver_schema)

    def delete_driver(self):
        driver = self.get_selected_driver()
        if driver:
            delete_driver(driver)
            self.model.refresh()
            self.model.layoutChanged.emit()
            self.listView.clearSelection()

    def open_driver_form(self, driver=None):
        self.driver_from_window = DriverForm(driver, callback=self.driver_form_callback)
        self.driver_from_window.show()

    def driver_form_callback(self, driver):
        """
        Callback method called in Driver Form
        :param driver: Pass driver if new instance have been created in Driver Form. None otherwise
        """
        self.model.refresh()
        self.model.layoutChanged.emit()
        self.listView.clearSelection()
        # self.driver_from_window.close()
        # self.driver_from_window = None
