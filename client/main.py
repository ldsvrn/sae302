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
from PyQt5.QtGui import QFont, QCloseEvent
import connection
import logging


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SAE3.02")
        self.setMinimumSize(1000, 500)
        self.tab = Tab(self)
        self.setCentralWidget(self.tab)
        self.show()

    def closeEvent(self, _e: QCloseEvent):
        if self.tab.tabs_open >= 1:
            box = QMessageBox()
            box.setWindowTitle("Quit ?")
            box.setText(
                "Do you really wish to quit? This will disconnect you from all servers."
            )
            box.addButton(QMessageBox.Yes)
            box.addButton(QMessageBox.No)

            ret = box.exec()

            if ret == QMessageBox.Yes:
                self.tab.disconnect_all()
                QCoreApplication.exit(0)
            else:
                _e.ignore()
        else:
            QCoreApplication.exit(0)


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

        # FIXME: should be relative to the script location
        try:
            with open("servers.csv", "r") as csvfile:
                for row in csv.reader(csvfile):
                    self.servers.append(
                        {"name": str(row[0]), "ip": str(row[1]), "port": int(row[2])}
                    )
        except Exception as e:
            logging.error(f"Error loading servers.csv, ignoring... ({e})")
            pass
        else:
            for conn in self.servers:
                self._create_tab(conn["name"], conn["ip"], conn["port"])

        self.LineEdit_addr = QLineEdit("IP")
        self.LineEdit_port = QLineEdit("Port")
        self.Button_conn = QPushButton("Connect")

        self.Button_conn.clicked.connect(self._connect_Clicked)

        self.layout.addWidget(self.LineEdit_addr, 0, 0)
        self.layout.addWidget(self.LineEdit_port, 0, 1)
        self.layout.addWidget(self.Button_conn, 0, 2)
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

        # TODO: URGENT: try except here or the programme WILL crash if a wrong ip is given
        tab["conn"] = connection.Connection(
            ip, port, tab["Label_info"], tab["LineEdit_resultcommand"]
        )

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

        # TODO: shell selection
        # lambda function => args 
        tab["Button_sendcommand"].clicked.connect(
            lambda: self._send_command(tab["conn"], tab["LineEdit_sendcommand"].text())
        )

    def _connect_Clicked(self):
        ip = self.LineEdit_addr.text()
        port = int(self.LineEdit_port.text())
        self._create_tab(ip, ip, port)

    def _send_command(self, conn: connection.Connection, command: str):
        conn.execute_command(command)

    def disconnect_all(self):
        if len(self.tabs) > 0:
            for i in self.tabs:
                i["conn"].disconnect()

    @property
    def tabs_open(self) -> int:
        return len(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
