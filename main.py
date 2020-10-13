import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont, QPainter, QPen, QBrush
from PyQt5.QtCore import Qt, QPoint

import xlsxwriter

import tkinter as tk
from PIL import ImageGrab, Image
import numpy as np
import cv2

import makeCrop
import image_to_text
import marker

##############  SAVE CROP AND MAIN WINDOW  #################
class MainApp(QMainWindow):
    def __init__(self):
        super(MainApp, self).__init__()

        self.crop = None
######################################################
        myQWidget = QWidget()
        self.layout = QHBoxLayout()
        self.toolbar = self.addToolBar('toolbar')

        self.newCrop = QAction(QIcon('icons/new.png'), 'New', self)
        self.newCrop.setShortcut('Ctrl+N')
        self.newCrop.triggered.connect(self.makeCropFunction)

        self.load = QAction(QIcon('icons/load.png'), 'Load', self)
        self.load.setShortcut('Ctrl+O')
        self.load.triggered.connect(self.loadFunction)

        self.saveJPG = QAction(QIcon('icons/save.png'), 'Save', self)
        self.saveJPG.setShortcut('Ctrl+S')
        self.saveJPG.triggered.connect(self.saveFunction)

        self.word = QAction(QIcon('icons/word.png'), 'Word', self)
        self.word.setShortcut('Ctrl+W')
        self.word.triggered.connect(self.wordFunction)

        self.excel = QAction(QIcon('icons/excel.png'), 'Excel', self)
        self.excel.setShortcut('Ctrl+E')
        self.excel.triggered.connect(self.excelFunction)

        self.marker = QAction(QIcon('icons/marker.png'), 'Marker', self)
        self.marker.triggered.connect(self.markerFunction)

        self.toolbar.addAction(self.newCrop)
        self.toolbar.addAction(self.load)
        self.toolbar.addAction(self.saveJPG)
        self.toolbar.addAction(self.word)
        self.toolbar.addAction(self.excel)
        self.toolbar.addAction(self.marker)

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
    def makeCropFunction(self):
        self.hide()
        self.ShowCropWindow = makeCrop.Crop(self)
        self.ShowCropWindow.show()

    def convertToQimage(self, npImg):
        return QImage(npImg.data, npImg.shape[1], npImg.shape[0], npImg.strides[0], QImage.Format_RGB888).rgbSwapped()

    def displayImage(self, npImg):
        self.crop = npImg
        qImage = self.convertToQimage(self.crop)
        self.welcome_info.setPixmap(QPixmap.fromImage(qImage))
        self.welcome_info.adjustSize()
        self.welcome_info.move(0, 0)
        self.welcome_info.setStyleSheet('padding :15px')
        self.resize(qImage.width() + 30, qImage.height() + self.toolbar.height() + 30)

    def loadFunction(self):
        path, _ = QFileDialog.getOpenFileName(self, 'Open File', '', 'Image files (*.jpg *.png)')
        if path:
            self.crop = cv2.imread(path)
            self.displayImage(self.crop)

    def saveFunction(self, crop):
        if self.crop is not None:
            crop = QPixmap(self.convertToQimage(self.crop))
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save as image', '', '*.png')
            if path:
                crop.save(file_path)

    def wordFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.docx')
            if path:
                QApplication.setOverrideCursor(Qt.WaitCursor)
                image_to_text.textToWord(path, self.crop)
                # open word
                os.startfile(path)
                QApplication.restoreOverrideCursor()

    def excelFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.xlsx')
            if path:
                #QApplication.setOverrideCursor(Qt.WaitCursor)
                temporary_excel_file = xlsxwriter.Workbook(path)
                temporary_excel_file.close()
                image_to_text.textToExcel(path, self.crop)
                # open excel
                os.startfile(path)
                #QApplication.restoreOverrideCursor()

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

### MARKER ###
    def markerFunction(self):
        if self.crop is not None:
            self.image = self.convertToQimage(self.crop)
            self.image = marker.Marker(self, self.image)
            self.image.show()

    def displayMarkeredImg(self, markeredImg):
        self.crop = markeredImg
        self.displayImage(markeredImg)

###################  START THE APP  ##########################
if __name__ == '__main__':
    QApplication.setStyle('Fusion')
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
