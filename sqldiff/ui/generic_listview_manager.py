from abc import abstractmethod, ABC

from PyQt5 import QtGui
from PyQt5.QtWidgets import QWidget, QMessageBox

from sqldiff.ui.designer.ui_generic_crud_listview_manager import Ui_GenericLisviewItemManager
from PyQt5 import QtCore

from sqldiff.ui.messageboxes import ConfirmMessageBoxProvider


class SelectableListViewMixin:
    """
    Mixin class for handling listView item selection using model.
    This mixin assumes that below fields are available in subclass:
    listView: Qt List View component
    model: Qt abstract model connected with ListView
    """
    def get_selected_item_index(self):
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            return index

    def get_selected_item(self):
        index = self.get_selected_item_index()
        if index is not None:
            return self.model.get_rows()[index]


class GenericListviewManagerWindow(QWidget, Ui_GenericLisviewItemManager, SelectableListViewMixin):
    """
    Defines generic window with ListView component that allows to manage CRUD operations on items on ListView.
    This view is able to show and manage different models.
    Editing model opens Specified entity form.
    """

    def __init__(self,
                 window_title,
                 model: QtCore.QAbstractListModel,
                 delete_item_method,
                 ItemFormClass,
                 SchemaClass,
                 confirm_delete_item_messagebox: ConfirmMessageBoxProvider,
                 *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        #
        self.setWindowModality(QtCore.Qt.ApplicationModal)
        self.item_form_window = None
        self.setWindowTitle(window_title)

        # Setup list view
        self.model = model
        self.listView.setModel(self.model)
        self.listView.selectionModel().currentChanged.connect(self.listview_selection_changed)
        self.current_selected_listview_item = None

        self.delete_item_method = delete_item_method
        self.ItemFormClass = ItemFormClass

        self.SchemaClass = SchemaClass

        self.confirm_delete_item_messagebox = confirm_delete_item_messagebox
        # Setup button actions
        self.newButton.clicked.connect(self.new_item)
        self.editButton.clicked.connect(self.edit_item)
        self.deleteButton.clicked.connect(self.delete_item)
        self.okButton.clicked.connect(self.save_changes)

        #
        self.modified = False

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        event.accept()

    def save_changes(self):
        self.modified = False
        # callback()
        self.close()

    def new_item(self):
        self.open_item_form()

    def edit_item(self):
        item = self.get_selected_item()
        if item:
            driver_schema = self.SchemaClass.from_orm(item)
            self.open_item_form(driver_schema)

    def delete_item(self):
        item = self.get_selected_item()
        if item:
            response_button = self.confirm_delete_item()
            if response_button == QMessageBox.Yes:
                self.delete_item_method(item)
                self.refresh_list_view()

    def open_item_form(self, item=None):
        self.item_form_window = self.ItemFormClass(item, callback=self.item_form_callback)
        self.item_form_window.show()

    def confirm_delete_item(self):
        return self.confirm_delete_item_messagebox.build(self)

    def refresh_list_view(self):
        self.model.refresh()
        self.model.layoutChanged.emit()
        self.listView.clearSelection()

    def item_form_callback(self, driver):
        """
        Callback method called in Driver Form
        :param driver: Pass driver if new instance have been created in Driver Form. None otherwise
        """
        self.refresh_list_view()

    def listview_selection_changed(self, indexes):
        """
        Executed every time selected item on a listview changed.
        Updates current selected item and calls on listview selection changed event.
        :param indexes: received from listview qt signal
        :return:
        """
        self.current_selected_listview_item = self.model.get_rows()[indexes.row()]
        self.on_listview_selection_changed(self.current_selected_listview_item)

    def on_listview_selection_changed(self, current_selected_listview_item):
        """
        Override method to define action
        :param current_selected_listview_item:
        :return:
        """
        pass


class ListViewManagerFactoryMethod(ABC):
    """
    Factory method for GenericListviewManagerWindow creation.
    """

    @abstractmethod
    def create_listview_manager_window(self) -> GenericListviewManagerWindow:
        """
        Define steps to build and create GenericListviewManagerWindow object
        :return: GenericListviewManagerWindow window or subclasses
        """
        pass
