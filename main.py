#  do naprawy:
#  1. przesunięcie kursora
#  2. opacity
#  3. działanie excela
#  4. poprawienie jakości rozpoznawania tekstu
#  5. błąd kiedy raz się kliknie, a nie narysuje się prostokąta
#  6. usunąć automatyczne zapis

import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont

import xlsxwriter

import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import cv2

import makeCrop
import image_to_text

##############  SAVE CROP AND MAIN WINDOW  #################

class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

######################################################

        self.crop = None

######################################################

        myQWidget = QWidget()
        self.layout = QHBoxLayout()
        self.toolbar = self.addToolBar('toolbar')

        newCrop = QAction(QIcon('icons/new.png'), 'New', self)
        newCrop.setShortcut('Ctrl+N')
        newCrop.triggered.connect(self.hideMainWindow)

        load = QAction(QIcon('icons/load.png'), 'Load', self)
        load.setShortcut('Ctrl+O')
        load.triggered.connect(self.loadFunction)

        saveJPG = QAction(QIcon('icons/save.png'), 'Save', self)
        saveJPG.setShortcut('Ctrl+S')
        saveJPG.triggered.connect(self.saveFunction)

        word = QAction(QIcon('icons/word.png'), 'Word', self)
        word.setShortcut('Ctrl+W')
        word.triggered.connect(self.wordFunction)

        excel = QAction(QIcon('icons/excel.png'), 'Excel', self)
        excel.setShortcut('Ctrl+E')
        excel.triggered.connect(self.excelFunction)


        self.toolbar.addAction(newCrop)
        self.toolbar.addAction(load)
        self.toolbar.addAction(saveJPG)
        self.toolbar.addAction(word)
        self.toolbar.addAction(excel)


        myQWidget.setLayout(self.layout)
        self.setStyleSheet('background-color: white;')
        self.setCentralWidget(myQWidget)
        self.setWindowIcon(QIcon('icons/logo.png'))
        self.setWindowTitle('SnipPy')
        self.setGeometry(450, 300, 450, 300)
        self.setMinimumSize(450, 300)


        self.welcome_info = QLabel(myQWidget)
        self.welcome_info.setText('ctrl + N = new crop\nctrl + O = load image\nctrl + S = save as jpg\nctrl + W = save in word\nctrl + E = save in excel\nesc = exit')
        self.welcome_info.setFont(QFont('Arial', 10, QFont.Black))
        self.welcome_info.move(10, 10)
        self.welcome_info.adjustSize()

###################  FUNCTIONS  ######################

    def hideMainWindow(self):
        self.hide()
        self.ShowCropWindow = makeCrop.Crop(self)
        self.ShowCropWindow.show()

    def convertNumpyImg(self, npImg):
        height, width = npImg.shape
        bytesPerLine = 3 * width
        return QPixmap(QImage(npImg.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped())

    def displayImage(self, image):
        self.crop = image
        qImage = QImage(image.data, image.shape[1], image.shape[0], image.strides[0], QImage.Format_RGB888).rgbSwapped()
        self.welcome_info.setPixmap(QPixmap.fromImage(qImage))
        self.welcome_info.adjustSize()
        self.welcome_info.move(0, 0)
        self.welcome_info.setStyleSheet('padding :15px')
        self.resize(qImage.width() + 30, qImage.height() + self.toolbar.height() + 30)

    def loadFunction(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image files (*.jpg *.png)')
        self.crop = cv2.imread(path)
        img = QImage(path)
        self.welcome_info.setPixmap(QPixmap.fromImage(img))
        self.welcome_info.adjustSize()
        self.welcome_info.move(0, 0)
        self.welcome_info.setStyleSheet('padding :15px')
        self.resize(img.width() + 30, img.height() + self.toolbar.height() + 30)

    def saveFunction(self, crop):
        if self.crop is not None:
            crop = MainApp.convertNumpyImg(self, self.crop)
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save as image', '', '*.png')
            if file_path:
                crop.save(file_path)

    def wordFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.docx')
            image_to_text.textToWord(path, self.crop)
            # open word
            os.startfile(path)

    def excelFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.xlsx')
            temporary_excel_file = xlsxwriter.Workbook(path)
            temporary_excel_file.close()
            image_to_text.textToExcel(path, self.crop)
            # open excel
            os.startfile(path)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()


###################  START THE APP  ##########################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
