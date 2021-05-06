from PyQt5 import QtCore
from PyQt5.QtCore import Qt

from sqldiff.appdata import schemas
from sqldiff.appdata.crud import get_connections, get_driver_type_by_connection, delete_connection
from sqldiff.ui.connection_basic_form import ConnectionBasicForm
from sqldiff.ui.driver_selector import DriverSelector
from sqldiff.ui.generic_listview_manager import GenericListviewManagerWindow, ListViewManagerFactoryMethod
from sqldiff.ui.messageboxes import ConfirmMessageBoxProvider
from sqldiff.ui.resources import DbIconsProvider


class ConnectionModel(QtCore.QAbstractListModel):
    def __init__(self, *args, **kwargs):
        super(ConnectionModel, self).__init__(*args, **kwargs)
        self.connections = get_connections()
        self.db_icons_provider = DbIconsProvider()

    def data(self, index, role=None):
        connection = self.connections[index.row()]
        connection_driver_type = get_driver_type_by_connection(connection)
        connection_driver_icon = self.db_icons_provider.get_icon(name=connection_driver_type.name)

        if role == Qt.DisplayRole:
            return connection.name

        if role == Qt.DecorationRole:
            return connection_driver_icon

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.connections)

    def refresh(self):
        self.connections = get_connections()

    def get_rows(self):
        return self.connections


class ConnectionListViewManagerWindow(GenericListviewManagerWindow):
    def __init__(self,
                 model: QtCore.QAbstractListModel,
                 delete_item_method,
                 ItemFormClass,
                 DriverSelectorClass,
                 SchemaClass,
                 confirm_delete_item_messagebox: ConfirmMessageBoxProvider,
                 *args, **kwargs):
        super().__init__(model,
                         delete_item_method,
                         ItemFormClass,
                         SchemaClass,
                         confirm_delete_item_messagebox,
                         *args, **kwargs)

        self.DriverSelectorClass = DriverSelectorClass

    def driver_selector_callback(self, driver):
        if driver:
            self.open_item_form(item=driver)

    def open_driver_selector(self):
        self.item_form_window = self.DriverSelectorClass(callback=self.driver_selector_callback)
        self.item_form_window.show()

    def open_item_form(self, item=None):
        if item:
            super().open_item_form(item=item)
        else:
            self.open_driver_selector()


class ConnectionListViewManagerFactory(ListViewManagerFactoryMethod):

    def create_listview_manager_window(self) -> GenericListviewManagerWindow:
        model = ConnectionModel()
        delete_item_method = delete_connection
        ItemFormClass = ConnectionBasicForm
        DriverSelectorClass = DriverSelector
        SchemaClass = schemas.Connection
        confirm_delete_item_messagebox = ConfirmMessageBoxProvider(
            text='Delete connection?',
            title='Delete connection?',
            informative_text='Do You want to delete selected connection definition?'
        )

        connection_listview_window = ConnectionListViewManagerWindow(
            model=model,
            delete_item_method=delete_item_method,
            ItemFormClass=ItemFormClass,
            DriverSelectorClass=DriverSelectorClass,
            SchemaClass=SchemaClass,
            confirm_delete_item_messagebox=confirm_delete_item_messagebox
        )
        return connection_listview_window
