from enum import Enum


class DriverType(str, Enum):
    GENERIC = 'Generic'
    POSTGRESLQ = 'PostgreSQL'
    TERADATA = 'Teradata'
