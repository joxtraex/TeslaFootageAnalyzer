import sys
import os
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QHBoxLayout, QGroupBox, QDialog, QVBoxLayout, \
    QGridLayout, QFileDialog, QListView, QLineEdit
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
    targetPath = None

    player1 = None
    player2 = None
    player3 = None

    textboxLeft = None
    textboxFront = None
    textboxRight = None

    dumpFileProcessing = False;
    
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

        self.player1 = Player()
        self.player1.resize(640, 480)
        self.player1.show()

        self.player2 = Player()
        self.player2.resize(640, 480)
        self.player2.show()

        self.player3 = Player()
        self.player3.resize(640, 480)
        self.player3.show()

        self.textboxLeft = QLineEdit(self)
        self.textboxLeft.resize(280, 40)
        self.textboxFront = QLineEdit(self)
        self.textboxFront.resize(280, 40)
        self.textboxRight= QLineEdit(self)
        self.textboxRight.resize(280, 40)

        button = QPushButton("Begin")
        button.clicked.connect(self.onClick)
        button2 = QPushButton("Back")
        button2.clicked.connect(self.onClick2)
        layout.addWidget(button, 0, 3)
        layout.addWidget(button2, 1, 3)
        layout.addWidget(self.textboxLeft, 2, 0)
        layout.addWidget(self.textboxFront, 2, 1)
        layout.addWidget(self.textboxRight, 2, 2)
        layout.addWidget(self.player1, 3, 0)
        layout.addWidget(self.player2, 3, 1)
        layout.addWidget(self.player3, 3, 2)

        self.list = QListView()
        self.list.setWindowTitle('Example List')
        self.list.setMinimumSize(600, 400)
        self.list.setGeometry(self.left, self.top+50, self.width, self.height)
        layout.addWidget(self.list, 4, 0)

        self.horizontalGroupBox.setLayout(layout)

    def onClick(self):
        print("processing")
        dialog_txt = "Choose Media File"
        filename = QFileDialog.getExistingDirectory(self, dialog_txt, os.path.expanduser('~'))
        self.modelList = []
        self.createListForDirectory(filename)

    def onClick2(self):
        lastModel = None
        # don't pop the last element
        if len(self.modelList) > 1:
            #Hack for fixing list - may get rid of list
            self.modelList.pop()
            lastModel = self.modelList.pop()
        else:
            lastModel = self.modelList[-1];
        print("ModeList[Pop] | "+str(lastModel))
        self.list.setModel(lastModel)
        self.list.show()
        self.list.disconnect()
        self.list.clicked.connect(self.processDirectory)


    def createListForDirectory(self, baseDirectory):
        self.model = QStandardItemModel(self.list)
        self.modelList.append(self.model)
        print("ModeList[A] | adding: "+str(self.model))
        self.basePath = baseDirectory

        for f in os.listdir(baseDirectory):
            if self.dumpFileProcessing is True:
                print("file: "+str(f))
            directoryPath = os.path.join(baseDirectory, f)
            if (os.path.isdir(directoryPath)):
                if self.dumpFileProcessing is True:
                    print("1 adding directory | "+directoryPath)
                if len(os.listdir(directoryPath)) <= 0:
                    print("EMPTY PATH || Excluding path: "+str(directoryPath) +" due to empty")
                    continue
                item = QStandardItem(f)
                self.model.appendRow(item)

        self.list.setModel(self.model)
        self.list.show()
        self.list.clicked.connect(self.processDirectory)

    def createListForMap(self, map):
        model2 = QStandardItemModel(self.list)
        self.modelList.append(model2)
        print("ModeList[B] | adding: "+str(model2))
        for item in map:
            print("2 adding directory")
            item = QStandardItem(item)
            model2.appendRow(item)

        self.list.setModel(model2)
        self.list.show()
        self.list.clicked.disconnect()
        self.list.clicked.connect(self.processDirectory2)


    def processDirectory(self, modelIndex):
        targetFile = self.model.itemFromIndex(modelIndex).text()
        if self.dumpFileProcessing is True:
            print("1 processing directory for: "+targetFile)

        self.basePathMap = []
        path = os.path.join(self.basePath, targetFile)
        self.targetPath = path
        print( "processing directory in path: "+path)
        for f in os.listdir(path):
            targetFilePath = os.path.join(self.basePath, f)
            #isFile = os.path.isfile(targetFilePath)
            if self.dumpFileProcessing is True:
                print("files in clicked directory: "+targetFilePath)
            if "front.mp4" in f:
                start = f.find("front.mp4")
                baseName = f[0:start]
                print("base path set as: "+baseName)
                self.basePathMap.append(baseName)

        self.basePathMap.sort()
        #for path in basePaths:
        for item in self.basePathMap:
            print("path XXX: "+item)

        self.createListForMap(self.basePathMap)

    def processDirectory2(self, modelIndex):
        targetFilePartial = self.modelList[-1].itemFromIndex(modelIndex).text()
        print("\n2 processing directory for: "+targetFilePartial)
        rebuiltPathA = os.path.abspath(os.path.join(self.targetPath, targetFilePartial[:len(targetFilePartial)-1]))
        #rebuiltPathB = os.path.abspath(os.path.join(rebuiltPathA, targetFilePartial))

        print("processing path(rebuilt): "+rebuiltPathA)

        self.pauseAllPlayersIfNecessary()

        self.textboxLeft.setText("Left: "+targetFilePartial[:len(targetFilePartial)-1]+"-left_repeater.mp4")
        self.player1.open_file(os.path.abspath(os.path.join(self.targetPath, targetFilePartial[:len(targetFilePartial)-1]+"-left_repeater.mp4")))

        self.textboxFront.setText("Front: "+targetFilePartial[:len(targetFilePartial)-1]+"-front.mp4")
        self.player2.open_file(os.path.abspath(os.path.join(self.targetPath, targetFilePartial[:len(targetFilePartial)-1]+"-front.mp4")))

        self.textboxRight.setText("Right: "+targetFilePartial[:len(targetFilePartial)-1]+"-right_repeater.mp4")
        self.player3.open_file(os.path.abspath(os.path.join(self.targetPath, targetFilePartial[:len(targetFilePartial)-1]+"-right_repeater.mp4")))

    def pauseAllPlayersIfNecessary(self):
        if self.player1.isPlaying():
            self.player1.stop()
        if self.player2.isPlaying():
            self.player2.stop()
        if self.player3.isPlaying():
            self.player3.stop()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())