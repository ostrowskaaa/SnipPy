import numpy as np
import cv2
import matplotlib.pyplot as plt
import pytesseract
import csv

import pandas as pd
import os
import numpy as np
import cv2
import pytesseract
import csv
import pandas as pd
import os

import image_to_text

class Tables():
    def start(img, path):
        grayImg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        thresh, img_bin = cv2.threshold(grayImg,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        img_bin = 255 - img_bin

        #  vertical and horizontal kernels
        kernel_len = np.array(grayImg).shape[1]//100
        ver_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (1, kernel_len))
        hor_kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (kernel_len, 1))
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2,2))

        # detect lines
        img1 = cv2.erode(img_bin, ver_kernel, iterations = 3)
        vertical_lines = cv2.dilate(img1, ver_kernel, iterations = 3)
        img2 = cv2.erode(img_bin, hor_kernel, iterations = 3)
        horizontal_lines = cv2.dilate(img2, hor_kernel, iterations = 3)

        # combine horizontal and vertical lines in a new image
        lines = cv2.addWeighted(vertical_lines, 0.5, horizontal_lines, 0.5, 0.0)
        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 2))
        lines = cv2.erode(~lines, kernel, iterations=2)
        thresh, lines = cv2.threshold(lines,128,255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
        #cv2.imwrite('lines.png', lines)

        bitxor = cv2.bitwise_xor(grayImg, lines)
        bitnot = cv2.bitwise_not(bitxor)

        contours, hierarchy = cv2.findContours(lines, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

        def sort_contours(cnts, method='left-to-right'):
                # initialize the reverse flag and sort index
            reverse = False
            i = 0
                # handle if we are sorting against the y-coordinate rather than
                # the x-coordinate of the bounding box
            if method == 'top-to-bottom' or method == 'bottom-to-top':
                i = 1
                    # construct the list of bounding boxes and sort them from top to
                    # bottom
                boundingBoxes = [cv2.boundingRect(c) for c in cnts]
                (cnts, boundingBoxes) = zip(*sorted(zip(cnts, boundingBoxes),
                key=lambda b:b[1][i], reverse=reverse))
            # return the list of sorted contours and bounding boxes
            return (cnts, boundingBoxes)

            # Sort all the contours by top to bottom.
        contours, boundingBoxes = sort_contours(contours, method='top-to-bottom')
        #Creating a list of heights for all detected boxes
        heights = [boundingBoxes[i][3] for i in range(len(boundingBoxes))]
        mean = np.mean(heights)
        box = []
        for c in contours:
            x, y, w, h = cv2.boundingRect(c)
            if (w<1000 and h<500):
                image = cv2.rectangle(grayImg,(x,y),(x+w,y+h),(0,255,0),2)
                box.append([x,y,w,h])

            #Creating two lists to define row and column in which cell is located
        row=[]
        column=[]
        j=0
        #Sorting the boxes to their respective row and column
        for i in range(len(box)):
            if(i==0):
                column.append(box[i])
                previous=box[i]
            else:
                if(box[i][1]<=previous[1]+mean/2):
                    column.append(box[i])
                    previous=box[i]
                    if(i==len(box)-1):
                        row.append(column)
                else:
                    row.append(column)
                    column=[]
                    previous = box[i]
                    column.append(box[i])
            countcol = 0

        for i in range(len(row)):
            countcol = len(row[i])
            if countcol > countcol:
                countcol = countcol

        center = [int(row[i][j][0]+row[i][j][2]/2) for j in range(len(row[i])) if row[0]]
        center=np.array(center)
        center.sort()

            #Regarding the distance to the columns center, the boxes are arranged in respective order
        finalboxes = []
        for i in range(len(row)):
            lis=[]
            for k in range(countcol):
                lis.append([])
            for j in range(len(row[i])):
                diff = abs(center-(row[i][j][0]+row[i][j][2]/4))
                minimum = min(diff)
                indexing = list(diff).index(minimum)
                lis[indexing].append(row[i][j])
            finalboxes.append(lis)
            #from every single image-based cell/box the strings are extracted via pytesseract and stored in a list
        outer=[]
        for i in range(len(finalboxes)):
            for j in range(len(finalboxes[i])):
                inner=''
                if(len(finalboxes[i][j])==0):
                    outer.append(' ')
                else:
                    for k in range(len(finalboxes[i][j])):
                        y,x,w,h = finalboxes[i][j][k][0],finalboxes[i][j][k][1], finalboxes[i][j][k][2],finalboxes[i][j][k][3]
                        finalimg = bitnot[x:x+h, y:y+w]
                        kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (2, 1))
                        border = cv2.copyMakeBorder(finalimg,2,2,2,2,   cv2.BORDER_CONSTANT,value=[255,255])
                        resizing = cv2.resize(border, None, fx=2, fy=2, interpolation=cv2.INTER_CUBIC)
                        dilation = cv2.dilate(resizing, kernel,iterations=1)
                        erosion = cv2.erode(dilation, kernel,iterations=1)

                        out = pytesseract.image_to_string(erosion)
                        if(len(out)==0):
                            out = pytesseract.image_to_string(erosion, lang='eng+pol+jpn', config='--psm 3')
                        inner = inner +" "+ out
                    outer.append(inner)
        #Creating a dataframe of the generated OCR list
        arr = np.array(outer)
        dataframe = pd.DataFrame(arr.reshape(len(row),countcol))
        data = dataframe.style.set_properties(align='left')
        data.to_excel(path)
