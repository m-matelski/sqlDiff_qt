from abc import ABC, abstractmethod
from sqldiff.appdata import schemas
from sqldiff.appdata.url_template import JdbcUrlTemplate
from sqldiff.db.jdbc import connect
from sqldiff.db.driver_type import DriverType


class ConnectionFactory(ABC):
    @abstractmethod
    def create_connection(self):
        pass


class PostgresConnectionFactory(ConnectionFactory):
    def __init__(self, connection_data: schemas.Connection):
        self.connection_data = connection_data

    def create_connection(self):
        url_args = {
            'host': self.connection_data.host,
            'port': self.connection_data.port,
            'database': self.connection_data.database
        }
        url = JdbcUrlTemplate(self.connection_data.driver.url_template)
        url_str = url.feed(url_args)

        driver_args = {
            'user': self.connection_data.username,
            'password': self.connection_data.password
        }

        driver_files = [str(driver_file.file_path) for driver_file in self.connection_data.driver.driver_files]

        return connect(
            jclassname=self.connection_data.driver.jdbc_class_name,
            url=url_str,
            driver_args=driver_args,
            jars=driver_files
        )


connection_factories = {
    DriverType.POSTGRESLQ: PostgresConnectionFactory
}
