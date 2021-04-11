from enum import Enum
from typing import List, Pattern, Optional, Any
from uuid import uuid4

from pydantic import Field, FilePath, constr, UUID4, SecretStr
from pydantic import BaseModel as PydanticBaseModel

from sqldiff.appdata.url_template import JdbcUrlTemplate


class DriverTypes(str, Enum):
    GENERIC = 'Generic'
    POSTGRES = 'PostgreSQL'
    TERADATA = 'Teradata'


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


################
# CONNECTIONS
################


class BaseConnection(BaseModel):
    host: str = Field(..., title='Host', description='Target database host address.')
    port: int = Field(..., title='Port', description='Database port')
    username: str = Field(..., title='Username', description='User name')
    password: SecretStr = Field(..., title='Password', description='TDatabase user password')

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value(),
        }


class SchemaConnection(BaseConnection):
    schema_name: Optional[str] = Field(..., title='Schema', description='Schema used in connection')


class DatabaseConnection(BaseConnection):
    database: Optional[str] = Field(..., title='Database', description='Database name to connect to')


class GenericConnection(SchemaConnection, DatabaseConnection):
    pass


#################
# DRIVERS
#################


class BaseDriver(BaseModel):
    # Predefined values
    id: UUID4 = Field(default_factory=uuid4)
    driver_name: str = Field(..., title='Driver Name', description='Unique driver definition name.')
    driver_type: DriverTypes = Field(..., title='Driver Type', description='Database driver type.')
    jdbc_class_name: str = Field(..., title='JDBC class name',
                                 description='JDBC class name in attached driver *.jar file.')
    url_template: str = Field(..., title='JDBC URL template')
    default_port: Optional[int] = Field(..., title='Port', description='Default database connection port.')
    # will cause the input value to be passed to re.compile(v) to create a regex
    expected_driver_files: List[Pattern] = Field(..., title='Expected driver files',
                                                 description='List of expected file names regexp.')
    is_predefined: bool = Field(default=True, title='Is Predefined', description='Is predefined by application')

    driver_files: List[FilePath] = Field(..., title='List of paths to JDBC *.jar files')


#################
# PERSISTENCE
#################

class PersistenceModel(BaseModel):
    """
    Persistence Model is used to store multiple records of pydantic type defined in "data" field.
    Additional metadata for persistence can be added.
    """
    # Custom Root Type. Overwrite root field in subclass.
    data: List[PydanticBaseModel]

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    def append(self, item):
        self.data.append(item)


class DriverPersistence(PersistenceModel):
    data: List[BaseDriver]

