
# nuitka-project: --mode=standalone
# nuitka-project: --include-data-file={MAIN_DIRECTORY}/Example-Icon.png=Example-Icon.png

import os

import cv2 as cv
import numpy as np

img = cv.imread(cv.samples.findFile(os.path.join(os.path.dirname(__file__), 'Example-Icon.png')))

gray = cv.cvtColor(img,cv.COLOR_BGR2GRAY)
edges = cv.Canny(gray,50,150,apertureSize = 3)

lines = cv.HoughLines(edges,1,np.pi/180,20)

for line in lines:
 rho,theta = line[0]
 a = np.cos(theta)
 b = np.sin(theta)
 x0 = a*rho
 y0 = b*rho
 x1 = int(x0 + 1000*(-b))
 y1 = int(y0 + 1000*(a))
 x2 = int(x0 - 1000*(-b))
 y2 = int(y0 - 1000*(a))

 cv.line(img,(x1,y1),(x2,y2),(0,0,255),2)

 print("LINE", x1, x2, y1, y2, x0, y0)

