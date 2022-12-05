#!/usr/bin/env python3
import sys
import csv

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
import connection

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
        self.servers = []
        # Add a bunch of tabs

        # TODO: try except 
        with open("servers.csv", "r") as csvfile:
            for row in csv.reader(csvfile):
                self.servers.append(
                    {
                        "name": str(row[0]),
                        "ip": str(row[1]),
                        "port": int(row[2])
                    }
                )
        
        print(self.servers)

        for conn in self.servers:
            self._create_tab(conn["name"], conn["ip"], conn["port"])

        LineEdit_addr = QLineEdit("IP")
        LineEdit_port = QLineEdit("Port")
        Button_conn = QPushButton("Connect")

        self.layout.addWidget(LineEdit_addr, 0, 0)
        self.layout.addWidget(LineEdit_port, 0, 1)
        self.layout.addWidget(Button_conn, 0, 2)
        self.layout.addWidget(self.tabwidget, 1, 0, 1, 3)

    def _create_tab(self, name: str, ip: str, port: int):
        self.tabs.append(
            {
                "widget": QWidget(),
                "Button_info": QPushButton("Get info."),
                "Label_info": QLabel(
                    "Placeholder\nPlaceholder\nPlaceholder\nPlaceholder\nPlaceholder"
                ),
                "ComboBox_shell": QComboBox(),
                "LineEdit_sendcommand": QLineEdit("Send a command..."),
                "Button_sendcommand": QPushButton("Send"),
                "LineEdit_resultcommand": QPlainTextEdit(
                    """
Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do eiusmod tempor
incididunt ut labore et dolore magna aliqua. Ut enim ad minim veniam, quis
nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat.
Duis aute irure dolor in reprehenderit in voluptate velit esse cillum dolore eu
fugiat nulla pariatur. Excepteur sint occaecat cupidatat non proident, sunt in
culpa qui officia deserunt mollit anim id est laborum.
                """
                ),
            }
        )
        tab = self.tabs[-1]

        tab["conn"] = connection.Connection(ip, port, tab["Label_info"], tab["LineEdit_resultcommand"])

        self.tabwidget.addTab(tab["widget"], name)

        # Set the layout
        tab["widget"].layout = QGridLayout()
        tab["widget"].setLayout(tab["widget"].layout)

        ### FIRST COL
        tab["widget"].layout.addWidget(tab["Button_info"], 0, 0)
        tab["widget"].layout.addWidget(tab["Label_info"], 1, 0, 3, 1)

        ### SECOND COL
        tab["widget"].layout.addWidget(tab["ComboBox_shell"], 0, 1)
        tab["widget"].layout.addWidget(tab["LineEdit_sendcommand"], 0, 2)
        tab["widget"].layout.addWidget(tab["Button_sendcommand"], 0, 3)
        tab["widget"].layout.addWidget(tab["LineEdit_resultcommand"], 1, 1, 3, 3)

        tab["LineEdit_resultcommand"].setFont(self.monospace)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
