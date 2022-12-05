#!/usr/bin/env python3
import sys
from PyQt5.QtWidgets import (
    QApplication,
    QMainWindow,
    QWidget,
    QGridLayout,
    QLabel,
    QLineEdit,
    QPushButton,
    QComboBox,
    QMessageBox,
    QVBoxLayout,
    QTabWidget,
    QPlainTextEdit,
)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont

class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SAE3.02")
        self.setMinimumSize(1000, 500)
        self.setCentralWidget(Tab(self))
        self.show()


"""
https://pythonspot.com/pyqt5-tabs/
"""


class Tab(QWidget):
    def __init__(self, parent: MainWindow) -> None:
        super(QWidget, self).__init__(parent)
        self.parent = parent
        self.layout = QGridLayout(self)
        self.setLayout(self.layout)

        # Create Tab Widget
        self.tabwidget = QTabWidget()

        # FIXME: WHY DOES IT NOT WORK AAAAAAAAAAAAAAAAAAAAAA
        self.monospace = QFont()
        self.monospace.setStyleHint(QFont.StyleHint.Courier)

        self.tabs = []
        self.connections = []
        # Add a bunch of tabs
        # FIXME: this should be a separate function to allow the creation of tabs by the user
        for i in range(10):
            self.tabs.append(
                {
                    "widget": QWidget(),
                    "Button_info": QPushButton("Get info."),
                    "Label_info": QLabel("Placeholder\nPlaceholder\nPlaceholder\nPlaceholder\nPlaceholder"),
                    "ComboBox_shell": QComboBox(),
                    "LineEdit_sendcommand": QLineEdit("Send a command..."),
                    "Button_sendcommand": QPushButton("Send"),
                    "LineEdit_resultcommand": QPlainTextEdit("""
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
                    """)
                }
            )
            self.tabwidget.addTab(self.tabs[i]["widget"], f"Tab {i}")
        
            # Set the layout
            self.tabs[i]["widget"].layout = QGridLayout()
            self.tabs[i]["widget"].setLayout(self.tabs[i]["widget"].layout)

            ### FIRST COL
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["Button_info"], 0, 0)
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["Label_info"], 1, 0, 3, 1)

            ### SECOND COL
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["ComboBox_shell"], 0, 1)
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["LineEdit_sendcommand"], 0, 2)
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["Button_sendcommand"], 0, 3)
            self.tabs[i]["widget"].layout.addWidget(self.tabs[i]["LineEdit_resultcommand"], 1, 1, 3, 3)

            self.tabs[i]["LineEdit_resultcommand"].setFont(self.monospace)

        LineEdit_addr = QLineEdit("IP")
        LineEdit_port = QLineEdit("Port")
        Button_conn = QPushButton("Connect")

        self.layout.addWidget(LineEdit_addr, 0, 0)
        self.layout.addWidget(LineEdit_port, 0, 1)
        self.layout.addWidget(Button_conn, 0, 2)
        self.layout.addWidget(self.tabwidget, 1, 0, 1, 3)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
