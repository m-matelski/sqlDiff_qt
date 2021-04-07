import path
import models
from sqldiff.appdata.persistence import JsonPersistenceManager

driver_manager = JsonPersistenceManager(path.DRIVERS_FILE_PATH, models.DriverPersistence, key='id')
