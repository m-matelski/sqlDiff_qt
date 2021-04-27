from pathlib import Path

from appdirs import AppDirs

app_dirs = AppDirs("SqlDiff", "")
DEFAULT_FILE_MODE = 0o644



APPLICATION_DATA_PATH = Path(app_dirs.user_data_dir) / 'data'
SQLITE_DATABASE_PATH = APPLICATION_DATA_PATH / "sql_app.db"
DATABASE_URL = f"sqlite:///{SQLITE_DATABASE_PATH}"


# Create application file tree
APPLICATION_DATA_PATH.parent.mkdir(parents=True, exist_ok=True)


class ResourcePaths:
    PATH_DB_ICON = Path(":/resources_data/db_icon")
    DB_ICON_POSTGRES = PATH_DB_ICON / "postgres.png"
    DB_ICON_GENERIC = PATH_DB_ICON / "generic.png"
    DB_ICON_TERADATA = PATH_DB_ICON / "teradata.png"

    PATH_DB_LOGO = Path(":/resources_data/db_logo")
    DB_LOGO_POSTGRES = PATH_DB_LOGO / "postgres.png"
    DB_LOGO_GENERIC = PATH_DB_LOGO / "generic.png"
    DB_LOGO_TERADATA = PATH_DB_LOGO / "teradata.png"

    PATH_ICON = Path(":/resources_data/app_icon")
    JAR_ICON = PATH_ICON / 'jar_icon.png'


