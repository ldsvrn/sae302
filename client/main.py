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
)
from PyQt5.QtCore import QCoreApplication


class MainWindow(QMainWindow):
    def __init__(self) -> None:
        super().__init__()
        self.setWindowTitle("SAE3.02")

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

        self.tabs = []
        self.connections = []
        # Add a bunch of tabs
        for i in range(10):
            self.tabs.append(QWidget())
            self.tabwidget.addTab(self.tabs[i], f"Tab {i}")
            self.tabs[i].layout = QGridLayout()
            self.tabs[i].setLayout(self.tabs[i].layout)

            self.tabs[i].layout.addWidget(QPushButton("Get info."), 0, 0)

        # Add tabswidget to layout
        self.layout.addWidget(QLineEdit(), 0, 0)
        self.layout.addWidget(QPushButton("Connect"), 0, 1)
        self.layout.addWidget(self.tabwidget, 1, 0, 1, 2)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
