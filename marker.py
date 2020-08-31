import sys, os
from PyQt5.QtWidgets import *
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage, QFont, QPainter, QPen, QBrush, QColor
from PyQt5.QtCore import Qt, QPoint
import cv2 as cv2

class Marker(QMainWindow):
    def __init__(self, parent, image):
        super(Marker, self).__init__(parent)

        myQwidget = QWidget()
        self.setWindowTitle('Marker')
        self.setWindowIcon(QIcon('icons/marker.png'))

        self.image = image
        self.display = QLabel(myQwidget)
        self.display.setPixmap(QPixmap.fromImage(self.image))
        self.display.move(0,0)
        self.display.setStyleSheet('padding:15px')
        self.resize(self.image.width(), self.image.height())

        self.drawing = False
        self.brushSize = 15
        self.brushColor = QColor(255, 255, 0, 10)
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

        fifeteenpxAction = QAction(QIcon(), '15px', self)
        mainMenu.addAction(fifeteenpxAction)
        fifeteenpxAction.triggered.connect(self.fifeteenPixel)

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
        self.parent().markerFunction()
        self.close()

    def fivePixel(self):
        self.brushSize = 5

    def ninePixel(self):
        self.brushSize = 9

    def fifeteenPixel(self):
        self.brushSize = 15

    def redColor(self):
        self.brushColor = QColor(255, 0, 0, 40)

    def yellowColor(self):
        self.brushColor = QColor(255, 255, 0, 100)

    def keyPressEvent(self, event):
        if event.key() == QtCore.Qt.Key_Escape:
            self.close()
