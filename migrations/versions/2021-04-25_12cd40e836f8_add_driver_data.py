"""Add driver data

Revision ID: 12cd40e836f8
Revises: fd95d6628f3c
Create Date: 2021-04-25 18:09:55.668954

"""
from alembic import op
import sqlalchemy as sa
import sqlalchemy_utils

from sqlalchemy import table, column, Integer, String, Date, Boolean
from sqlalchemy_utils import UUIDType

from sqldiff.appdata.path import ResourcePaths

# revision identifiers, used by Alembic.
revision = '12cd40e836f8'
down_revision = 'fd95d6628f3c'
branch_labels = None
depends_on = None

# Create an ad-hoc table to use for the insert statement.
driver_types_table = table(
    'driver_types',
    column('id', UUIDType(binary=False)),
    column('name', String),
    column('icon_file_path', String),
    column('logo_file_path', String)
)

drivers_table = table(
    'drivers',
    column('id', UUIDType(binary=False)),
    column('name', String),
    column('jdbc_class_name', String),
    column('url_template', String),
    column('default_port', Integer),
    column('is_predefined', Boolean),
    column('driver_type_id', UUIDType(binary=False))
)

expected_driver_files_table = table(
    'expected_driver_files',
    column('id', UUIDType(binary=False)),
    column('file_regex', String),
    column('driver_id', UUIDType(binary=False))
)

GENERIC_DRIVER_TYPE_UUID = '08f6dab2ce0d4f6e9ee0cb20a02079ae'
POSTGRES_DRIVER_TYPE_UUID = 'cb36e2d7b96e4451ab7a02510dee3571'
TERADATA_DRIVER_TYPE_UUID = '1e3d0000326b4e078ceaab2e75cf0004'

POSTGRES_DRIVER_UUID = '225f4c141b874b23abf159d15faee2b2'
TERADATA_DRIVER_UUID = 'fbe03300b5df45b6975094801b9206a5'


def upgrade():
    # Insert driver types
    op.bulk_insert(
        driver_types_table,
        [
            {
                'id': GENERIC_DRIVER_TYPE_UUID,
                'name': 'Generic',
                'icon_file_path': str(ResourcePaths.DB_ICON_GENERIC),
                'logo_file_path': str(ResourcePaths.DB_LOGO_GENERIC)

            },
            {
                'id': POSTGRES_DRIVER_TYPE_UUID,
                'name': 'PostgreSQL',
                'icon_file_path': str(ResourcePaths.DB_ICON_POSTGRES),
                'logo_file_path': str(ResourcePaths.DB_LOGO_POSTGRES)

            },
            {
                'id': TERADATA_DRIVER_TYPE_UUID,
                'name': 'Teradata',
                'icon_file_path': str(ResourcePaths.DB_ICON_TERADATA),
                'logo_file_path': str(ResourcePaths.DB_LOGO_TERADATA)

            }
        ],
        multiinsert=False
    )

    # Insert predefined drivers
    op.bulk_insert(
        drivers_table,
        [
            {
                'id': POSTGRES_DRIVER_UUID,
                'name': 'PostgreSQL',
                'jdbc_class_name': 'org.postgresql.Driver',
                'url_template': 'jdbc:postgresql://{host}[:{port}]/[{database}]',
                'default_port': 5432,
                'is_predefined': True,
                'driver_type_id': POSTGRES_DRIVER_TYPE_UUID,
            },
            {
                'id': TERADATA_DRIVER_UUID,
                'name': 'Teradata',
                'jdbc_class_name': 'com.teradata.jdbc.TeraDriver',
                'url_template': 'jdbc:teradata://{host}/DATABASE={database},DBS_PORT={port}',
                'default_port': 1025,
                'is_predefined': True,
                'driver_type_id': TERADATA_DRIVER_TYPE_UUID,
            },
        ],
        multiinsert=False
    )

    # Insert expected driver files for predefined drivers
    op.bulk_insert(
        expected_driver_files_table,
        [
            # Postgres
            {
                'id': '7d5c9eeeecfc4bb29a2b967b5fdf8f5f',
                'file_regex': '.*postgres.*.jar',
                'driver_id': POSTGRES_DRIVER_UUID
            },
            # Teradata
            {
                'id': '447365a7f3684291b52000d725d83389',
                'file_regex': '.*terajdbc4.jar',
                'driver_id': TERADATA_DRIVER_UUID
            },
            {
                'id': 'b26204f793fe45a6839ad5f25e91c3ba',
                'file_regex': '.*tdgssconfig.jar',
                'driver_id': TERADATA_DRIVER_UUID
            },
        ],
        multiinsert=False
    )


def downgrade():
    pass
