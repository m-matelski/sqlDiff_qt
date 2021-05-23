import argparse
import sys

from PyQt5.QtWidgets import QMainWindow, QApplication

from sqldiff.ui.main_window import MainWindow

# Load resources
import ui.designer.resources_rc
# Process initial data
import appdata.migration


def process_cl_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--dry-run', action='store_true',
                        help='Runs application in a dry mode. Main application loop is omitted.')
    parser.add_argument('--dry-runn', action='store_true',
                        help='Runs application in a dry mode. Main application loop is omitted.')

    parsed_args, unparsed_args = parser.parse_known_args()
    return parsed_args, unparsed_args


def on_focus_changed(old, new):
    print(f'changing focus {old} -> {new}')


if __name__ == "__main__":
    args, _ = process_cl_args()
    app = QApplication(sys.argv)
    app.focusChanged.connect(on_focus_changed)
    w = MainWindow()
    if not args.dry_run:
        app.exec_()
    else:
        print('Dry run')
