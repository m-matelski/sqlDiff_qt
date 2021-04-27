import re
from pathlib import PosixPath
from uuid import UUID

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


def upsert_driver(driver: schemas.BaseDriver, db: Session = db):
    d = driver.dict()
    d = {
        'id': UUID('225f4c14-1b87-4b23-abf1-59d15faee2b2'),
        # 'driver_type': {'name': 'PostgreSQL', 'icon_file_path': PosixPath(':/resources_data/db_icon/postgres.png'),
        #                 'logo_file_path': PosixPath(':/resources_data/db_logo/postgres.png')},
        'jdbc_class_name': 'org.postgresql.Driver', 'url_template': 'jdbc:postgresql://{host}[:{port}]/[{database}]',
        'default_port': '5432', 'is_predefined': True,
        'expected_driver_files': [
           {'id': UUID('7d5c9eee-ecfc-4bb2-9a2b-967b5fdf8f5f'), 'file_regex': re.compile('.*postgres.*.jar'),
            'driver_id': UUID('225f4c14-1b87-4b23-abf1-59d15faee2b2')}],
        # 'driver_files': [],
        'name': 'PostgreSQL'}
    # driver1 = models.Driver(
    #     name =
    # )
    driver = models.Driver(**d)
    a = 1
