import re
from pathlib import PosixPath
from typing import List
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from sqldiff.appdata import models, schemas

from sqlalchemy.orm import Session
from sqldiff.appdata.dbconf import db_session


def get_drivers(db: Session = db_session):
    return db.query(models.Driver).all()


def get_driver_by_id(driver_id, db: Session = db_session):
    return db.query(models.Driver).filter(models.Driver.id == driver_id).one()


def get_driver_by_connection(connection: models.Connection, db: Session = db_session):
    return db.query(models.Driver).join(models.Connection).filter(models.Connection.id == connection.id).one()


def get_expected(db: Session = db_session, skip: int = 0, limit: int = 100):
    return db.query(models.ExpectedDriverFile).offset(skip).limit(limit).all()


def get_driver_types(db: Session = db_session):
    return db.query(models.DriverType).all()


def get_driver_type_by_name(name, db: Session = db_session):
    return db.query(models.DriverType).filter(models.DriverType.name == name).one()


def get_driver_type_by_id(driver_type_id, db: Session = db_session):
    return db.query(models.DriverType).filter(models.DriverType.id == driver_type_id).one()


def get_driver_type_by_connection(connection: models.Connection, db: Session = db_session):
    return db.query(models.DriverType).join(models.Driver) \
        .join(models.Connection).filter(models.Connection.id == connection.id).one()


def get_driver_type_by_connection_id(connection_id, db: Session = db_session):
    return db.query(models.DriverType).join(models.Connection).filter(models.Connection.id == connection_id).one()


def get_generic_driver_type(db: Session = db_session):
    return db.query(models.DriverType).filter(models.DriverType.name == 'Generic').one()


def get_driver_type_by_driver_id(driver_id, db: Session = db_session):
    return db.query(models.DriverType).join(models.Driver).filter(models.Driver.id == driver_id).one()


def delete_driver_files_by_driver_id(driver_id, db: Session = db_session):
    db.query(models.DriverFile).filter(models.DriverFile.driver_id == driver_id).delete()


def insert_driver(driver: schemas.BaseDriver, db: Session = db_session):
    driver_instance = models.Driver.create_from_schema(driver, schemas.DriverCreate)
    # Add driver type relation
    driver_instance.driver_type = get_driver_type_by_id(driver.driver_type.id)
    # Add driver files relation
    driver_files = [models.DriverFile.create_from_schema(driver_file, schemas.DriverFileCreate)
                    for driver_file in driver.driver_files]
    driver_instance.driver_files = driver_files

    db.add(driver_instance)
    db.commit()
    db.refresh(driver_instance)
    return driver_instance


def update_driver(driver: schemas.BaseDriver, db: Session = db_session):
    driver_instance = db.query(models.Driver).filter(models.Driver.id == driver.id).first()

    # Update fields
    driver_create = schemas.DriverCreate(**driver.dict())
    db.query(models.Driver).filter(models.Driver.id == driver.id).update(driver_create.dict())

    # Update type
    driver_instance.driver_type = get_driver_type_by_id(driver.driver_type.id)

    # rebuild driver files relation
    delete_driver_files_by_driver_id(driver.id)
    driver_files = [models.DriverFile.create_from_schema(driver_file, schemas.DriverFileCreate)
                    for driver_file in driver.driver_files]
    driver_instance.driver_files = driver_files

    # db.add(driver_instance)
    db.commit()
    db.refresh(driver_instance)
    return driver_instance


def upsert_driver(driver: schemas.BaseDriver, db: Session = db_session):
    driver_instance = db.query(models.Driver).filter(models.Driver.id == driver.id).first()
    if driver_instance:
        return update_driver(driver, db)
    else:
        return insert_driver(driver, db)


def delete_driver(driver: models.Driver, db: Session = db_session):
    db.delete(driver)
    db.commit()


def get_connections(db: Session = db_session):
    return db.query(models.Connection).all()


def get_connection_by_name(name, db: Session = db_session):
    return db.query(models.Connection).filter(models.Connection.name == name).first()


def get_connection_by_id(id, db: Session = db_session):
    return db.query(models.Connection).filter(models.Connection.id == id).one()


def delete_connection(connection: models.Connection, db: Session = db_session):
    db.delete(connection)
    db.commit()


def insert_connection(connection: schemas.Connection, db: Session = db_session):
    connection_instance = models.Connection.create_from_schema(connection, schemas.ConnectionCreate)
    # build connection driver relation
    connection_driver = get_driver_by_id(connection.driver.id)
    connection_instance.driver = connection_driver

    db.add(connection_instance)
    db.commit()
    db.refresh(connection_instance)
    return connection_instance


def update_connection(connection: schemas.Connection, db: Session = db_session):
    # connection_instance = db.query(models.Connection).filter(models.Connection.id == connection.id).one()
    connection_create = schemas.ConnectionCreate(**connection.dict())
    db.query(models.Connection).filter(models.Connection.id == connection.id).update(connection_create.dict())
    db.commit()


def upsert_connection(connection: schemas.Connection, db: Session = db_session):
    # try:
    #     existing_connection_instance = db.query(models.Connection).filter(models.Connection.id == connection.id).one()
    #     update_connection(connection)
    # except NoResultFound:
    #     insert_connection(connection)
    #
    driver_instance = db.query(models.Connection).filter(models.Connection.id == connection.id).first()
    if driver_instance:
        return update_connection(connection, db)
    else:
        return insert_connection(connection, db)
