from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache, cached_property
from pathlib import Path
from typing import List

from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog, QStyle, QMessageBox

from sqldiff.appdata.managers import driver_type_manager
from sqldiff.appdata.models import BaseDriver
from sqldiff.appdata.path import Resources
from sqldiff.appdata.persistence import PersistenceManager
from sqldiff.ui.designer.ui_driver_form import Ui_DriverForm
from PyQt5.QtCore import Qt

generic_driver_type = driver_type_manager.get_by_key(name='Generic')


class PathStatus(str, Enum):
    """Path status related to expected *.jar files regexps"""
    SATISFIED = 'Satisfied'
    MISSING = 'Missing'
    UNEXPECTED = 'Not defined'


class PatternType(str, Enum):
    PATH = 'Path'
    PATTERN = 'Pattern'


@dataclass
class PathRecord:
    """Path record used as a model for ListView with *.jar file paths"""
    pattern: str
    status: PathStatus
    type: PatternType


class PathModel(QtCore.QAbstractListModel):
    """
    Model for Driver Files list view in Driver form.
    It returns list of paths to JDBC jar files,
    and list of expected jar files regexp if no added file satisfy defined regexp
    """

    def __init__(self, driver: BaseDriver, style: QStyle, *args, **kwargs):
        super(PathModel, self).__init__(*args, **kwargs)
        self.driver = driver
        self.style = style
        self.data_records: List[PathRecord] = []
        self.jar_icon = QtGui.QIcon(str(Resources.JAR_ICON))
        self.refresh_data()

    def data(self, index, role=None):
        idx = index.row()
        record = self.data_records[idx]

        # Handle display role
        if role == Qt.DisplayRole:
            return record.pattern

        row_style = self.predefined_driver_styles if self.driver.is_predefined else self.custom_driver_styles
        try:
            return row_style[record.status][role]
        except KeyError:
            pass

    @cached_property
    def predefined_driver_styles(self):
        """
        Set of list view styling values for predefined drivers.
        """
        d = {
            PathStatus.SATISFIED: {
                Qt.DecorationRole: self.style.standardIcon(QStyle.SP_DialogApplyButton),
                QtCore.Qt.TextColorRole: None,
                QtCore.Qt.ToolTipRole: "Selected JAR matches expected file criteria."
            },
            PathStatus.UNEXPECTED: {
                Qt.DecorationRole: self.style.standardIcon(QStyle.SP_MessageBoxInformation),
                QtCore.Qt.TextColorRole: None,
                QtCore.Qt.ToolTipRole: "Picked unexpected driver file."
            },
            PathStatus.MISSING: {
                Qt.DecorationRole: self.style.standardIcon(QStyle.SP_MessageBoxQuestion),
                QtCore.Qt.TextColorRole: QtGui.QColor("#c91818"),
                QtCore.Qt.ToolTipRole: "Driver file not defined."
            }
        }
        return d

    @cached_property
    def custom_driver_styles(self):
        """
        Set of list view styling values for new drivers.
        New drivers dont have list with expected *.jar files,
        so user's chosen path to *.jar won't be matched with any regexp
        """
        d = {
            PathStatus.UNEXPECTED: {
                Qt.DecorationRole: self.style.standardIcon(QStyle.SP_DialogApplyButton),
                QtCore.Qt.TextColorRole: None,
                QtCore.Qt.ToolTipRole: "Chosen driver file."
            },
        }
        return d

    def rowCount(self, parent=None, *args, **kwargs):
        return len(self.data_records)

    def refresh_data(self):
        """
        Store expected files (regexps) and user's chosen files in one list.
        """
        if not self.driver:
            return []

        files = []
        for driver_file in self.driver.driver_files:
            match = any([e.match(str(driver_file)) for e in self.driver.expected_driver_files])
            status = PathStatus.SATISFIED if match else PathStatus.UNEXPECTED
            files.append(PathRecord(pattern=str(driver_file), status=status, type=PatternType.PATH))

        expected_files = []
        for expected_file in self.driver.expected_driver_files:
            match = any([expected_file.match(str(f)) for f in self.driver.driver_files])
            if not match:
                expected_files.append(
                    PathRecord(pattern=expected_file.pattern, status=PathStatus.MISSING, type=PatternType.PATTERN))

        self.data_records = files + expected_files
        return self.data_records


