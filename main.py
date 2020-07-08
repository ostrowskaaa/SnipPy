import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage

import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

import makeCrop

##############  SAVE CROP AND MAIN WINDOW  #################

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        myQWidget = QWidget()
        layout = QHBoxLayout()
        self.toolbar = self.addToolBar('toolbar')

        newCrop = QAction(QIcon('new.png'), 'new', self)
        newCrop.setShortcut('Ctrl+N')
        newCrop.triggered.connect(self.hideMainWindow)

        saveJPG = QAction(QIcon('save.png'), 'save', self)
        saveJPG.setShortcut('Ctrl+S')
        saveJPG.triggered.connect(self.save_function)

        word = QAction(QIcon('word.png'), 'word', self)
        word.setShortcut('Ctrl+W')
        word.triggered.connect(self.word_function)

        excel = QAction(QIcon('excel.png'), 'excel', self)
        excel.setShortcut('Ctrl+E')
        excel.triggered.connect(self.excel_function)

        exit = QAction('', self)
        exit.setShortcut('Escape')
        exit.triggered.connect(self.keyPressEvent)


        self.toolbar.addAction(newCrop)
        self.toolbar.addAction(saveJPG)
        self.toolbar.addAction(word)
        self.toolbar.addAction(excel)
        self.toolbar.addAction(exit)


        myQWidget.setLayout(layout)
        self.setCentralWidget(myQWidget)
        self.setWindowIcon(QtGui.QIcon('logo.png'))
        self.setWindowTitle('SnipPy')
        self.setGeometry(450, 300, 450, 300)


###################  FUNCTIONS  ######################

    def hideMainWindow(self):
        self.hide()
        self.ShowCropWindow = makeCrop.Crop(self)
        self.ShowCropWindow.show()


    def save_function(self, crop):
        if self.crop is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save as image', "", '*.png')
            if file_path:
                self.crop.save(file_path)
                print('saved')

    def word_function(self, crop):
        if crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', "", '*.docx')
            image_to_text.textTOword(path)
            # open word
            os.startfile(path)

    def excel_function(self, crop):
        if crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', "", '*.xlsx')
            temporary_excel_file = xlsxwriter.Workbook(path)
            temporary_excel_file.close()
            image_to_text.textTOexcel(path)
            # open excel
            os.startfile(path)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


###################  START THE APP  ##########################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainApp()

    welcome_info = QLabel(main)
    welcome_info.setText("ctrl+N = new crop\nctrl+S = save as jpg\nctrl+w = save in word\nctrl+e = save in excel\nesc = exit")
    welcome_info.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
    welcome_info.move(30, 60)
    welcome_info.adjustSize()

    main.show()
    sys.exit(app.exec_())
