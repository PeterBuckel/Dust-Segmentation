import sys
from PyQt5.QtWidgets import QApplication, QLabel, QGridLayout, QWidget,QMainWindow
from PyQt5.QtGui import QPixmap
from PyQt5 import QtCore, QtGui, QtWidgets
import cv2
import matplotlib as plt
import os
from skimage import segmentation
import numpy as np
from skimage import morphology
import re

def atof(text):
    try:
        retval = float(text)
    except ValueError:
        retval = text
    return retval

def natural_keys(text):
    return [ atof(c) for c in re.split(r'[+-]?([0-9]+(?:[.][0-9]*)?|[.][0-9]+)', text) ]


input_folder = "C:/Users/bucke/PycharmProjects/GUI_dustlabeling/input"
frame = []
for subdir, dirs, files in os.walk(input_folder):
    files.sort(key=natural_keys)
    print(files)
    for file in files:
        img = os.path.join(subdir, file)
        if img is not None:
            frame.append(img)
print(frame)
cv2.namedWindow('image', cv2.WINDOW_NORMAL)        # Create window with freedom of dimensions
cv2.resizeWindow('image', 512, 512)
count = 0

img = cv2.imread(frame[count])
print(frame[count])
img = cv2.resize(img, (512, 512), interpolation=cv2.INTER_LINEAR)
img = cv2.cvtColor(img,cv2.COLOR_BGR2HSV)
h,s,v = cv2.split(img)
clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16,16))
s1 = clahe.apply(s)
v1= clahe.apply(v)
orgnew2 = cv2.merge((h,s1,v1))
img = cv2.cvtColor(orgnew2,cv2.COLOR_HSV2BGR)
cv2.imshow('image', img)
count += 1
value = 0


