from typing import Union
from uuid import uuid4

from PyQt5.QtGui import QIntValidator
from PyQt5.QtWidgets import QWidget, QMessageBox
from pydantic import ValidationError
from sqlalchemy.exc import IntegrityError

from sqldiff.appdata import schemas
from sqldiff.appdata.crud import upsert_connection
from sqldiff.appdata.dbconf import db_session
from sqldiff.db.connection import ConnectionApp
from sqldiff.ui.designer.ui_connection_basic_form import Ui_ConnectionBasicForm
from PyQt5 import QtCore, QtGui

from sqldiff.ui.utils.messageboxes import SaveChangesMessageBoxProvider
from sqldiff.ui.utils.resources import DbIconsProvider


class ConnectionBasicForm(QWidget, Ui_ConnectionBasicForm):
    def __init__(self, connection: Union[schemas.BaseDriver, schemas.Connection], callback=None, *args, **kwargs):
        """
        Connection Basic Form init.
        :param connection: connection instance to edit in form. If connection is DriverType -
            new connection of that type will be created
        :param callback: Callback function instance. Will be called on close. Connection can be passed back.
        """
        super().__init__(*args, **kwargs)

        self.new_driver = False
        if isinstance(connection, schemas.BaseDriver):
            self.connection_driver = connection
            self.connection = None
            self.new_driver = True
        elif isinstance(connection, schemas.Connection):
            self.connection_driver = connection.driver
            self.connection = connection
        else:
            raise RuntimeError('connection type should be type of DriverType or Connection.')

        # call setupUi method from compiled ui file
        self.setupUi(self)
        # set window to modal mode
        self.setWindowModality(QtCore.Qt.ApplicationModal)

        self.callback = callback

        # Get db logo images
        self.db_icons_provider = DbIconsProvider()
        self.driver_type = self.connection_driver.driver_type
        self.db_logo = self.db_icons_provider.get_logo(self.driver_type.name)
        self.labelDriverLogo.setPixmap(self.db_logo)

        # If driver have been modified
        self.modified = True

        self.setup_form()

        self.portLineEdit.setValidator(QIntValidator(0, 65535, self))

        self.testConnectionButton.clicked.connect(self.test_connection)
        self.cancelButton.clicked.connect(self.close)
        self.okButton.clicked.connect(self.save_changes_and_close)

    def test_connection(self):
        try:
            self.read_form()
            self.connection.password = self.passwordLineEdit.text()
            connection = ConnectionApp(self.connection)
            connection.close()
            print(f'test_connection using:{self.connection}')
        except ValidationError as e:
            QMessageBox.critical(self, "Invalid connection data.", str(e))
            return
        except Exception as e:
            QMessageBox.critical(self, "Error while connecting.", str(e))
            return
        QMessageBox.information(self, "Success!", "Connected successfully!")


    def closeEvent(self, event: QtGui.QCloseEvent) -> None:
        if self.modified:
            button = SaveChangesMessageBoxProvider(text='Connection settings have been modified.').build(self)
            if button == QMessageBox.Discard:
                event.accept()
            else:
                event.ignore()

    def save_changes_and_close(self):
        try:
            self.read_form()
            self.modified = False
            print(f'save changes using: {self.connection}')
            upsert_connection(self.connection)
            self.close()
            self.callback(self.connection)
        except ValidationError as e:
            QMessageBox.critical(self, "Invalid connection data.", str(e))

        except IntegrityError as e:
            db_session.rollback()
            QMessageBox.critical(self, "Invalid connection data.",
                                 "Connection with that name already exists. Please change connection name.")

    def setup_form(self):
        self.labelDriverName.setText(
            f"Driver: {self.connection_driver.name} [{self.connection_driver.driver_type.name} JDBC Driver]")
        if self.connection:
            self.load_form()

    def load_form(self):
        self.nameLineEdit.setText(self.connection.name)
        self.hostLineEdit.setText(self.connection.host)
        self.portLineEdit.setText(str(self.connection.port))
        self.databaseLineEdit.setText(self.connection.database)
        self.schemaLineEdit.setText(self.connection.schema_name)
        self.userLineEdit.setText(self.connection.username)
        if self.connection.password:
            self.passwordLineEdit.setText(self.connection.password)
            self.savePasswordCheckBox.setCheckState(True)

    def get_connection_id(self):
        if self.connection:
            connection_id = self.connection.id
        else:
            connection_id = uuid4()
        return connection_id

    def get_password_from_form(self):
        if self.savePasswordCheckBox.checkState():
            return self.passwordLineEdit.text()
        return None


    def read_form(self):
        connection = schemas.Connection(
            id=self.get_connection_id(),
            name=self.nameLineEdit.text() or None,
            host=self.hostLineEdit.text() or None,
            port=self.portLineEdit.text() or None,
            database=self.databaseLineEdit.text() or None,
            schema_name=self.schemaLineEdit.text() or None,
            username=self.userLineEdit.text() or None,
            password=self.get_password_from_form() or None,
            driver=self.connection_driver

        )
        self.connection = connection