class DriverForm(QWidget, Ui_DriverForm):
    def __init__(self, driver_manager, driver_type_manager, driver: BaseDriver = None, callback=None, *args, **kwargs):
        """
        Driver Form init.
        :param driver_manager: Driver JSON Persistence manager
        :param driver_type_manager: Driver Type JSON Persistence manager
        :param driver: driver instance to edit in form. If None - new driver will be created
        :param callback: Driver Manager callback function instance. Will be called on close.
        :param args: args
        :param kwargs: kwargs
        """
        super().__init__(*args, **kwargs)

        # call setupUi method from compiled ui file
        self.setupUi(self)

        # set window to modal mode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        if driver:
            # Assign driver instance if driver have been sent for edit
            self.driver = driver
            self.new_driver = False
        else:
            # Create new driver instance
            self.driver = BaseDriver.construct(
                driver_name='NewDriver',
                driver_type=generic_driver_type,
                jdbc_class_name='',
                url_template='',
                default_port='',
                expected_driver_files=[],
                is_predefined=False,
                driver_files=[]
            )
            self.new_driver = True

        self.driver_manager = driver_manager
        self.driver_type_manager = driver_type_manager
        self.callback = callback

        # Get db logo images
        self.db_logos = {dt.name: QtGui.QPixmap(str(dt.logo_file_path)) for dt in driver_type_manager}

        # If driver have been modified
        self.modified = True

        # setup form
        self.setup_form()
        # Setup list view
        self.model = PathModel(self.driver, self.style())
        self.listView.setModel(self.model)

        # setup buttons
        self.addPathButton.clicked.connect(self.add_path)
        self.removeButton.clicked.connect(self.remove_path)
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.save_changes_and_close)

        print(f"driver form instance id = {id(self)}")

    def add_path(self):
        """Open file dialog window and add chosen *.jar path to driver."""
        path_raw, _ = QFileDialog.getOpenFileName(self, "Add JDBC *.jar file", "", "JAR files (*.jar)")
        if path_raw:
            pass
            path = Path(path_raw)
            if path not in self.driver.driver_files:
                self.driver.driver_files.append(path)
            else:
                QMessageBox.information(self, "Path already defined.", "Path already defined.").show()
        self.model.refresh_data()
        self.model.layoutChanged.emit()

    def remove_path(self):
        """Remove driver *.jar path from driver settings."""
        indexes = self.listView.selectedIndexes()
        if indexes:
            index = indexes[0].row()
            path = Path(self.model.data_records[index].pattern)
            if path in self.driver.driver_files:
                self.driver.driver_files.remove(path)
            self.model.refresh_data()
            self.model.layoutChanged.emit()
            self.listView.clearSelection()

    def save_changes_and_close(self):
        try:
            new_driver = self.model_from_form()
            self.driver_manager.upsert(new_driver)
            self.modified = False
            callback_driver = new_driver if self.new_driver else None
            self.driver_manager.commit()
            self.callback(callback_driver)
            self.close()

        except ValueError as e:
            QMessageBox.critical(self, "Invalid driver data.", str(e))

    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.modified:
            msg = QMessageBox(
                icon=QMessageBox.Information,
                text='Driver settings have been modified.',
                parent=self,
            )
            msg.setWindowTitle('Changes detected.')
            msg.setInformativeText('Do You want to discard changes and exit?')
            msg.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
            msg.setDefaultButton(QMessageBox.Cancel)
            button = msg.exec_()
            if button == QMessageBox.Discard:
                self.driver_manager.rollback()
                self.callback(None)
                event.accept()

            else:
                event.ignore()

    def setup_form(self):
        self.setup_driver_type_combobox()
        self.setup_driver_logo()
        if self.driver is not None:
            self.populate_form()
            if self.driver.is_predefined:
                self.disable_components_for_predefined_driver()
        else:
            self.labelDriverName.setText('Generic JDBC Driver')

    def populate_form(self):
        self.defaultPortLineEdit.setText(str(self.driver.default_port))
        self.driverClassNameLineEdit.setText(self.driver.jdbc_class_name)
        self.driverNameLineEdit.setText(self.driver.driver_name)
        self.urlTemplateLineEdit.setText(self.driver.url_template)
        self.labelDriverName.setText(self.driver.driver_name)

    def model_from_form(self):
        form_dict = {
            'driver_name': self.driverNameLineEdit.text(),
            'driver_type': self.driver_type_manager.get_by_key(name=self.driverTypeComboBox.currentText()),
            'jdbc_class_name': self.driverClassNameLineEdit.text(),
            'url_template': self.urlTemplateLineEdit.text(),
            'default_port': self.defaultPortLineEdit.text(),
            'driver_files': [Path(i.pattern) for i in self.model.data_records if i.type == PatternType.PATH],

        }
        driver = BaseDriver.construct(
            id=self.driver.id,
            expected_driver_files=self.driver.expected_driver_files,
            is_predefined=self.driver.is_predefined,
            **form_dict
        )
        return driver

    def setup_driver_type_combobox(self):
        for driver_type in self.driver_type_manager:
            self.driverTypeComboBox.addItem(driver_type.name)
        if self.driver is not None:
            self.driverTypeComboBox.setCurrentText(self.driver.driver_type.name)
        else:
            self.driverTypeComboBox.setCurrentText(self.driver_type_manager.get_by_key(name='Generic').name)

    def setup_driver_logo(self):
        if self.driver is not None:
            self.labelDriverLogo.setPixmap(self.db_logos[self.driver.driver_type.name])
        else:
            generic_db_logo = self.db_logos[self.driver_type_manager.get_by_key(name='Generic').name]
            self.labelDriverLogo.setPixmap(generic_db_logo)

    def disable_components_for_predefined_driver(self):
        """Make line edits read only for predefined driver"""
        self.defaultPortLineEdit.setEnabled(False)
        self.driverClassNameLineEdit.setEnabled(False)
        self.driverNameLineEdit.setEnabled(False)
        self.urlTemplateLineEdit.setEnabled(False)
        self.labelDriverName.setEnabled(False)
        self.driverTypeComboBox.setEnabled(False)
