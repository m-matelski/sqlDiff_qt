from collections import namedtuple
from dataclasses import dataclass
from enum import Enum
from functools import lru_cache, cached_property
from pathlib import Path
from typing import List
from sqldiff.appdata import models, schemas


from PyQt5 import QtCore, QtGui
from PyQt5.QtWidgets import QWidget, QFileDialog, QStyle, QMessageBox

from sqldiff.appdata import schemas
from sqldiff.appdata.crud import get_driver_type_by_name, get_driver_types, upsert_driver
from sqldiff.appdata.path import ResourcePaths

from sqldiff.ui.designer.ui_driver_form import Ui_DriverForm
from PyQt5.QtCore import Qt

generic_driver_type = 'Generic'


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

    def __init__(self, driver: schemas.BaseDriver, style: QStyle, *args, **kwargs):
        super(PathModel, self).__init__(*args, **kwargs)
        self.driver = driver
        self.style = style
        self.data_records: List[PathRecord] = []
        self.jar_icon = QtGui.QIcon(str(ResourcePaths.JAR_ICON))
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
            match = any([e.file_regex.match(str(driver_file)) for e in self.driver.expected_driver_files])
            status = PathStatus.SATISFIED if match else PathStatus.UNEXPECTED
            files.append(PathRecord(pattern=str(driver_file.file_path), status=status, type=PatternType.PATH))

        expected_files = []
        for expected_file in self.driver.expected_driver_files:
            match = any([expected_file.file_regex.match(str(f)) for f in self.driver.driver_files])
            if not match:
                expected_files.append(
                    PathRecord(pattern=str(expected_file.file_regex), status=PathStatus.MISSING, type=PatternType.PATTERN))

        self.data_records = files + expected_files
        return self.data_records


class DriverForm(QWidget, Ui_DriverForm):
    def __init__(self, driver: schemas.BaseDriver = None, callback=None, *args, **kwargs):
        """
        Driver Form init.
        :param driver: driver instance to edit in form. If None - new driver will be created
        :param callback: Callback function instance. Will be called on close. Driver can be passed back
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
            self.driver = schemas.BaseDriver.construct(
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

        self.callback = callback

        # Get db logo images
        self.db_logo = None

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
        path_raw, _ = QFileDialog.getOpenFileName(self, "Add JDBC *.jar file", "", "JAR files (*.jar);; all (*.*)")
        if path_raw:
            path = Path(path_raw)
            if path not in self.driver.driver_files:
                driver_file = schemas.DriverFile(
                    file_path=path,
                    driver_id=self.driver.id
                )
                # add_driver_file_path(self.driver, driver_file)
                self.driver.driver_files.append(driver_file)
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
            driver_file = None
            for f in self.driver.driver_files:
                if f.file_path == path:
                    driver_file = f
                    break
            if driver_file in self.driver.driver_files:
                self.driver.driver_files.remove(driver_file)
            self.model.refresh_data()
            self.model.layoutChanged.emit()
            self.listView.clearSelection()

    def save_changes_and_close(self):
        try:
            new_driver = self.model_from_form()
            upsert_driver(new_driver)
            self.modified = False
            callback_driver = new_driver if self.new_driver else None
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
        self.driverNameLineEdit.setText(self.driver.name)
        self.urlTemplateLineEdit.setText(self.driver.url_template)
        self.labelDriverName.setText(self.driver.name)

    def get_driver_type_from_combobox(self):
        # get driver type record based on text in combobox
        driver_type_model_instance = get_driver_type_by_name(name=self.driverTypeComboBox.currentText())
        driver_type = schemas.DriverType.from_orm(driver_type_model_instance)
        return driver_type

    def model_from_form(self):
        driver_files = self.driver.driver_files
        # listview_paths = [i for i in self.model.data_records if i.type == PatternType.PATH]
        # for p in listview_paths:
        #     path = Path(p.pattern)
        #     if not any(path in df.file_path for df in self.driver.driver_files):
        #         driver_files.append(
        #             schemas.DriverFile(
        #                 file_path=Path(path),
        #                 driver_id=self.driver.id
        #             )
        #         )
        # [Path(i.pattern) for i in self.model.data_records if i.type == PatternType.PATH],
        # get_driver_type_by_name
        form_dict = {
            'name': self.driverNameLineEdit.text(),
            'driver_type': self.get_driver_type_from_combobox(),
            'jdbc_class_name': self.driverClassNameLineEdit.text(),
            'url_template': self.urlTemplateLineEdit.text(),
            'default_port': self.defaultPortLineEdit.text(),
            'driver_files': driver_files,

        }
        driver = schemas.BaseDriver(
            id=self.driver.id,
            expected_driver_files=self.driver.expected_driver_files,
            is_predefined=self.driver.is_predefined,
            **form_dict
        )
        return driver

    def setup_driver_type_combobox(self):
        driver_types = get_driver_types()
        for driver_type in driver_types:
            self.driverTypeComboBox.addItem(driver_type.name)
        if self.driver is not None:
            self.driverTypeComboBox.setCurrentText(self.driver.driver_type.name)
        else:
            self.driverTypeComboBox.setCurrentText('Generic JDBC Driver')

    def setup_driver_logo(self):

        logo_path = None
        if self.driver is not None:
            logo_path = self.driver.driver_type.logo_file_path
        else:
            logo_path = ResourcePaths.DB_LOGO_GENERIC
        self.db_logo = QtGui.QPixmap(str(logo_path))
        self.labelDriverLogo.setPixmap(self.db_logo)

    def disable_components_for_predefined_driver(self):
        """Make line edits read only for predefined driver"""
        self.defaultPortLineEdit.setEnabled(False)
        self.driverClassNameLineEdit.setEnabled(False)
        self.driverNameLineEdit.setEnabled(False)
        self.urlTemplateLineEdit.setEnabled(False)
        self.labelDriverName.setEnabled(False)
        self.driverTypeComboBox.setEnabled(False)
