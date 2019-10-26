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

    videoPlayerLeft = None
    videoPlayerFront = None
    videoPlayerRight = None
    videoPlayerBack = None

    textboxLeft = None
    textboxFront = None
    textboxBack = None
    textboxRight = None

    dumpFileProcessing = False
    
    def __init__(self):
        super().__init__()
        self.title = 'Tesla Footage Analyzer'
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
        self.horizontalGroupBox = QGroupBox("Path: ")
        layout = QGridLayout()

        self.videoPlayerLeft = Player()
        self.videoPlayerLeft.resize(640, 480)
        self.videoPlayerLeft.show()

        self.videoPlayerFront = Player()
        self.videoPlayerFront.resize(640, 480)
        self.videoPlayerFront.show()

        self.videoPlayerRight = Player()
        self.videoPlayerRight.resize(640, 480)
        self.videoPlayerRight.show()

        self.videoPlayerBack = Player()
        self.videoPlayerBack.resize(640,480)
        self.videoPlayerBack.show()

        self.textboxLeft = QLineEdit(self)
        self.textboxLeft.resize(280, 40)
        self.textboxFront = QLineEdit(self)
        self.textboxFront.resize(280, 40)
        self.textboxBack = QLineEdit(self)
        self.textboxBack.resize(280, 40)
        self.textboxRight= QLineEdit(self)
        self.textboxRight.resize(280, 40)

        button = QPushButton("Load Path")
        button.clicked.connect(self.beginProcessingDirectory)
        button2 = QPushButton("Back")
        button2.clicked.connect(self.goBack)
        layout.addWidget(button, 0, 3)
        layout.addWidget(button2, 1, 3)
        layout.addWidget(self.textboxLeft, 2, 0)
        layout.addWidget(self.textboxFront, 2, 1)
        layout.addWidget(self.textboxBack, 2, 2)
        layout.addWidget(self.textboxRight, 2, 3)
        layout.addWidget(self.videoPlayerLeft, 3, 0)
        layout.addWidget(self.videoPlayerFront, 3, 1)
        layout.addWidget(self.videoPlayerBack, 3, 2)
        layout.addWidget(self.videoPlayerRight, 3, 3)

        #List for list of files
        self.list = QListView()
        self.list.setWindowTitle("Tesla Foootage Analyzer")
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
    # and will also add regular directories
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
            if self.dumpFileProcessing:
                print("PROCESS DIRECTORY | file: "+str(f))
            directoryPath = self.joinAndSanitizePath(baseDirectory, f)
            if (os.path.isdir(directoryPath)):
                if self.dumpFileProcessing:
                    print("PROCESS DIRECTORY | 1 adding directory | "+directoryPath)
                if len(os.listdir(directoryPath)) <= 0:
                    print("PROCESS DIRECTORY | EMPTY PATH || Excluding path: "+str(directoryPath) +" due to empty")
                    continue
                if self.dumpFileProcessing:
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
                if self.dumpFileProcessing:
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
        if self.dumpFileProcessing:
            print("PROCESSING DIRECTORY | 1 processing directory for: "+targetFile)

        self.basePathMap = []
        path = self.joinAndSanitizePath(self.basePath, targetFile)
        self.targetPath = path
        print("PROCESSING DIRECTORY | processing directory in path: "+path)
        if not os.path.exists(path):
            print("PROCESSING DIRECTORY | checking path is mp4 pattern")
            self.processPattern(path)
            return
        else:
            self.createListForDirectory(path)

    def processPattern(self, pattern):
        targetFilePartial = pattern
        print("\n2 PLAYING PATTERN | processing directory for: "+targetFilePartial)
        rebuiltPathA = self.joinAndSanitizePath(self.targetPath, targetFilePartial[:len(targetFilePartial)-1])
        #rebuiltPathB = os.path.abspath(os.path.join(rebuiltPathA, targetFilePartial))

        print("PLAYING PATTERN |processing path(rebuilt): "+rebuiltPathA)

        self.pauseAllPlayersIfNecessary()
        self.horizontalGroupBox.setTitle("Path: "+self.targetPath)
        partial = targetFilePartial[:len(targetFilePartial)-1]
        
        self.textboxLeft.setText("Left: "+partial+"-left_repeater.mp4")
        self.videoPlayerLeft.open_file(os.path.abspath(os.path.join(self.targetPath, partial + "-left_repeater.mp4")))

        self.textboxFront.setText("Front: "+partial+"-front.mp4")
        self.videoPlayerFront.open_file(os.path.abspath(os.path.join(self.targetPath, partial + "-front.mp4")))

        self.textboxBack.setText("Front: "+partial+"-back.mp4")
        self.videoPlayerBack.open_file(os.path.abspath(os.path.join(self.targetPath, partial + "-back.mp4")))

        self.textboxRight.setText("Right: "+partial+"-right_repeater.mp4")
        self.videoPlayerRight.open_file(os.path.abspath(os.path.join(self.targetPath, partial + "-right_repeater.mp4")))



    def pauseAllPlayersIfNecessary(self):
        if self.videoPlayerLeft.isPlaying():
            self.videoPlayerLeft.stop()
        if self.videoPlayerFront.isPlaying():
            self.videoPlayerFront.stop()
        if self.videoPlayerBack.isPlaying():
            self.videoPlayerFront.stop()
        if self.videoPlayerRight.isPlaying():
            self.videoPlayerRight.stop()

    def sanitizePaths(self, path1):
        return os.path.abspath(path1)

    def joinAndSanitizePath(self, path1, path2):
        return self.sanitizePaths(os.path.join(path1, path2))

if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())