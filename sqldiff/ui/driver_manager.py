from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from sqldiff.ui.designer.ui_driver_manager import Ui_DriverManager

from sqldiff.appdata.persistence import PersistenceManager
from sqldiff.ui.driver_form import DriverForm


class DriverModel(QtCore.QAbstractListModel):
    def __init__(self, driver_manager: PersistenceManager, driver_type_manager: PersistenceManager, *args, **kwargs):
        super(DriverModel, self).__init__(*args, **kwargs)
        self.driver_manager = driver_manager
        self.driver_type_manager = driver_type_manager
        self.db_icons = {dt.name: QtGui.QPixmap(str(dt.icon_file_path)).scaledToWidth(64) for dt in driver_type_manager}

    def data(self, index, role=None):
        driver_name = self.driver_manager[index.row()].driver_type.name
        driver_icon = self.db_icons[driver_name]
        if role == Qt.DisplayRole:
            return driver_name

        if role == Qt.DecorationRole:
            return driver_icon

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.driver_manager)


class DriverManager(QWidget, Ui_DriverManager):
    def __init__(self, driver_manager, driver_type_manager, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        #
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.driver_from_window = None
        # Setup driver managers
        self.driver_manager = driver_manager
        self.driver_type_manager = driver_type_manager
        # Setup list view
        self.model = DriverModel(driver_manager, driver_type_manager)
        self.listView.setModel(self.model)
        self.listView.selectionModel().currentChanged.connect(self.driver_list_view_selection_changed)
        self.current_selected_driver_on_view = None
        # Setup button actions
        self.newButton.clicked.connect(self.new_driver)
        self.editButton.clicked.connect(self.edit_driver)
        self.deleteButton.clicked.connect(self.delete_driver)
        self.okButton.clicked.connect(self.save_changes)
        self.cancelButton.clicked.connect(self.discard_changes)

    def closeEvent(self, a0: QtGui.QCloseEvent) -> None:
        # print('close')
        pass

    def driver_list_view_selection_changed(self, indexes):
        self.current_selected_driver_on_view = self.driver_manager[indexes.row()]
        if self.current_selected_driver_on_view.is_predefined:
            self.deleteButton.setEnabled(False)
        else:
            self.deleteButton.setEnabled(True)

    def new_driver(self):
        self.open_driver_form()

    def edit_driver(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            driver = self.driver_manager[index]
            self.open_driver_form(driver)

    def delete_driver(self):
        pass

    def save_changes(self):
        pass

    def discard_changes(self):
        pass

    def open_driver_form(self, driver=None):
        # TODO pass self for handling callback, setup contract
        self.driver_from_window = DriverForm(self.driver_manager, self.driver_type_manager, driver,
                                             callback=self.driver_form_callback)
        self.driver_from_window.show()

    def driver_form_callback(self, driver):
        """
        Callback method called in Driver Form
        :param driver: Pass driver if new instance have been created in Driver Form. None otherwise
        """
        print('driver form callback')
        self.model.layoutChanged.emit()
        self.listView.clearSelection()
        # self.driver_from_window.close()
        # self.driver_from_window = None


