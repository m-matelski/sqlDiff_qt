from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore

from sqldiff.appdata import schemas
from sqldiff.ui.designer.ui_driver_selector import Ui_DriverSelector
from sqldiff.ui.widgets.predesigned.driver_manager import DriverModel
from sqldiff.ui.widgets.predesigned.generic_listview_manager import SelectableListViewMixin


class DriverSelector(QWidget, Ui_DriverSelector, SelectableListViewMixin):
    def __init__(self, callback=None, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # call setupUi method from compiled ui file
        self.setupUi(self)
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.model = DriverModel()
        self.listView.setModel(self.model)
        self.callback = callback

        self.cancelButton.clicked.connect(self.close)
        self.nextButton.clicked.connect(self.choose_driver)

    def choose_driver(self):
        driver = self.get_selected_item()
        if driver:
            driver_schema = schemas.BaseDriver.from_orm(driver)
            self.callback(driver_schema)
