import re
from pathlib import PosixPath
from typing import List
from uuid import UUID

from sqlalchemy.exc import NoResultFound

from sqldiff.appdata import models, schemas

from sqlalchemy.orm import Session
from sqldiff.appdata.dbconf import db


# def get_drivers(db: Session = db, skip: int = 0, limit: int = 100):

def get_drivers(db: Session = db):
    # q = db.query(models.Driver).all()
    # q = db.query(models.Driver)
    # print(str(q.statement.compile(dialect=sqlite.dialect())))
    return db.query(models.Driver).all()


def get_driver_by_id(id, db: Session = db):
    return db.query(models.Driver).filter(id=id)


def get_expected(db: Session = db, skip: int = 0, limit: int = 100):
    return db.query(models.ExpectedDriverFile).offset(skip).limit(limit).all()


def get_driver_types(db: Session = db):
    return db.query(models.DriverType).all()


def get_driver_type_by_name(name, db: Session = db):
    return db.query(models.DriverType).filter(models.DriverType.name == name).first()


def get_generic_driver_type(db: Session = db):
    return db.query(models.DriverType).filter(models.DriverType.name == 'Generic').one()


def upsert_driver(driver: schemas.BaseDriver, db: Session = db):
    # TODO write tests for method
    try:
        driver_instance = db.query(models.Driver).filter(models.Driver.id == driver.id).one()
    except NoResultFound:
        driver_instance = models.Driver.create_from_schema(driver, schemas.DriverCreate)
        driver_instance.driver_type = get_generic_driver_type(db)

    # Add relations
    # Add driver files relation from form. Delete (overwrite) previously defined driver files.
    driver_files = [models.DriverFile.create_from_schema(driver_file, schemas.DriverFileCreate)
                    for driver_file in driver.driver_files]
    driver_instance.driver_files = driver_files

    db.add(driver_instance)
    db.commit()
    db.refresh(driver_instance)
    return driver_instance


def delete_driver(driver: models.Driver, db: Session = db):
    db.delete(driver)
    db.commit()


def delete_drivers(drivers: List[models.Driver], db: Session = db):
    for driver in drivers:
        delete_driver(driver)


