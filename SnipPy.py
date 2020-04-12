#   1. otwiera sie gui <WELCOME TO MY SNIPPY TOOL> -> opcje: NEW, SAVE, WORD, EXCEL
#   2. zaznaczanie kursorem określonej części ekranu
#   3. wyświetlić skórty klawiszowe na wejściu -> dlaczego nie są całe?
#   4. snipping musi oddawać crop
#   5. jak już będzie oddawał crop, trzeba zmienić produceText

# ZROBIONE:
#  - zapisywanie wycięcia jako png
#  - wychodzenie z apki
#  - przetwarzanie zdjęcia w text
#  - zapisywanie tekstu w pliku worda i otwieranie apki worda
#  - zapisywanie w excel i otwieranie apki excel

import sys
import os
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QFileDialog
from PyQt5 import QtGui, QtCore
from PyQt5.QtGui import QIcon

import xlsxwriter

import image_to_text
import mouse


class SnipPyApp(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle('SnipPy')
        self.toolbar = self.addToolBar('Save')

        newCrop = QAction(QIcon('new.png'), 'new', self)
        newCrop.setShortcut('Ctrl+N')
        newCrop.triggered.connect(self.new)

        saveJPG = QAction(QIcon('save.png'), 'save', self)
        saveJPG.setShortcut('Ctrl+S')
        saveJPG.triggered.connect(self.save)

        word = QAction(QIcon('word.png'), 'word', self)
        word.setShortcut('Ctrl+W')
        word.triggered.connect(self.word_function)

        excel = QAction(QIcon('excel.png'), 'excel', self)
        excel.setShortcut('Ctrl+E')
        excel.triggered.connect(self.excel_function)

        exit = QAction('exit', self)
        exit.triggered.connect(self.keyPressEvent)


        self.toolbar.addAction(saveJPG)
        self.toolbar.addAction(newCrop)
        self.toolbar.addAction(word)
        self.toolbar.addAction(excel)

        self.Snip = mouse.snipping()
        self.setGeometry(450,300, 450, 300)



    # chosen part of the screen
    import cv2
    crop = cv2.imread('przyklad.png', 0)


    # ------------ OPTIONS -----------
    def save(self, crop):
        if self.crop is not None:
            file_path, _ = QFileDialog.getSaveFileName(self, 'Save as image', "", '*.png')
            if file_path:
                self.crop.save(file_path)
                print('saved')

    def new(self, crop):

        # after snipping crop is given to produce text
        image_to_text.produceText(crop)


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


if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SnipPyApp()

    welcome_info = QLabel(window)
    welcome_info.setText("ctrl+N = new crop\nctrl+S = save as jpg\nctrl+w = save in word\nctrl+e = save in excel\nctrl+q or esc = exit")
    welcome_info.setFont(QtGui.QFont("Arial", 10, QtGui.QFont.Black))
    welcome_info.move(30, 60)

    window.show()
    sys.exit(app.exec_())
