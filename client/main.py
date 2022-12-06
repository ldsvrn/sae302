#!/usr/bin/env python3
import sys
import csv
import logging

import connection

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
    QTabWidget,
    QTextBrowser,
    QHBoxLayout
)
from PyQt5.QtCore import QCoreApplication
from PyQt5.QtGui import QFont, QCloseEvent

DEBUG = True

if DEBUG:
    logging.basicConfig(level=logging.DEBUG)
else:
    logging.basicConfig(level=logging.WARNING)


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
            if not DEBUG:
                box = QMessageBox()
                box.setWindowTitle("Quit ?")
                box.setText(
                    "Do you really wish to quit? This will disconnect you from all servers."
                )
                box.addButton(QMessageBox.Yes)
                box.addButton(QMessageBox.No)

                ret = box.exec()
            else:
                ret = QMessageBox.Yes

            if ret == QMessageBox.Yes:
                self.tab.disconnect_all()
                QCoreApplication.exit(0)
            else:
                _e.ignore()
        else:
            QCoreApplication.exit(0)


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
        self.monospace.setStyleHint(QFont.StyleHint.Monospace)

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
            logging.warning(f"Error loading servers.csv, ignoring... ({e})")
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
                "widget_left": QWidget(),
                "widget_right": QWidget(),
                "Button_info": QPushButton("Get info."),
                "Label_info": QLabel(
                    "Placeholder\nPlaceholder\nPlaceholder\nPlaceholder\nPlaceholder"
                ),
                "ComboBox_shell": QComboBox(),
                "LineEdit_sendcommand": QLineEdit("Send a command..."),
                "Button_clear": QPushButton("Clear"),
                "TextBrowser_resultcommand": QTextBrowser(),
            }
        )
        tab = self.tabs[-1]

        # TODO: URGENT: try except here or the programme WILL crash if a wrong ip is given

        # FIXME: just crashes the client with no traceback, maybe
        # create a classmethod in connection to check if the server is available
        # before attempting a connection in _connect_Clicked
        tab["conn"] = connection.Connection(
            ip, port, tab["Label_info"], tab["TextBrowser_resultcommand"]
        )

        self.tabwidget.addTab(tab["widget"], name)

        # CREATE LAYOUTS
        tab["widget"].layout = QHBoxLayout()
        tab["widget_left"].layout = QGridLayout()
        tab["widget_right"].layout = QGridLayout()

        tab["widget"].setLayout(tab["widget"].layout)
        tab["widget_left"].setLayout(tab["widget_left"].layout)
        tab["widget_right"].setLayout(tab["widget_right"].layout)

        tab["widget"].layout.addWidget(tab["widget_left"])
        tab["widget"].layout.addWidget(tab["widget_right"])

        ### widget_left
        tab["widget_left"].layout.addWidget(tab["Button_info"], 0, 0)
        tab["widget_left"].layout.addWidget(tab["Label_info"], 1, 0)

        ### widget_right
        tab["widget_right"].layout.addWidget(tab["ComboBox_shell"], 3, 1)
        tab["widget_right"].layout.addWidget(tab["LineEdit_sendcommand"], 3, 2)
        tab["widget_right"].layout.addWidget(tab["Button_clear"], 3, 3)
        tab["widget_right"].layout.addWidget(tab["TextBrowser_resultcommand"], 0, 1, 3, 3)

        # TODO: try this on windows to check if "monospace" works
        tab["TextBrowser_resultcommand"].setFont(QFont("monospace"))
        tab["TextBrowser_resultcommand"].setAcceptRichText(True)
        tab["TextBrowser_resultcommand"].setOpenExternalLinks(True)

        # TODO: shell selection (combobox)
        tab["LineEdit_sendcommand"].returnPressed.connect(
            lambda: self._send_command(tab["conn"], tab["LineEdit_sendcommand"].text())
        )

        tab["Button_clear"].clicked.connect(
            lambda: tab["TextBrowser_resultcommand"].clear()
        )

        tab["Button_info"].clicked.connect(lambda: tab["conn"].send("info"))

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
