import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QFileDialog, QListView
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSlot

from pyqt5vlc import Player
from FootageArchiverList import FootageArchiverList
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from PyQt5.QtCore import QModelIndex

# E:\TeslaCam
class App(QDialog):
    list = None
    model = None
    modelList = None
    basePath = None
    basePathMap = None

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
        button2 = QPushButton("Back")
        button.clicked.connect(self.onClick2)
        layout.addWidget(button, 0, 3)
        layout.addWidget(button2, 1, 3)
        layout.addWidget(player1, 2, 0)
        layout.addWidget(player2, 2, 1)
        layout.addWidget(player3, 2, 2)

        self.list = QListView()
        self.list.setWindowTitle('Example List')
        self.list.setMinimumSize(600, 400)
        self.list.setGeometry(self.left, self.top+50, self.width, self.height)
        layout.addWidget(self.list, 3, 0)

        self.horizontalGroupBox.setLayout(layout)

    def onClick(self):
        print("processing")
        dialog_txt = "Choose Media File"
        filename = QFileDialog.getExistingDirectory(self, dialog_txt, os.path.expanduser('~'))
        self.modelList = []
        self.createListForDirectory(filename, None)

    def onClick2(self):
        lastModel = self.modelList.pop()
        self.list.setModel(lastModel)
        self.list.show()
        self.list.clicked.connect(self.processDirectory)


    def createListForDirectory(self, baseDirectory, map):
        self.model = QStandardItemModel(self.list)
        self.modelList.append(self.model)
        self.basePath = baseDirectory
        for f in os.listdir(baseDirectory):
            print("file: "+str(f))
            if (os.path.isdir(os.path.join(baseDirectory, f))):
                print("adding directory")
                item = QStandardItem(f)
                self.model.appendRow(item)

        self.list.setModel(self.model)
        self.list.show()
        self.list.clicked.connect(self.processDirectory)

    def processDirectory(self, modelIndex):
        targetFile = self.model.itemFromIndex(modelIndex).text()
        print("processing directory for: "+targetFile)

        self.basePathMap = []
        path = os.path.join(self.basePath, targetFile)
        print( "processing directory in path: "+path)
        for f in os.listdir(path):
            targetFilePath = os.path.join(self.basePath, f)
            #isFile = os.path.isfile(targetFilePath)
            print("files in clicked directory: "+targetFilePath)
            if "front.mp4" in f:
                start = f.find("front.mp4")
                baseName = f[0:start]
                print("base path set as: "+baseName)
                self.basePathMap.append(baseName)

        #for path in basePaths:
        for item in self.basePathMap:
            print("path XXX: "+item)

        #self.createListForDirectory(None, self.basePathMap)









if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())