from PyQt5 import QtWidgets, QtCore, QtGui
from PyQt5.QtCore import Qt
import tkinter as tk
from PIL import ImageGrab
import numpy as np
import cv2

import SnipPy

class snipping(QtWidgets.QWidget):
    is_working = False

    def __init__(self, parent=None):
        super(snipping, self).__init__()
        self.parent = parent
        self.setWindowFlags(Qt.WindowStaysOnTopHint)

        root = tk.Tk()
        screen_width = root.winfo_screenwidth()
        screen_height = root.winfo_screenheight()
        self.setGeometry(0, 0, screen_width, screen_height)
        self.begin = QtCore.QPoint()
        self.end = QtCore.QPoint()


    def start(self):
        snipping.is_working = True
        self.setWindowOpacity(0.3)
        QtWidgets.QApplication.setOverrideCursor(QtGui.QCursor(QtCore.Qt.CrossCursor))
        self.show()

    def paintEvent(self, event):
        if snipping.is_working:
            brush_color = (128, 128, 255, 100)
            #lw = 3
            opacity = 0.3
        else:
            self.begin = QtCore.QPoint()
            self.end = QtCore.QPoint()
            brush_color = (0, 0, 0, 0)
            opacity = 0

        self.setWindowOpacity(opacity)
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

    def mouseReleaseEvent(self, event):
        snipping.is_working = False
        QtWidgets.QApplication.restoreOverrideCursor()

        x_start = min(self.begin.x(), self.end.x())
        y_start = min(self.begin.y(), self.end.y())
        x_end = max(self.begin.x(), self.end.x())
        y_end = max(self.begin.y(), self.end.y())

        self.repaint()
        QtWidgets.QApplication.processEvents()
        capturedImage = ImageGrab.grab(bbox=(x_start, y_start, x_end, y_end))
        QtWidgets.QApplication.processEvents()
        capturedImage = cv2.cvtColor(np.array(capturedImage), cv2.COLOR_BGR2RGB)
        SaveImage = cv2.imwrite('output_image.png', capturedImage)


        SnipPy.SnipPyApp(SaveImage)
