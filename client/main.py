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
    QTabWidget
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
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Create Tab Widget
        self.tabwidget = QTabWidget()

        self.tabs = []
        # Add a bunch of tabs
        for i in range(10):
            self.tabs.append(QWidget())
            self.tabwidget.addTab(self.tabs[i], f"Tab {i}")
            self.tabs[i].layout = QGridLayout()
            self.tabs[i].setLayout(self.tabs[i].layout)

        # # Create first tab
        # self.tab1.layout = QVBoxLayout(self)
        # self.pushButton1 = QPushButton("PyQt5 button")
        # self.tab1.layout.addWidget(self.pushButton1)
        # self.tab1.setLayout(self.tab1.layout)
        self.tabs[0].layout.addWidget(QPushButton("Hello World!"), 0, 0)
        self.tabs[0].layout.addWidget(QPushButton("Hello!"), 1, 1)
        self.tabs[0].layout.addWidget(QPushButton("Test!"), 0, 3)

        # Add tabswidget to layout
        self.layout.addWidget(self.tabwidget)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    app.exec()
