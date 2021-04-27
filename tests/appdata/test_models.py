import unittest
from pathlib import Path
from uuid import uuid4

from sqldiff.appdata import schemas, models
from sqldiff.appdata.url_template import JdbcUrlTemplate


class TestBaseDriverModel(unittest.TestCase):

    def test_create_model_from_base_driver_schema(self):
        # driver_file = DriverFile.construct(
        #     driver_id=uuid4(),
        #     file_path=Path('/')
        # )

        driver_file_dict = {
            'name': 'name',
            'icon_file_path': Path('/'),
            'logo_file_path': Path('/'),
            'dummy': 123
        }

        driver_file_create = schemas.DriverType(**driver_file_dict)
        a = 1

    def test_create_driver_file_model_from_schema(self):
        driver_schema = schemas.DriverFile.construct(driver_id=uuid4(),
                   file_path=Path('/'))

        driver_file_model_instance = models.DriverFile.create_from_schema(driver_schema, schemas.DriverFile)
        a = 1
        x = []
        b = 1

    def test3(self):
        driver_create = schemas.DriverCreate(
            default_port=5432,

        )
