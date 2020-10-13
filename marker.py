import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint
import cv2 as cv2
import numpy as np

class Marker(QMainWindow):
    def __init__(self, parent, image):
        super(Marker, self).__init__(parent)

        myQwidget = QWidget()
        self.setWindowTitle('Marker')
        self.setWindowIcon(QIcon('icons/marker.png'))

        self.original_image = image.copy()
        self.image = image.copy()
        self.resize(self.image.width(), self.image.height())

        self.drawing = False
        self.brushSize = 15
        self.brushColor = QColor(255, 255, 0, 70)
        self.lastPoint = QPoint()

        mainMenu = self.menuBar()

        saveAction = QAction(QIcon('icons/save.png'), 'Save',self)
        saveAction.setShortcut('Ctrl+S')
        mainMenu.addAction(saveAction)
        saveAction.triggered.connect(self.save)

        clearAction = QAction(QIcon('icons/clear.png'), 'Clear', self)
        clearAction.setShortcut('Ctrl+C')
        mainMenu.addAction(clearAction)
        clearAction.triggered.connect(self.clear)

        fivepxAction = QAction(QIcon('icons/fivepx.png'), '5px', self)
        mainMenu.addAction(fivepxAction)
        fivepxAction.triggered.connect(self.fivePixel)

        ninepxAction = QAction(QIcon(), '9px', self)
        mainMenu.addAction(ninepxAction)
        ninepxAction.triggered.connect(self.ninePixel)

        fifteenpxAction = QAction(QIcon(), '15px', self)
        mainMenu.addAction(fifteenpxAction)
        fifteenpxAction.triggered.connect(self.fifteenPixel)

        redAction = QAction(QIcon('icons/red.png'), 'Red', self)
        mainMenu.addAction(redAction)
        redAction.triggered.connect(self.redColor)

        yellowAction = QAction(QIcon('icons/yellow.png'), 'Yellow', self)
        mainMenu.addAction(yellowAction)
        yellowAction.triggered.connect(self.yellowColor)

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = True
            self.lastPoint = event.pos()

    def mouseMoveEvent(self, event):
        if(event.buttons() & Qt.LeftButton) & self.drawing:
            painter = QPainter(self.image)
            painter.setPen(QPen(self.brushColor, self.brushSize, Qt.SolidLine, Qt.RoundCap, Qt.RoundJoin))
            painter.drawLine(self.lastPoint, event.pos())
            self.lastPoint = event.pos()
            self.update()

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.drawing = False

    def paintEvent(self, event):
        canvasPainter  = QPainter(self)
        canvasPainter.drawImage(self.rect(),self.image, self.image.rect())

    def save(self):
        self.image.save('t.png','png')
        cv = cv2.imread('t.png')
        self.parent().displayMarkeredImg(cv)
        os.remove('t.png')
        self.close()

    def clear(self):
        self.image = self.original_image
        self.repaint()

    def fivePixel(self):
        self.brushSize = 5

    def ninePixel(self):
        self.brushSize = 9

    def fifteenPixel(self):
        self.brushSize = 15

    def redColor(self):
        self.brushColor = QColor(255, 0, 0, 40)

    def yellowColor(self):
        self.brushColor = QColor(255, 255, 0, 100)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
