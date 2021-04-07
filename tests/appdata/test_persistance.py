import os
import unittest
from typing import List

from pydantic import BaseModel

from sqldiff.appdata.models import PersistenceModel
from sqldiff.appdata.persistence import JsonPersistenceManager


class TestModel(BaseModel):
    id: int
    field1: str


class TestPersistenceModel(PersistenceModel):
    data: List[TestModel]


FILE_PATH = 'test_persistence.json'


class TestJsonPersistenceManager(unittest.TestCase):

    def setUp(self) -> None:
        with open(FILE_PATH, 'w') as file:
            pass

    def tearDown(self) -> None:
        os.remove(FILE_PATH)

    def test_insert(self):
        """Test inserting data using manager"""
        pm = JsonPersistenceManager(FILE_PATH, TestPersistenceModel, key='id')
        record1 = TestModel(id=1, field1='value1')
        pm.insert(record1)
        self.assertEqual(record1, pm.data[0])

    def test_delete(self):
        """Test delete record"""
        pm = JsonPersistenceManager(FILE_PATH, TestPersistenceModel, key='id')
        record1 = TestModel(id=1, field1='value1')
        record2 = TestModel(id=2, field1='value2')
        pm.insert(record1)
        pm.insert(record2)
        self.assertEqual(len(pm.data), 2)

        pm.delete(record2)
        self.assertEqual(len(pm.data), 1)

    def test_update(self):
        """Test update record"""
        pm = JsonPersistenceManager(FILE_PATH, TestPersistenceModel, key='id')
        record1 = TestModel(id=1, field1='value1')
        record2 = TestModel(id=2, field1='value2')
        pm.insert(record1)
        pm.insert(record2)
        record2.field1 = 'value3'
        pm.update(record2)

        updated_record = pm.get_by_key(id=2)
        self.assertEqual(record2, updated_record)

    def test_transactions(self):
        """Test transaction commit and rollback"""
        pm = JsonPersistenceManager(FILE_PATH, TestPersistenceModel, key='id')
        record1 = TestModel(id=1, field1='value1')
        record2 = TestModel(id=2, field1='value2')
        pm.insert(record1)
        pm.insert(record2)
        pm.commit()
        record2.field1 = 'value3'
        pm.rollback()
        r = pm.get_by_key(id=2)
        self.assertEqual(r.field1, 'value2')
