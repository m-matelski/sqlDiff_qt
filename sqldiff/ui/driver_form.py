from PyQt5.QtWidgets import QWidget

from sqldiff.ui.designer.ui_driver_form import Ui_DriverForm


class DriverForm(QWidget, Ui_DriverForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setupUi(self)
