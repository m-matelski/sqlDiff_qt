import json
import uuid

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, UniqueConstraint
from sqlalchemy.orm import relationship

from sqldiff.appdata.dbconf import Base

from sqlalchemy_utils import UUIDType

from sqldiff.appdata import schemas


class CreateFromSchemaMixin:
    @classmethod
    def create_from_schema(cls, schema_instance, SchemaClass):
        # recreate SchemaClass if more detailed subclass with relation passed
        model_instance = SchemaClass(**schema_instance.dict())
        # using json to trigger pydantic encoders
        model_instance_dict = json.loads(model_instance.json())
        obj = cls(**model_instance_dict)
        return obj


class DriverType(Base):
    __tablename__ = "driver_types"
    __table_args__ = (
        UniqueConstraint('name', ),
    )
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String)
    icon_file_path = Column(String)
    logo_file_path = Column(String)

    driver = relationship("Driver", back_populates="driver_type")


class ExpectedDriverFile(Base):
    __tablename__ = "expected_driver_files"
    __table_args__ = (
        UniqueConstraint('file_regex', 'driver_id'),
    )
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    file_regex = Column(String)
    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'))

    driver = relationship("Driver", back_populates="expected_driver_files")


class DriverFile(CreateFromSchemaMixin, Base):
    __tablename__ = "driver_files"
    __table_args__ = (
        UniqueConstraint('file_path', 'driver_id'),
    )
    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    file_path = Column(String)
    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'))

    driver = relationship("Driver", back_populates="driver_files")


class Driver(CreateFromSchemaMixin, Base):
    __tablename__ = "drivers"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True)
    jdbc_class_name = Column(String)
    url_template = Column(String)
    default_port = Column(Integer)
    is_predefined = Column(Boolean)
    driver_type_id = Column(UUIDType(binary=False), ForeignKey('driver_types.id'))

    expected_driver_files = relationship("ExpectedDriverFile", back_populates="driver")
    driver_files = relationship("DriverFile", back_populates="driver")
    driver_type = relationship("DriverType", back_populates="driver")
    connections = relationship("Connection", back_populates="driver")



class Connection(CreateFromSchemaMixin, Base):
    __tablename__ = "connections"

    id = Column(UUIDType(binary=False), primary_key=True, default=uuid.uuid4)
    name = Column(String, unique=True, nullable=False)
    host = Column(String)
    port = Column(Integer)
    database = Column(String)
    schema_name = Column(String)
    username = Column(String)
    password = Column(String)
    driver_id = Column(UUIDType(binary=False), ForeignKey('drivers.id'))
    driver = relationship("Driver", back_populates="connections")

