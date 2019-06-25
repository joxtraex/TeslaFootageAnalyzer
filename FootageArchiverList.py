from PyQt5.QtWidgets import QListView
from PyQt5.QtGui import QStandardItem, QStandardItemModel
from os import listdir
from os.path import isfile, join

class FootageArchiverList:
    def __init__(self):
        super().__init__()
        self.title = 'PyQt5 layout - pythonspot.com'
        self.left = 10
        self.top = 10
        self.width = 1920
        self.height = 1080

    def initUI(self, file):
        list = QListView()
        list.setWindowTitle('Example List')
        list.setMinimumSize(600, 400)
        list.setGeometry(self.left, self.top+50, self.width, self.height)

        model = QStandardItemModel(list)
        for f in file:
            item = QStandardItem(f)
            model.appendRow(item)

        list.setModel(model)
        list.show()

    def processDirectory(self, file):
        if not file:
            return
        print("processing file: "+file)
        self.initUI(listdir(file))