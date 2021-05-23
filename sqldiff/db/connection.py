from uuid import uuid4
from sqldiff.appdata import crud
from sqldiff.appdata import schemas
from sqldiff.db.connection_factory import connection_factories


class ConnectionApp:
    def __init__(self, connection_data: schemas.Connection):
        self.connection_data = connection_data
        self.ConnectionFactory = connection_factories[self.connection_data.driver.driver_type.name]
        self.connection = self.ConnectionFactory(self.connection_data).create_connection()


    def close(self):
        self.connection.close()


