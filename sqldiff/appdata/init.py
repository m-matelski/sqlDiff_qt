"""
Initialize application data
"""
from typing import List

from pydantic import BaseModel

import path  # Needs to be executed
from sqldiff.appdata.managers import driver_manager
from sqldiff.appdata.models import BaseDriver, DriverTypes
from sqldiff.appdata.persistence import PersistenceManager
from sqldiff.appdata.url_template import JdbcUrlTemplate


def init_manager_data(manager: PersistenceManager, data: List[BaseModel]):
    if manager.is_empty():
        for record in data:
            manager.insert(record)
        manager.commit()


drivers = [
    BaseDriver(
        driver_name='PostgreSQL',
        driver_type=DriverTypes.POSTGRES,
        jdbc_class_name='org.postgresql.Driver',
        url_template=JdbcUrlTemplate.ModelField('jdbc:postgresql://{host}[:{port}]/[{database}]'),
        default_port=5432,
        expected_driver_files=['postgres.*.jar'],
        driver_files=[]
    ),
]

init_manager_data(driver_manager, drivers)
