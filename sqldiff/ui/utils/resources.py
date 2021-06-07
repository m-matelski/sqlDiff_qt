from sqldiff.appdata.crud import get_driver_types
from PyQt5 import QtGui


class DbIconsProvider:
    def __init__(self):
        # Creates driver types reference in constructor as it won't change during program execution
        self.driver_types = {driver_type.name: driver_type for driver_type in get_driver_types()}
        pass

    def get_icon_pixmap(self, name, scaled_to_width):
        driver_type = self.driver_types[name]
        pixmap = QtGui.QPixmap(str(driver_type.icon_file_path)).scaledToWidth(scaled_to_width)
        return pixmap

    def get_icon(self, name):
        driver_type = self.driver_types[name]
        icon = QtGui.QIcon(str(driver_type.icon_file_path))
        return icon

    def get_logo(self, name):
        driver_type = self.driver_types[name]
        pixmap = QtGui.QPixmap(str(driver_type.logo_file_path))
        return pixmap


