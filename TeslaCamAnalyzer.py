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

    dumpFileProcessing = False
    
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
        button.clicked.connect(self.beginProcessingDirectory)
        button2 = QPushButton("Back")
        button2.clicked.connect(self.goBack)
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
        self.list.show()
        self.list.clicked.connect(self.processDirectory)

        self.horizontalGroupBox.setLayout(layout)

    def beginProcessingDirectory(self):
        print("beginProcessingDirectory")
        dialog_txt = "Choose Media File"
        filename = QFileDialog.getExistingDirectory(self, dialog_txt, os.path.expanduser('~'))

        if not filename:
            print("unable to process empty directory, returning")
            return
        self.modelList = []
        self.createListForDirectory(filename)

    def goBack(self):
        if self.basePath is None:
            return
        os.chdir(self.basePath)
        os.chdir("..")
        newPath = os.getcwd()
        print("back button going from: "+str(self.basePath)+" to "+str(newPath))
        self.createListForDirectory(newPath)



    # will add files according to patterns for mp4s
    # and will alos add regular directories
    # possibly split out mp4s to another UI piece
    def createListForDirectory(self, baseDirectory):
        self.model = QStandardItemModel(self.list)
        print("PROCESS DIRECTORY | ModeList[A] | adding: "+str(self.model))
        self.basePath = baseDirectory

        directories = []
        mp4Files = []
        if not os.path.exists(baseDirectory):
            print("PROCESS DIRECTORY | ERROR NO PATH: "+baseDirectory)
            return
        for f in os.listdir(baseDirectory):
            if self.dumpFileProcessing is True:
                print("PROCESS DIRECTORY | file: "+str(f))
            directoryPath = self.joinAndSanitizePath(baseDirectory, f)
            if (os.path.isdir(directoryPath)):
                if self.dumpFileProcessing is True:
                    print("PROCESS DIRECTORY | 1 adding directory | "+directoryPath)
                if len(os.listdir(directoryPath)) <= 0:
                    print("PROCESS DIRECTORY | EMPTY PATH || Excluding path: "+str(directoryPath) +" due to empty")
                    continue
                if self.dumpFileProcessing is True:
                    print("PROCESS DIRECTORY | adding path "+f+" to directory list")
                directories.append(f)
            else :
                if ".mp4" in f:
                    print("PROCESS DIRECTORY | adding mp4 "+f+" to mp4 list")
                    mp4Files.append(f)

        listOfProcessedMp4s = self.processListOfMp4s(mp4Files)

        if listOfProcessedMp4s is not None:
            print("processing list of mp4s")
            listOfProcessedMp4s.sort()
            self.processListAndAdd(listOfProcessedMp4s)
        if directories is not None:
            print("processing list of directories")
            directories.sort()
            self.processListAndAdd(directories)

        self.list.setModel(self.model)

    def processListAndAdd(self, listToProcess):
        if listToProcess is not None:
            print("PROCESS LIST | List is not none | length: "+str(len(listToProcess)))
            for item in listToProcess:
                print("PROCESS LIST | List item: "+item)
                newItem = QStandardItem(item)
                if self.dumpFileProcessing is True:
                    print("PROCESS LIST | adding :" +str(newItem)+" | to model")
                self.model.appendRow(newItem)
        else:
            print("List is empty")

    def processListOfMp4s(self, listOfMp4s):
        if listOfMp4s is None or len(listOfMp4s) == 0:
            print("no MP4s to process")
            return None

        print("PROCESSING MP4s | ")
        processedMp4s = []
        for item in listOfMp4s:
            print("PROCESSING MP4s | item: "+item)
            if "front.mp4" in item:
                start = item.find("front.mp4")
                baseName = item[0:start]
                print("PROCESSING MP4s | baseName: "+baseName)
                processedMp4s.append(baseName)
        return processedMp4s


    def processDirectory(self, modelIndex):
        targetFile = self.model.itemFromIndex(modelIndex).text()
        if self.dumpFileProcessing is True:
            print("PROCESSING DIRECTORY | 1 processing directory for: "+targetFile)

        self.basePathMap = []
        path = self.joinAndSanitizePath(self.basePath, targetFile)
        self.targetPath = path
        print("PROCESSING DIRECTORY | processing directory in path: "+path)
        if not os.path.exists(path):
            print("PROCESSING DIRECTORY | checking path is mp4 pattern")
            self.processDirectory2(path)
            return
        else:
            self.createListForDirectory(path)

    def processDirectory2(self, pattern):
        targetFilePartial = pattern
        print("\n2 PLAYING PATTERN | processing directory for: "+targetFilePartial)
        rebuiltPathA = self.joinAndSanitizePath(self.targetPath, targetFilePartial[:len(targetFilePartial)-1])
        #rebuiltPathB = os.path.abspath(os.path.join(rebuiltPathA, targetFilePartial))

        print("PLAYING PATTERN |processing path(rebuilt): "+rebuiltPathA)

        self.pauseAllPlayersIfNecessary()

        partial = targetFilePartial[:len(targetFilePartial)-1]
        self.textboxLeft.setText("Left: "+partial+"-left_repeater.mp4")
        self.player1.open_file(os.path.abspath(os.path.join(self.targetPath, partial+"-left_repeater.mp4")))

        self.textboxFront.setText("Front: "+partial+"-front.mp4")
        self.player2.open_file(os.path.abspath(os.path.join(self.targetPath, partial+"-front.mp4")))

        self.textboxRight.setText("Right: "+partial+"-right_repeater.mp4")
        self.player3.open_file(os.path.abspath(os.path.join(self.targetPath, partial+"-right_repeater.mp4")))

    def pauseAllPlayersIfNecessary(self):
        if self.player1.isPlaying():
            self.player1.stop()
        if self.player2.isPlaying():
            self.player2.stop()
        if self.player3.isPlaying():
            self.player3.stop()

    def sanitizePaths(self, path1):
        return os.path.abspath(path1)

    def joinAndSanitizePath(self, path1, path2):
        return self.sanitizePaths(os.path.join(path1, path2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())