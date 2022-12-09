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
    QHBoxLayout,
    QMessageBox,
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
        # TODO: implement a way to close tabs
        self.tabwidget.setTabsClosable(True)
        self.tabwidget.setMovable(True)

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
        Label_info = QLabel("Placeholder\nPlaceholder\nPlaceholder\nPlaceholder\nPlaceholder")
        TextBrowser_resultcommand = QTextBrowser()
        # Never crash when connectiong to a server, instead send notification to user
        try:
            conn = connection.Connection(
                ip, port, Label_info, TextBrowser_resultcommand
            )
        except Exception as e:
            logging.error(f"Connection to {name}, {ip}:{port} failed! ({e})")
            self.error_box(
                e, f"Connection to {name} ({ip}:{port}) failed!"
            )
        else:
            self.tabs.append(
                {
                    "widget": QWidget(),
                    "widget_left": QWidget(),
                    "widget_right": QWidget(),
                    "Button_info": QPushButton("Refresh information"),
                    "Label_info": Label_info,
                    "ComboBox_shell": QComboBox(),
                    "LineEdit_sendcommand": QLineEdit(),
                    "Button_clear": QPushButton("Clear"),
                    "TextBrowser_resultcommand": TextBrowser_resultcommand,
                    "Button_disconnect": QPushButton("Disconnect"),
                    "Button_kill": QPushButton("Kill"),
                    "Button_reset": QPushButton("Reset"),
                    "Button_reco": QPushButton("Reconnect"),
                }
            )
            tab = self.tabs[-1]

            tab["conn"] = conn

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

            # row: int, column: int, rowSpan: int, columnSpan: int
            ### widget_left
            tab["widget_left"].layout.addWidget(tab["Button_reco"], 1, 0, 1, 3)
            tab["widget_left"].layout.addWidget(tab["Button_info"], 2, 0, 1, 3)
            tab["widget_left"].layout.addWidget(tab["Label_info"], 3, 0, 1, 3)
            # action buttons
            tab["widget_left"].layout.addWidget(tab["Button_disconnect"], 0, 0)
            tab["widget_left"].layout.addWidget(tab["Button_kill"], 0, 1)
            tab["widget_left"].layout.addWidget(tab["Button_reset"], 0, 2)
            tab["Button_reco"].setEnabled(False)

            ### widget_right
            tab["widget_right"].layout.addWidget(
                tab["TextBrowser_resultcommand"], 1, 0, 3, 3
            )
            tab["widget_right"].layout.addWidget(tab["ComboBox_shell"], 4, 0)
            tab["widget_right"].layout.addWidget(tab["LineEdit_sendcommand"], 4, 1)
            tab["widget_right"].layout.addWidget(tab["Button_clear"], 4, 2)

            # TODO: try this on windows to check if "monospace" works
            tab["TextBrowser_resultcommand"].setFont(QFont("monospace"))
            tab["TextBrowser_resultcommand"].setAcceptRichText(True)
            tab["TextBrowser_resultcommand"].setOpenExternalLinks(True)

            tab["ComboBox_shell"].addItems(["default", "dos", "powershell", "linux"])

            # TODO: shell selection (combobox)
            tab["LineEdit_sendcommand"].returnPressed.connect(
                lambda: self._send_command(
                    tab["conn"], tab["LineEdit_sendcommand"], tab["ComboBox_shell"]
                )
            )

            tab["Button_clear"].clicked.connect(
                lambda: tab["TextBrowser_resultcommand"].clear()
            )

            tab["Button_info"].clicked.connect(lambda: tab["conn"].send("info"))

            # FIXME: Broken Pipe if trying to disconenect from an already disconnected server
            #
            tab["Button_disconnect"].clicked.connect(
                lambda: self.disconnect(tab, "disconnect")
            )
            tab["Button_kill"].clicked.connect(lambda: self.disconnect(tab, "kill"))
            tab["Button_reset"].clicked.connect(lambda: self.disconnect(tab, "reset"))

            tab["Button_reco"].clicked.connect(lambda: self.reco(tab))

    def _connect_Clicked(self):
        ip = self.LineEdit_addr.text()
        port = self.LineEdit_port.text()
        try:
            port = int(port)
        except ValueError as e:
            self.error_box(e, f"Invalid port: {port}!")
            logging.error(f"Invalid port: {port}")
        else:
            self._create_tab(f"{ip}:{port}", ip, port)

    # FIXME: interactive commands make this all fall apart
    def _send_command(
        self, conn: connection.Connection, lineedit: QLineEdit, combobox: QComboBox
    ):
        # TODO: select shell with combobox
        # ["default", "dos", "powershell", "linux"]
        idx = combobox.currentIndex()
        if idx == 0:
            conn.execute_command(lineedit.text())
        elif idx == 1:
            conn.execute_command(lineedit.text(), "dos")
        elif idx == 2:
            conn.execute_command(lineedit.text(), "powershell")
        elif idx == 3:
            conn.execute_command(lineedit.text(), "linux")
        lineedit.setText("")

    def disconnect_all(self):
        if len(self.tabs) > 0:
            for i in self.tabs:
                # Just log errors instead of crashing, it should only happen when a server is already disconnected
                try:
                    i["conn"].disconnect()
                except Exception as e:
                    logging.error(
                        f"Encountered exception while disconnecting all clients: {e}"
                    )
                    continue

    def disconnect(self, tab: dict, action: str):
        if action == "disconnect":
            tab["conn"].disconnect()
        elif action == "reset":
            tab["conn"].reset()
        elif action == "kill":
            tab["conn"].kill()
        tab["Button_reco"].setEnabled(True)
        tab["Button_disconnect"].setEnabled(False)
        tab["Button_kill"].setEnabled(False)
        tab["Button_reset"].setEnabled(False)
        tab["Button_info"].setEnabled(False)

    def reco(self, tab):
        try:
            tab["conn"].reconnect()
        except Exception as e:
            self.error_box(e, "Reconnection failed!")
        else:
            tab["Button_reco"].setEnabled(False)
            tab["Button_disconnect"].setEnabled(True)
            tab["Button_kill"].setEnabled(True)
            tab["Button_reset"].setEnabled(True)
            tab["Button_info"].setEnabled(True)

    def error_box(self, e, message: str = ""):
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Critical)
        msg.setText(f"{message} ({e})")
        msg.exec()

    @property
    def tabs_open(self) -> int:
        return len(self.tabs)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
