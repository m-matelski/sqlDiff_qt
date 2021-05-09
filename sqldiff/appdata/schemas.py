from enum import Enum
from typing import List, Pattern, Optional, Any
from uuid import uuid4

from pydantic import Field, FilePath, constr, UUID4, SecretStr
from pydantic import BaseModel as PydanticBaseModel
from pathlib import Path


class BaseModel(PydanticBaseModel):
    class Config:
        arbitrary_types_allowed = True


#################
# DRIVERS
#################

class DriverType(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    name: str = Field(..., title='Driver type name', description='Database driver type name.')
    icon_file_path: Path = Field(..., description='Image file name of database icon in qt resources')
    logo_file_path: Path = Field(..., description='Image file name of database logo in qt resources')

    class Config:
        orm_mode = True


class ExpectedDriverFile(BaseModel):
    id: UUID4 = Field(default_factory=uuid4)
    file_regex: Pattern = Field(..., title='Expected driver files',
                                description='expected file name regexp.')
    driver_id: UUID4

    class Config:
        orm_mode = True


class DriverFileCreate(BaseModel):
    file_path: FilePath = Field(..., title='List of paths to JDBC *.jar files')

    class Config:
        json_encoders = {
            FilePath: lambda v: str(v),
        }


class DriverFile(DriverFileCreate):
    id: UUID4 = Field(default_factory=uuid4)
    driver_id: UUID4

    class Config:
        orm_mode = True


class DriverCreate(BaseModel):
    name: str = Field(..., title='Driver Name', description='Unique driver definition name.')
    jdbc_class_name: str = Field(..., title='JDBC class name',
                                 description='JDBC class name in attached driver *.jar file.')
    url_template: str = Field(..., title='JDBC URL template')
    default_port: Optional[int] = Field(..., title='Port', description='Default database connection port.')
    is_predefined: bool = Field(default=True, title='Is Predefined', description='Is predefined by application')


class BaseDriver(DriverCreate):
    # Predefined values
    id: UUID4 = Field(default_factory=uuid4)

    driver_type: DriverType = Field(..., title='Driver Type', description='Database driver type.')
    # will cause the input value to be passed to re.compile(v) to create a regex
    expected_driver_files: List[ExpectedDriverFile] = Field(..., title='Expected driver files',
                                                            description='List of expected file names regexp.')
    driver_files: List[DriverFile] = Field(..., title='List of paths to JDBC *.jar files')

    class Config:
        orm_mode = True


################
# CONNECTIONS
################

class ConnectionCreate(BaseModel):
    name: str = Field(..., title='Connection Name', description='Unique connection name.')
    host: str = Field(..., title='Host', description='Target database host address.')
    port: int = Field(..., title='Port', description='Database port')
    database: Optional[str] = Field(..., title='Database', description='Database name to connect to')
    schema_name: Optional[str] = Field(..., title='Schema', description='Schema used in connection')
    username: str = Field(..., title='Username', description='User name')
    password: Optional[SecretStr] = Field(..., title='Password', description='Database user password')

    class Config:
        json_encoders = {
            SecretStr: lambda v: v.get_secret_value(),
        }


class Connection(ConnectionCreate):
    id: UUID4 = Field(default_factory=uuid4)
    driver: BaseDriver = Field(..., title='Connection driver.')

    class Config:
        orm_mode = True
