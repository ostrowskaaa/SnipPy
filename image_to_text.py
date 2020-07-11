import os
import cv2
import pytesseract

import pandas as pd
import numpy as np

from docx import Document
from docx.shared import Inches

import SnipPy
import detect_tables


def produceText(image):
    return pytesseract.image_to_string(image, lang='eng+pol+jpn', config=r'--oem 3 --psm 6')

def textToWord(path, img):
    text = produceText(img)
    if text is not None:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(path)

def textToExcel(path, img):
    cImage = np.copy(img)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    canny = cv2.Canny(gray, 50, 150)

    linesP = cv2.HoughLinesP(canny, 1, np.pi/180, 50, 350, 6)

    def is_vertical(line):
        return line[0]==line[2]
    def is_horizontal(line):
        return line[1]==line[3]

    horizontal_lines = []
    vertical_lines = []

    if linesP is not None:
        for i in range(0, len(linesP)):
            l = linesP[i][0]
            if (is_vertical(l)):
                vertical_lines.append(l)
            elif (is_horizontal(l)):
                horizontal_lines.append(l)

    for i, line in enumerate(horizontal_lines):
        cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,0), 2, cv2.LINE_AA)

    for i, line in enumerate(vertical_lines):
        cv2.line(cImage, (line[0], line[1]), (line[2], line[3]), (0,0,0), 2, cv2.LINE_AA)

    if len(vertical_lines) != 0 and len(horizontal_lines) != 0:
        detect_tables.Tables.start(img,path)
    else:
        text = produceText(img)
        if text is not None:
            with open('output.txt', 'w+', encoding='utf-8') as file:
                pytesseract.image_to_string(img, lang='eng+pol+jpn', config=r'--oem 3 --psm 6')
                file.write(text)
            df = pd.read_table('output.txt')
            df.to_excel(path, 'Sheet1', index=False)
            os.remove('output.txt')
