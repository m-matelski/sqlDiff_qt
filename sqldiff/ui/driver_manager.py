from PyQt5.QtWidgets import QWidget, QMessageBox
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from sqldiff.appdata.crud import get_drivers, delete_driver, get_driver_types

from sqldiff.ui.driver_form import DriverForm
from sqldiff.appdata import schemas

from sqldiff.appdata.dbconf import db_session
from sqldiff.ui.generic_listview_manager import ListViewManagerFactoryMethod, GenericListviewManagerWindow
from sqldiff.ui.messageboxes import ConfirmMessageBoxProvider
from sqldiff.ui.resources import DbIconsProvider


class DriverModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(DriverModel, self).__init__(*args, **kwargs)
        self.drivers = get_drivers()
        self.db_icons_provider = DbIconsProvider()

    def data(self, index, role=None):
        driver_name = self.drivers[index.row()].name
        driver_type_name = self.drivers[index.row()].driver_type.name
        driver_icon = self.db_icons_provider.get_icon_pixmap(name=driver_type_name, scaled_to_width=64)
        if role == Qt.DisplayRole:
            return driver_name

        if role == Qt.DecorationRole:
            return driver_icon

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.drivers)

    def refresh(self):
        self.drivers = get_drivers()

    def get_rows(self):
        return self.drivers


class DriverListViewManagerWindow(GenericListviewManagerWindow):
    def on_listview_selection_changed(self, current_selected_listview_item):
        """
        Override method to define action
        :param current_selected_listview_item:
        :return:
        """
        if current_selected_listview_item.is_predefined:
            self.deleteButton.setEnabled(False)
        else:
            self.deleteButton.setEnabled(True)


class DriverListViewManagerFactory(ListViewManagerFactoryMethod):

    def create_listview_manager_window(self) -> GenericListviewManagerWindow:
        model = DriverModel()
        delete_item_method = delete_driver
        ItemFormClass = DriverForm
        SchemaClass = schemas.BaseDriver
        confirm_delete_item_messagebox = ConfirmMessageBoxProvider(
            text='Delete driver?',
            title='Delete driver?',
            informative_text='Do You want to delete selected driver definition?'
        )

        driver_listview_window = DriverListViewManagerWindow(
            model=model,
            delete_item_method=delete_item_method,
            ItemFormClass=ItemFormClass,
            SchemaClass=SchemaClass,
            confirm_delete_item_messagebox=confirm_delete_item_messagebox
        )
        return driver_listview_window
