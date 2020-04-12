import os
import cv2
import pytesseract

import pandas as pd

from docx import Document
from docx.shared import Inches

import SnipPy


text = None


def produceText(image):
    global text
    # 1 color image, 0 grey
    image = cv2.imread('przyklad.png', 0)
    image = cv2.threshold(image, 0,255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    #pytesseract.pytesseract.pytesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'
    text = pytesseract.image_to_string(image, lang="eng+pol+jpn", config=r'--oem 3 --psm 6')
    print(text)

    cv2.waitKey(0)
    cv2.destroyAllWindows()
    return text

def textTOword(path):
    global text
    if text is not None:
        doc = Document()
        doc.add_paragraph(text)
        doc.save(path)

def textTOexcel(path):
    global text
    if text is not None:
        with open('output.txt', "w+", encoding="utf-8") as file:
            file.write(text)

        df = pd.read_table('output.txt')
        df.to_excel(path, 'Sheet1', index=False)
    os.remove('output.txt')
    return df
