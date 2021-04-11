from abc import ABC, abstractmethod

from operator import attrgetter, itemgetter
from typing import Type, Union, List

from sqldiff.appdata.models import PersistenceModel


class PersistenceManagerException(Exception):
    pass


class RecordAlreadyExists(PersistenceManagerException):
    pass


class RecordDoesntExists(PersistenceManagerException):
    pass


class PersistenceManager(ABC):

    @abstractmethod
    def insert(self, entry):
        """Insert entry record"""
        pass

    @abstractmethod
    def update(self, entry):
        """Update entry record"""
        pass

    @abstractmethod
    def delete(self, entry):
        """Delete entry record"""
        pass

    @abstractmethod
    def get_all(self):
        """Get all records from manager"""
        pass

    @abstractmethod
    def commit(self):
        """Get all records from manager"""
        pass

    @abstractmethod
    def rollback(self):
        """Get all records from manager"""
        pass

    @abstractmethod
    def is_empty(self):
        """Returns true if there is no data"""
        pass


class JsonFilePersistenceManager(PersistenceManager):
    """
    Persistence Manager allowing to CRUD data in JSON format from/to specified file path.
    Allows finding records.
    """

    def __init__(self, file_path: str, PersistenceModel: Type[PersistenceModel], key: Union[str, List[str]]):
        self.key = key
        self.PersistenceModel = PersistenceModel
        self.file_path = file_path
        self.data = None
        self._read_persistence_data()

    def __iter__(self):
        return iter(self.data)

    def __getitem__(self, item):
        return self.data[item]

    def __len__(self):
        return len(self.data)

    @property
    def key(self):
        return self._key

    @key.setter
    def key(self, value):
        if isinstance(value, str):
            self._key = (value,)
        else:
            self._key = tuple(value)
        self.key_attr_getter = attrgetter(*self._key)

    @property
    def key_attrs(self):
        return [self.key_attr_getter(i) for i in self.data]

    def _write_persistence_data(self):
        """Overwrites data file with current PersistenceManager data."""
        with open(self.file_path, 'w') as file:
            file.write(self.data.json(indent=4))

    def _read_persistence_data(self):
        with open(self.file_path, 'r') as file:
            file_data = file.read()
            if file_data:
                self.data = self.PersistenceModel.parse_raw(file_data)
            else:
                self.data = PersistenceModel(data=[])

    def insert(self, entry):
        if self.key_attr_getter(entry) not in self.key_attrs:
            self.data.append(entry)
        else:
            raise RecordAlreadyExists(f"Record with keys: {self.key} = {self.key_attr_getter(entry)}, "
                                      f"already exists.")

    def delete(self, entry):
        key = self.key_attr_getter(entry)
        self.data = [i for i in self.data if key != self.key_attr_getter(i)]
        pass

    def update(self, entry):
        self.delete(entry)
        self.insert(entry)
        pass

    def find_by(self, **field_conditions):
        field_names = tuple(field_conditions.keys())
        field_values = tuple(field_conditions.values())
        fields_attr_getter = attrgetter(*field_names)
        matching_records = []
        for record in self.data:
            current_record_key_values = fields_attr_getter(record)
            if not isinstance(current_record_key_values, tuple):
                current_record_key_values = (current_record_key_values,)
            if current_record_key_values == field_values:
                matching_records.append(record)
        return matching_records

    def get_by_key(self, **key_conditions):
        if self.key != tuple(key_conditions.keys()):
            raise ValueError('Invalid key fields.')
        result = self.find_by(**key_conditions)
        if len(result) > 1:
            raise ValueError('Key duplicates')

        try:
            return result[0]
        except IndexError:
            return None

    def get_all(self):
        return self.data

    def is_empty(self):
        return bool(not self.data)

    def commit(self):
        self._write_persistence_data()

    def rollback(self):
        self._read_persistence_data()