dcp_sp = np.zeros(img.shape[:2])
segments = np.zeros(img.shape[:2])
th1 = np.zeros(img.shape[:2])
newimg = np.zeros(img.shape[:2])
newimg_inv = np.zeros(img.shape[:2])
newimg_color = np.zeros(img.shape[:2])
color_mask = np.zeros(img.shape[:2])
Llval = 100
Lhval = 200
Alval = 100
Ahval = 150
Blval = 103
Bhval = 150
bin_value = 80
class Ui_Form(object):

    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(317, 495)
        self.thresh_Slider = QtWidgets.QSlider(Form)
        self.thresh_Slider.setGeometry(QtCore.QRect(70, 100, 160, 22))
        self.thresh_Slider.setAcceptDrops(False)
        self.thresh_Slider.setAutoFillBackground(True)
        self.thresh_Slider.setMinimum(0)
        self.thresh_Slider.setMaximum(255)
        self.thresh_Slider.setSliderPosition(bin_value)
        self.thresh_Slider.setValue(bin_value)
        self.thresh_Slider.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.thresh_Slider.setTickInterval(10)
        self.thresh_Slider.setOrientation(QtCore.Qt.Horizontal)
        self.thresh_Slider.setObjectName("thresh_Slider")
        self.thresh_Slider.valueChanged[int].connect(self.thresh_valuechange)

        self.thresh = QtWidgets.QCheckBox(Form)
        self.thresh.setGeometry(QtCore.QRect(100, 70, 70, 17))
        self.thresh.setObjectName("thresh")
        self.thresh.stateChanged.connect(self.thresh_m)

        self.dcp = QtWidgets.QCheckBox(Form)
        self.dcp.setGeometry(QtCore.QRect(100, 40, 121, 17))
        self.dcp.setObjectName("dcp")
        self.dcp.stateChanged.connect(self.dcp_m)

        self.color = QtWidgets.QCheckBox(Form)
        self.color.setGeometry(QtCore.QRect(90, 150, 121, 17))
        self.color.setObjectName("color")
        self.color.stateChanged.connect(self.color_m)

        self.image_field = QtWidgets.QLabel(Form)
        self.image_field.setGeometry(QtCore.QRect(260, 20, 791, 611))
        self.image_field.setText("")
        self.image_field.setObjectName("image_field")

        self.NextImage = QtWidgets.QPushButton(Form)
        self.NextImage.setGeometry(QtCore.QRect(110, 460, 75, 23))
        self.NextImage.setObjectName("NextImage")
        self.NextImage.clicked.connect(self.NextImg)

        self.label_thresh = QtWidgets.QLabel(Form)
        self.label_thresh.setGeometry(QtCore.QRect(140, 130, 21, 16))
        self.label_thresh.setObjectName("label_thresh")

        self.L_low = QtWidgets.QSlider(Form)
        self.L_low.setAcceptDrops(False)
        self.L_low.setAutoFillBackground(True)
        self.L_low.setMinimum(0)
        self.L_low.setMaximum(255)
        self.L_low.setSliderPosition(100)
        self.L_low.setValue(100)
        self.L_low.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.L_low.setTickInterval(10)
        self.L_low.setGeometry(QtCore.QRect(20, 210, 22, 160))
        self.L_low.setOrientation(QtCore.Qt.Vertical)
        self.L_low.setObjectName("L_low")
        self.L_low.valueChanged[int].connect(self.thresh_L_Low)
        self.L_High = QtWidgets.QSlider(Form)
        self.L_High.setAcceptDrops(False)
        self.L_High.setAutoFillBackground(True)
        self.L_High.setMinimum(0)
        self.L_High.setMaximum(255)
        self.L_High.setSliderPosition(200)
        self.L_High.setValue(200)
        self.L_High.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.L_High.setTickInterval(10)
        self.L_High.setGeometry(QtCore.QRect(60, 210, 22, 160))
        self.L_High.setOrientation(QtCore.Qt.Vertical)
        self.L_High.setObjectName("L_High")
        self.L_High.valueChanged[int].connect(self.thresh_L_High)

        self.A_Low = QtWidgets.QSlider(Form)
        self.A_Low.setAcceptDrops(False)
        self.A_Low.setAutoFillBackground(True)
        self.A_Low.setMinimum(0)
        self.A_Low.setMaximum(255)
        self.A_Low.setSliderPosition(100)
        self.A_Low.setValue(100)
        self.A_Low.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.A_Low.setTickInterval(10)
        self.A_Low.setGeometry(QtCore.QRect(120, 210, 22, 160))
        self.A_Low.setOrientation(QtCore.Qt.Vertical)
        self.A_Low.setObjectName("A_Low")
        self.A_Low.valueChanged[int].connect(self.thresh_A_Low)
        self.A_High = QtWidgets.QSlider(Form)
        self.A_High.setAcceptDrops(False)
        self.A_High.setAutoFillBackground(True)
        self.A_High.setMinimum(0)
        self.A_High.setMaximum(255)
        self.A_High.setSliderPosition(150)
        self.A_High.setValue(150)
        self.A_High.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.A_High.setTickInterval(10)
        self.A_High.setGeometry(QtCore.QRect(160, 210, 22, 160))
        self.A_High.setOrientation(QtCore.Qt.Vertical)
        self.A_High.setObjectName("A_High")
        self.A_High.valueChanged[int].connect(self.thresh_A_High)

        self.B_Low = QtWidgets.QSlider(Form)
        self.B_Low.setAcceptDrops(False)
        self.B_Low.setAutoFillBackground(True)
        self.B_Low.setMinimum(0)
        self.B_Low.setMaximum(255)
        self.B_Low.setSliderPosition(103)
        self.B_Low.setValue(103)
        self.B_Low.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.B_Low.setTickInterval(10)
        self.B_Low.setGeometry(QtCore.QRect(230, 210, 22, 160))
        self.B_Low.setOrientation(QtCore.Qt.Vertical)
        self.B_Low.setObjectName("B_Low")
        self.B_Low.valueChanged[int].connect(self.thresh_B_Low)
        self.B_High = QtWidgets.QSlider(Form)
        self.B_High.setAcceptDrops(False)
        self.B_High.setAutoFillBackground(True)
        self.B_High.setMinimum(0)
        self.B_High.setMaximum(255)
        self.B_High.setSliderPosition(150)
        self.B_High.setValue(150)
        self.B_High.setTickPosition(QtWidgets.QSlider.TicksBelow)
        self.B_High.setTickInterval(10)
        self.B_High.setGeometry(QtCore.QRect(270, 210, 22, 160))
        self.B_High.setOrientation(QtCore.Qt.Vertical)
        self.B_High.setObjectName("B_High")
        self.B_High.valueChanged[int].connect(self.thresh_B_High)

        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(30, 190, 47, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(130, 190, 51, 16))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(240, 190, 51, 16))
        self.label_4.setObjectName("label_4")

        self.L_Low_val = QtWidgets.QLabel(Form)
        self.L_Low_val.setGeometry(QtCore.QRect(20, 390, 21, 16))
        self.L_Low_val.setObjectName("L_Low_val")
        self.L_low_2 = QtWidgets.QLabel(Form)
        self.L_low_2.setGeometry(QtCore.QRect(20, 370, 21, 16))
        self.L_low_2.setObjectName("L_low_2")
        self.L_High_2 = QtWidgets.QLabel(Form)
        self.L_High_2.setGeometry(QtCore.QRect(60, 370, 21, 16))
        self.L_High_2.setObjectName("L_High_2")
        self.A_Low_2 = QtWidgets.QLabel(Form)
        self.A_Low_2.setGeometry(QtCore.QRect(120, 370, 21, 16))
        self.A_Low_2.setObjectName("A_Low_2")
        self.A_High_2 = QtWidgets.QLabel(Form)
        self.A_High_2.setGeometry(QtCore.QRect(160, 370, 21, 16))
        self.A_High_2.setObjectName("A_High_2")
        self.B_Low_2 = QtWidgets.QLabel(Form)
        self.B_Low_2.setGeometry(QtCore.QRect(230, 370, 21, 16))
        self.B_Low_2.setObjectName("B_Low_2")
        self.B_High_2 = QtWidgets.QLabel(Form)
        self.B_High_2.setGeometry(QtCore.QRect(270, 370, 21, 16))
        self.B_High_2.setObjectName("B_High_2")
        self.L_High_val = QtWidgets.QLabel(Form)
        self.L_High_val.setGeometry(QtCore.QRect(60, 390, 21, 16))
        self.L_High_val.setObjectName("L_High_val")
        self.A_Low_val = QtWidgets.QLabel(Form)
        self.A_Low_val.setGeometry(QtCore.QRect(120, 390, 21, 16))
        self.A_Low_val.setObjectName("A_Low_val")
        self.A_High_val = QtWidgets.QLabel(Form)
        self.A_High_val.setGeometry(QtCore.QRect(160, 390, 21, 16))
        self.A_High_val.setObjectName("A_High_val")
        self.B_Low_val = QtWidgets.QLabel(Form)
        self.B_Low_val.setGeometry(QtCore.QRect(230, 390, 21, 16))
        self.B_Low_val.setObjectName("B_Low_val")
        self.B_High_val = QtWidgets.QLabel(Form)
        self.B_High_val.setGeometry(QtCore.QRect(270, 390, 21, 16))
        self.B_High_val.setObjectName("B_High_val")

        self.Removeholes = QtWidgets.QCheckBox(Form)
        self.Removeholes.setGeometry(QtCore.QRect(10, 420, 91, 17))
        self.Removeholes.setObjectName("Removeholes")
        self.Removeholes.stateChanged.connect(self.remholes)

        self.FloodFill = QtWidgets.QCheckBox(Form)
        self.FloodFill.setGeometry(QtCore.QRect(10, 440, 70, 17))
        self.FloodFill.setObjectName("FloodFill")
        self.FloodFill.stateChanged.connect(self.floddfill)

        self.Erosion = QtWidgets.QCheckBox(Form)
        self.Erosion.setGeometry(QtCore.QRect(230, 420, 70, 17))
        self.Erosion.setObjectName("Erosion")
        self.Erosion.stateChanged.connect(self.erosion)

        self.Dilation = QtWidgets.QCheckBox(Form)
        self.Dilation.setGeometry(QtCore.QRect(230, 440, 70, 17))
        self.Dilation.setObjectName("Dilation")
        self.Dilation.stateChanged.connect(self.dilation)

        self.Closing = QtWidgets.QCheckBox(Form)
        self.Closing.setGeometry(QtCore.QRect(130, 420, 70, 17))
        self.Closing.setObjectName("Closing")
        self.Closing.stateChanged.connect(self.closing)

        self.Opening = QtWidgets.QCheckBox(Form)
        self.Opening.setGeometry(QtCore.QRect(130, 440, 70, 17))
        self.Opening.setObjectName("Opening")
        self.Opening.stateChanged.connect(self.opening)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def opening(self):
        if self.Opening.isChecked() == True:
            global newimg_color
            global color_mask
            kernel = np.ones((3, 3), np.uint8)
            color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_OPEN, kernel, iterations=1, borderType=cv2.BORDER_CONSTANT,borderValue =(0,0,0))
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def closing(self):
        if self.Closing.isChecked() == True:
            global newimg_color
            global color_mask
            kernel = np.ones((3, 3), np.uint8)
            color_mask = cv2.morphologyEx(color_mask, cv2.MORPH_CLOSE, kernel, iterations=1, borderType=cv2.BORDER_CONSTANT,borderValue =(0,0,0))
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def dilation(self):
        if self.Dilation.isChecked() == True:
            global newimg_color
            global color_mask
            kernel = np.ones((3, 3), np.uint8)
            color_mask = cv2.dilate(color_mask, kernel, iterations=1, borderType=cv2.BORDER_CONSTANT,borderValue =(0,0,0))
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def erosion(self):
        if self.Erosion.isChecked() == True:
            global newimg_color
            global color_mask
            kernel = np.ones((3, 3), np.uint8)
            color_mask = cv2.erode(color_mask, kernel, iterations=1,borderType=cv2.BORDER_CONSTANT, borderValue =(0,0,0))
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def remholes(self):
        if self.Removeholes.isChecked() == True:
            global newimg_color
            global color_mask
            color_mask = morphology.area_opening(color_mask, area_threshold=6400, connectivity=1, parent=None, tree_traverser=None)
            #color_mask = morphology.remove_small_holes(color_mask, 100000)
            color_mask = color_mask * 255
            color_mask = color_mask.astype('uint8')
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def floddfill(self):
        if self.FloodFill.isChecked() == True:
            global newimg_color
            global color_mask
            h, w = color_mask.shape[:2]
            seed_point = 250,300#300,250#240,155#970, 620  # 387,314 #250,290#
            temp = np.zeros((h+2, w+2), np.uint8)
            cv2.floodFill(color_mask, temp, seed_point, 255, flags=cv2.FLOODFILL_MASK_ONLY)
            color_mask = temp * 255
            color_mask = color_mask.astype('uint8')
            color_mask = color_mask[1: h + 1, 1: w + 1]
            #print(np.shape(color_mask))
            #color_mask = cv2.resize(color_mask, (512, 512), interpolation=cv2.INTER_LINEAR)  # 76
            print(np.shape(color_mask))
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def thresh_valuechange(self, value):
        global newimg
        global newimg_inv
        global bin_value
        ret, th1 = cv2.threshold(dcp_sp, value, 255, cv2.THRESH_BINARY_INV)
        newimg = cv2.bitwise_and(img, img, mask=th1)
        th1_inv = cv2.bitwise_not(th1)
        th1_inv = morphology.remove_small_holes(th1_inv, 100000)
        th1_inv  = th1_inv  * 255
        th1_inv  = th1_inv.astype('uint8')
        newimg_inv = cv2.bitwise_and(img, img, mask=th1_inv)
        self.label_thresh.setText(str(value))
        bin_value = value
        cv2.imshow('image', newimg_inv)

    def thresh_L_Low(self, value):
        global Llval
        Llval = value
        self.L_Low_val.setText(str(value))
        self.color_m()
    def thresh_L_High(self, value):
        global Lhval
        Lhval = value
        self.L_High_val.setText(str(value))
        self.color_m()
    def thresh_A_Low(self, value):
        global Alval
        Alval = value
        self.A_Low_val.setText(str(value))
        self.color_m()
    def thresh_A_High(self, value):
        global Ahval
        Ahval = value
        self.A_High_val.setText(str(value))
        self.color_m()
    def thresh_B_Low(self, value):
        global Blval
        Blval = value
        self.B_Low_val.setText(str(value))
        self.color_m()
    def thresh_B_High(self, value):
        global Bhval
        Bhval = value
        self.B_High_val.setText(str(value))
        self.color_m()

    def NextImg(self):
        global count
        global img
        global dcp_sp
        global segments
        global th1
        global newimg
        global newimg_inv
        global newimg_color
        global color_mask
        color_mask = cv2.resize(color_mask, (512, 512), interpolation=cv2.INTER_AREA)#, fx=4, fy=4)
        print(np.unique(color_mask))
        cv2.imwrite('C:/Users/bucke/PycharmProjects/GUI_dustlabeling/output/img_1 ('+str(count)+').png', color_mask)
        img = cv2.imread(frame[count])
        img = cv2.resize(img, (512,512), interpolation=cv2.INTER_LINEAR)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(img)
        clahe = cv2.createCLAHE(clipLimit=2.0, tileGridSize=(16, 16))
        s1 = clahe.apply(s)
        v1 = clahe.apply(v)
        orgnew2 = cv2.merge((h, s1, v1))
        img = cv2.cvtColor(orgnew2, cv2.COLOR_HSV2BGR)
        cv2.imshow('image', img)

        ##### Reset All #####
        self.dcp.setChecked(False)
        self.color.setChecked(False)
        self.thresh.setChecked(False)
        self.FloodFill.setChecked(False)
        self.Removeholes.setChecked(False)
        self.Erosion.setChecked(False)
        self.Dilation.setChecked(False)
        self.Closing.setChecked(False)
        self.Opening.setChecked(False)

        dcp_sp = np.zeros(img.shape[:2])
        segments = np.zeros(img.shape[:2])
        th1 = np.zeros(img.shape[:2])
        newimg = np.zeros(img.shape[:2])
        newimg_inv = np.zeros(img.shape[:2])
        newimg_color = np.zeros(img.shape[:2])
        color_mask = np.zeros(img.shape[:2])
        count += 1

    def dcp_m(self, Form):
        #printing the checked status
        if self.dcp.isChecked() == True:
            segments = segmentation.slic(img, n_segments=5000,max_num_iter=100, sigma=0, convert2lab=True)
            global dcp_sp
            for i in np.unique(segments):
                mask = np.zeros(segments.shape[:2])
                mask = mask.astype('uint8')
                mask[segments == i] = 255
                img_masked = cv2.bitwise_and(img, img, mask=mask)
                b, g, r = cv2.split(img_masked)
                dc = cv2.min(cv2.min(r, g), b)
                img_mask = dc[np.where(mask == 255)]
                img_min = np.min(img_mask, axis=0)
                dcp_sp[mask == 255] = img_min

            dcp_sp = dcp_sp.astype('uint8')
            cv2.imshow('image', dcp_sp)

    def thresh_m(self):
        # printing the checked status
        if self.thresh.isChecked() == True:
            global newimg
            global newimg_inv
            ret, th1 = cv2.threshold(dcp_sp, bin_value, 255, cv2.THRESH_BINARY_INV)
            newimg = cv2.bitwise_and(img, img, mask=th1)
            th1_inv = cv2.bitwise_not(th1)
            newimg_inv = cv2.bitwise_and(img, img, mask=th1_inv)
            #newimg_inv = cv2.blur(newimg_inv, (3, 3))
            cv2.imshow('image', newimg_inv)

    def color_m(self):
        # printing the checked status
        if self.color.isChecked() == True:
            global newimg_color
            global color_mask
            newimg_lab = cv2.cvtColor(newimg_inv, cv2.COLOR_BGR2LAB)
            lowerRange = np.array([Llval, Alval, Blval], dtype="uint8")  # [100, 100, 103]
            upperRange = np.array([Lhval, Ahval, Bhval], dtype="uint8")  # [200, 150, 140]
            mask_color_extraction = cv2.inRange(newimg_lab, lowerRange, upperRange)
            kernel = np.ones((3, 3), np.uint8)
            opening = cv2.morphologyEx(mask_color_extraction, cv2.MORPH_OPEN, kernel, iterations=1, borderType=cv2.BORDER_CONSTANT,borderValue =(0,0,0))
            cleaned = morphology.remove_small_holes(opening, 100000)
            color_mask = cleaned*255
            color_mask = color_mask.astype('uint8')
            newimg_color = cv2.bitwise_and(newimg_inv, newimg_inv, mask=color_mask)
            cv2.imshow('image', newimg_color)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.thresh.setText(_translate("Form", "Threshold"))
        self.dcp.setText(_translate("Form", "Dark Channel Prior"))
        self.color.setText(_translate("Form", "Color Segmentation"))
        self.NextImage.setText(_translate("Form", "Next Image"))
        self.label_thresh.setText(_translate("Form", "80"))
        self.label_2.setText(_translate("Form", "L-Channel"))
        self.label_3.setText(_translate("Form", "A-Channel"))
        self.label_4.setText(_translate("Form", "B-Channel"))
        self.L_Low_val.setText(_translate("Form", "100"))
        self.L_low_2.setText(_translate("Form", "Low"))
        self.L_High_2.setText(_translate("Form", "High"))
        self.A_Low_2.setText(_translate("Form", "Low"))
        self.A_High_2.setText(_translate("Form", "High"))
        self.B_Low_2.setText(_translate("Form", "Low"))
        self.B_High_2.setText(_translate("Form", "High"))
        self.L_High_val.setText(_translate("Form", "200"))
        self.A_Low_val.setText(_translate("Form", "100"))
        self.A_High_val.setText(_translate("Form", "150"))
        self.B_Low_val.setText(_translate("Form", "103"))
        self.B_High_val.setText(_translate("Form", "150"))
        self.Removeholes.setText(_translate("Form", "Remove Holes"))
        self.FloodFill.setText(_translate("Form", "FloodFill"))
        self.Erosion.setText(_translate("Form", "Erosion"))
        self.Dilation.setText(_translate("Form", "Dilation"))
        self.Closing.setText(_translate("Form", "Closing"))
        self.Opening.setText(_translate("Form", "Opening"))




def main():
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_Form()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec())
main()


