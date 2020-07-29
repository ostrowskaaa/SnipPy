#  do naprawy:
#  1. marker żółty
#  2. kułeczko w trakcie przetwarzania
#  *3. rysowanie tabeli
#  4. poprawienie jakości rozpoznawania tekstu
#  5. błąd kiedy raz się kliknie, a nie narysuje się prostokąta

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

######################################################

        self.crop = None
        self.drawing = False
        self.lastPoint = QPoint()
        self.run = False

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


        self.undo = QAction(QIcon('icons/undo.png'), 'Undo', self)
        self.undo.triggered.connect(self.undoFunction)
        self.redo = QAction(QIcon('icons/redo.png'), 'Redo', self)
        self.redo.triggered.connect(self.redoFunction)
        self.toolbar.addAction(self.undo)
        self.toolbar.addAction(self.redo)
        self.undo.setVisible(False)
        self.redo.setVisible(False)


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

    def convertNumpyImg(self, npImg):
        height, width, rgb = npImg.shape
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
        MainApp.displayImage(self, self.crop)

    def saveFunction(self, crop):
        if self.crop is not None:
            crop = MainApp.convertNumpyImg(self, self.crop)
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save as image', '', '*.png')
            if file_path:
                crop.save(file_path)
            else:
                raise OSError('No directory')

    def wordFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.docx')
            if path != '':
                image_to_text.textToWord(path, self.crop)
                # open word
                os.startfile(path)
            else:
                raise OSError('No directory')

    def excelFunction(self, crop):
        if self.crop is not None:
            path, _ = QFileDialog.getSaveFileName(self, 'Choose directory', '', '*.xlsx')
            if path != '':
                temporary_excel_file = xlsxwriter.Workbook(path)
                temporary_excel_file.close()
                image_to_text.textToExcel(path, self.crop)
                # open excel
                os.startfile(path)
            else:
                raise OSError('No directory')

### MARKER ###
    def markerFunction(self):
        if self.crop is not None:
            height, width, rgb = self.crop.shape
            bytesPerLine = 3 * width
            self.crop = QImage(self.crop.data, width, height, bytesPerLine, QImage.Format_RGB888).rgbSwapped()
            self.undo.setVisible(True)
            self.redo.setVisible(True)
            self.run = True
        else:
            raise OSError('No image')

    def mousePressEvent(self, event):
        if self.run:
            if event.button() == Qt.LeftButton:
                self.drawing = True
                self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if self.run:
            if(event.buttons() & Qt.LeftButton) & self.drawing:
                painter = QPainter(self.crop)
                painter.setPen(QPen(Qt.yellow, 7, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))   # 7 = brush size
                painter.drawLine(self.lastPoint, event.pos())
                self.lastPoint = event.pos()
                self.update()

    def mouseReleaseEvent(self, event):
        if self.run:
            if event.button() == Qt.LeftButton:
                self.drawing = False

    def paintEvent(self, event):
        if self.run:
            canvasPainter  = QPainter(self)
            canvasPainter.drawImage(0, self.crop, self.crop.rect())
###########################################################################


    def undoFunction(self):
        print('undo')

    def redoFunction(self):
        print('redo')

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()

###################  START THE APP  ##########################

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = MainApp()
    main.show()
    sys.exit(app.exec_())
