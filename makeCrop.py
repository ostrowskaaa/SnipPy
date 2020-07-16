import sys, os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon, QPixmap, QImage

import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

###############  MAKE A CROP  ########################

class Crop(QMainWindow):
    is_working = False

    def __init__(self,parent):
        super(Crop, self).__init__(parent)
        self.setAttribute(QtCore.Qt.WA_DeleteOnClose)

        root = tk.Tk()
        cropWidget = QWidget()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()
        Crop.is_working = True
        self.setWindowOpacity(0.45)
        self.showFullScreen()
        QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))

    def paintEvent(self, event):
        if Crop.is_working:
            brush_color = (128, 128, 255, 100)
            paint = QtGui.QPainter(self)
            paint.setPen(QtGui.QPen(QtGui.QColor('black')))
            paint.setBrush(QtGui.QColor(*brush_color))
            rectangle = QtCore.QRectF(self.begin, self.end)
            paint.drawRect(rectangle)

    def mousePressEvent(self, event):
        self.begin = event.pos()
        self.end = self.begin
        self.update()

    def mouseMoveEvent(self, event):
        self.end = event.pos()
        self.update()

    # when you realease mouse
    def mouseReleaseEvent(self, event):
        Crop.is_working = False
        QApplication.restoreOverrideCursor()

        x_start = min(self.begin.x(), self.end.x())
        y_start = min(self.begin.y(), self.end.y())
        x_end = max(self.begin.x(), self.end.x())
        y_end = max(self.begin.y(), self.end.y())

        self.repaint()
        QApplication.processEvents()
        self.setWindowOpacity(0)
        capturedImage = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))
        QApplication.processEvents()
        capturedImage = cv2.cvtColor(np.array(capturedImage), cv2.COLOR_BGR2RGB)
        save = cv2.imwrite('captured_image.png', capturedImage)
        self.parent().displayImage(capturedImage)
        self.close()
        self.parent().show()
