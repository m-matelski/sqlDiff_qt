from PyQt5.QtWidgets import QMainWindow, QApplication

from sqldiff.ui.main_window import MainWindow

# Load resources
import ui.designer.resources_rc
# Process initial data
import appdata.migration

import sys

if __name__ == "__main__":
    app = QApplication(sys.argv)
    w = MainWindow()
    app.exec_()
