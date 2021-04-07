from pathlib import Path

from appdirs import AppDirs

app_dirs = AppDirs("SqlDiff", "")
d = app_dirs.user_data_dir

DEFAULT_FILE_MODE = 0o644

APPLICATION_DATA_PATH = Path(app_dirs.user_data_dir) / 'data'
DRIVERS_FILE_PATH = APPLICATION_DATA_PATH / 'drivers.json'

p = DRIVERS_FILE_PATH.resolve()

# Create application file tree
DRIVERS_FILE_PATH.parent.mkdir(parents=True, exist_ok=True)
DRIVERS_FILE_PATH.touch(exist_ok=True, mode=DEFAULT_FILE_MODE)


