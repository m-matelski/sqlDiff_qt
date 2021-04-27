import unittest

from sqldiff.appdata.schemas import BaseDriver, DriverType
from sqldiff.appdata.url_template import JdbcUrlTemplate


class TestBaseDriverModel(unittest.TestCase):

    def test_model_serialization(self):
        driver = BaseDriver(
            driver_name='PostgreSQL',
            driver_type=DriverType.POSTGRES,
            jdbc_class_name='org.postgresql.Driver',
            url_template='jdbc:postgresql://{host}[:{port}]/[{database}]',
            default_port=5432,
            expected_driver_files=['postgres.*.jar'],
            driver_files=[]
        )

        json_content = driver.json(indent=4)
        a =1


