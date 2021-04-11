"""
Initialize application data
"""
from typing import List

from pydantic import BaseModel

import sqldiff.appdata.path  # Needs to be executed
from sqldiff.appdata.managers import driver_manager
from sqldiff.appdata.models import BaseDriver, DriverTypes
from sqldiff.appdata.persistence import PersistenceManager
from sqldiff.appdata.url_template import JdbcUrlTemplate


def init_manager_data(manager: PersistenceManager, data: List[BaseModel]):
    """
    Load initial data.
    Load and persist input data using provided Persistence Manager.
    """
    if manager.is_empty():
        for record in data:
            manager.insert(record)
        manager.commit()


predefined_drivers = [
    BaseDriver(
        driver_name='PostgreSQL',
        driver_type=DriverTypes.POSTGRES,
        jdbc_class_name='org.postgresql.Driver',
        url_template='jdbc:postgresql://{host}[:{port}]/[{database}]',
        default_port=5432,
        expected_driver_files=['postgres.*.jar'],
        driver_files=[]
    ),
    BaseDriver(
        driver_name='Teradata',
        driver_type=DriverTypes.TERADATA,
        jdbc_class_name='com.teradata.jdbc.TeraDriver',
        url_template='jdbc:teradata://{host}/DATABASE={database},DBS_PORT={port}',
        default_port=1025,
        expected_driver_files=['terajdbc4.jar', 'tdgssconfig.jar'],
        driver_files=[]
    ),
]

init_manager_data(driver_manager, predefined_drivers)
