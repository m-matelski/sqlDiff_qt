from PyQt5.QtWidgets import QWidget
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import Qt

from sqldiff.ui.designer.ui_driver_manager import Ui_DriverManager

from sqldiff.appdata.managers import driver_manager
from sqldiff.appdata.persistence import PersistenceManager


class DriverModel(QtCore.QAbstractListModel):
    def __init__(self, driver_manager: PersistenceManager, *args, **kwargs):
        super(DriverModel, self).__init__(*args, **kwargs)
        self.driver_manager = driver_manager
        self.image = QtGui.QPixmap(":/resources_data/db_icon/postgres.png").scaledToWidth(64)

    def data(self, index, role=None):
        if role == Qt.DisplayRole:
            text = self.driver_manager[index.row()].driver_name
            return text

        if role == Qt.DecorationRole:
            # status, _ = self.driver_manager[index.row()]
            # if status:
            return self.image

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.driver_manager)


class DriverManager(QWidget, Ui_DriverManager):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
        self.model = DriverModel(driver_manager)
        self.listView.setModel(self.model)

