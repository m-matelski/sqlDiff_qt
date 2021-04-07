import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from sqldiff.ui.designer.main_window import Ui_MainWindow


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.show()


app = QApplication(sys.argv)
w = MainWindow()
app.exec_()
