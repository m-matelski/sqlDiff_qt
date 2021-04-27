"""
This module is responsible for calling in-app sqlite migration when application is launchde.
"""

import sys
from pathlib import Path
from alembic.config import Config
from alembic import command

from sqldiff.appdata.path import DATABASE_URL


def run_migrations(script_location: str, dsn: str) -> None:
    alembic_cfg = Config('alembic.ini')
    alembic_cfg.set_main_option('script_location', script_location)
    alembic_cfg.set_main_option('sqlalchemy.url', dsn)
    command.upgrade(alembic_cfg, 'head')


MIGRATIONS_PATH = Path.cwd() / 'migrations'

print(f'{MIGRATIONS_PATH=}')

# If current module isn't called by alembic, then run application migration.
# Migration is done when application is launched.
# This condition is needed to avoid performing migration when using other alembic commands during development
if Path(sys.modules['__main__'].__file__).stem != 'alembic':
    print('Doing in app migrations')
    run_migrations(str(MIGRATIONS_PATH), DATABASE_URL)
