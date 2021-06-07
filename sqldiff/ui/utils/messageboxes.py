from PyQt5.QtWidgets import QMessageBox


class ConfirmMessageBoxProvider:
    """
    Confirmation message box factory with Yes/No answers
    """

    def __init__(self, text, title, informative_text):
        self.text = text
        self.title = title
        self.informative_text = informative_text

    def build(self, parent):
        msg = QMessageBox(
            icon=QMessageBox.Question,
            text=self.text,
            parent=parent,
        )
        msg.setWindowTitle(self.title)
        msg.setInformativeText(self.informative_text)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        msg.setDefaultButton(QMessageBox.No)

        button = msg.exec_()
        return button


class SaveChangesMessageBoxProvider:
    """
    Confirmation message box factory with Discard/Cancel answers
    """

    def __init__(self, text,
                 title='Changes detected.',
                 informative_text='Do You want to discard changes and exit?'):
        self.text = text
        self.title = title
        self.informative_text = informative_text

    def build(self, parent):
        msg = QMessageBox(
            icon=QMessageBox.Information,
            text='Driver settings have been modified.',
            parent=parent,
        )
        msg.setWindowTitle('Changes detected.')
        msg.setInformativeText('Do You want to discard changes and exit?')
        msg.setStandardButtons(QMessageBox.Discard | QMessageBox.Cancel)
        msg.setDefaultButton(QMessageBox.Cancel)
        button = msg.exec_()
        return button
