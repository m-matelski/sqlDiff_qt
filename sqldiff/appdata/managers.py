from sqldiff.appdata import path, models
from sqldiff.appdata.persistence import JsonFilePersistenceManager

driver_manager = JsonFilePersistenceManager(path.DRIVERS_FILE_PATH, models.DriverPersistence, key='id')
driver_type_manager = JsonFilePersistenceManager(path.DRIVER_TYPE_FILE_PATH, models.DriverTypePersistence, key='name')
