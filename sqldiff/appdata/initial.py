"""
Initialize application data
"""
from typing import List

from pydantic import BaseModel

import sqldiff.appdata.path  # Needs to be executed
from sqldiff.appdata.managers import driver_manager, driver_type_manager
from sqldiff.appdata.models import BaseDriver, DriverType
from sqldiff.appdata.persistence import PersistenceManager
from sqldiff.appdata.url_template import JdbcUrlTemplate
from sqldiff.appdata.path import Resources

SCHEMA_VERSION = 1

def init_manager_data(manager: PersistenceManager, data: List[BaseModel]):
    """
    Load initial data.
    Load and persist input data using provided Persistence Manager.
    """
    if manager.is_empty():
        for record in data:
            manager.insert(record)
        manager.commit()
    return manager


# Db types
predefined_driver_types = [
    DriverType(name='Generic', icon_file_path=Resources.DB_ICON_GENERIC, logo_file_path=Resources.DB_LOGO_GENERIC),
    DriverType(name='PostgreSQL', icon_file_path=Resources.DB_ICON_POSTGRES, logo_file_path=Resources.DB_LOGO_POSTGRES),
    DriverType(name='Teradata', icon_file_path=Resources.DB_ICON_TERADATA, logo_file_path=Resources.DB_LOGO_TERADATA)
]

init_manager_data(driver_type_manager, predefined_driver_types)

# Drivers
predefined_drivers = [
    BaseDriver(
        driver_name='PostgreSQL',
        driver_type=driver_type_manager.get_by_key(name='PostgreSQL'),
        jdbc_class_name='org.postgresql.Driver',
        url_template='jdbc:postgresql://{host}[:{port}]/[{database}]',
        default_port=5432,
        expected_driver_files=['.*postgres.*.jar'],
        driver_files=[]
    ),
    BaseDriver(
        driver_name='Teradata',
        driver_type=driver_type_manager.get_by_key(name='Teradata'),
        jdbc_class_name='com.teradata.jdbc.TeraDriver',
        url_template='jdbc:teradata://{host}/DATABASE={database},DBS_PORT={port}',
        default_port=1025,
        expected_driver_files=['.*terajdbc4.jar', '.*tdgssconfig.jar'],
        driver_files=[]
    ),
]

init_manager_data(driver_manager, predefined_drivers)
