import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QFileDialog
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyqt5vlc import Player
from FootageArchiverList import FootageArchiverList

# E:\TeslaCam
class App(QDialog):

    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top+50, self.width, self.height)

        self.createGridLayout()

        windowLayout = QVBoxLayout()
        windowLayout.addWidget(self.horizontalGroupBox)
        self.setLayout(windowLayout)

        self.show()

    def createGridLayout(self):
        self.horizontalGroupBox = QGroupBox("Grid")
        layout = QGridLayout()
        #layout.setColumnStretch(1, 3)
        #layout.setColumnStretch(2, 3)

        player1 = Player()
        player1.resize(640, 480)
        player1.show();

        player2 = Player()
        player2.resize(640, 480)
        player2.show();

        player3 = Player()
        player3.resize(640, 480)
        player3.show();

        button = QPushButton("Begin")
        button.clicked.connect(self.onClick)
        layout.addWidget(button, 0, 3)
        layout.addWidget(player1, 1, 0)
        layout.addWidget(player2, 1, 1)
        layout.addWidget(player3, 1, 2)

        self.horizontalGroupBox.setLayout(layout)

    def onClick(self):
        print("processing")
        dialog_txt = "Choose Media File"
        filename = QFileDialog.getExistingDirectory(self, dialog_txt, os.path.expanduser('~'))
        footageArchiver = FootageArchiverList()
        footageArchiver.processDirectory(filename)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())