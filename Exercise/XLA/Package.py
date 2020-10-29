import os
import sys
import cv2
import math
import numpy as np
from PyQt5 import uic, QtGui
from matplotlib import pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *

class MyWindow(QMainWindow):
    def __init__(self):
        super(MyWindow,self).__init__()
        uic.loadUi('mid.ui',self)
        self.width = 941
        self.height = 511
        # Open file from folder
        layout = QVBoxLayout()
        self.browseImg = self.findChild(QPushButton, 'browseBtn')
        self.browseImg.clicked.connect(self.getfile)
        layout.addWidget(self.browseImg)
        self.labelImg = self.findChild(QLabel, 'ImageLabel')

        self.sizeImg = self.findChild(QComboBox, 'sizeCbb')
        self.typeImg = self.findChild(QComboBox, 'typeCbb')
        self.filterImg = self.findChild(QPushButton, 'filBtn')
        self.blurImg = self.findChild(QPushButton, 'blurBtn')
        self.sharpImg = self.findChild(QPushButton, 'sharpBtn')
        self.linearImg = self.findChild(QPushButton, 'linearBtn')
        self.logImg = self.findChild(QPushButton, 'logBtn')
        self.gammaImg = self.findChild(QPushButton, 'gammaBtn')
        self.salt_pepperImg = self.findChild(QPushButton, 'saltpepBtn')
        self.sobelImg = self.findChild(QPushButton, 'sobelBtn')
        self.prewittImg = self.findChild(QPushButton, 'prewittBtn')
        self.otsuImg = self.findChild(QPushButton, 'otsuBtn')
        self.binaryImg = self.findChild(QPushButton,'binaryBtn')
        self.truncImg = self.findChild(QPushButton, 'truncBtn')
        self.tozeroImg = self.findChild(QPushButton, 'tozeroBtn')

        self.filterImg.clicked.connect(self.type)
        self.blurImg.clicked.connect(self.blur)
        self.sharpImg.clicked.connect(self.sharpen)
        self.show()
    def getfile(self):
        fname = QFileDialog.getOpenFileName(self, 'Open file', 'c:\\','Image files(*.jpg *.png *.gif)')
        imagePath = fname[0]
        self.ffImage = imagePath
        self.labelImg.setPixmap(QPixmap(imagePath))
        # self.resize(pixmap.width(), pixmap.height())
    def cv_to_pixmap(self,cvImg):
        height, width, channel = cvImg.shape
        bytesPerLine = 3 * width
        qImg = QImage(cvImg.data, width, height, bytesPerLine, QImage.Format_RGB888)
        return qImg
    def type(self):
        image = self.ffImage
        value = self.sizeImg.currentIndex()*2+1
        if(self.typeImg.currentIndex() == 1):
            image = cv2.blur(self.ffImage, (value,value))
        elif(self.typeImg.currentIndex() == 2):
            image = cv2.GaussianBlur(self.ffImage, (value,value),0)
        elif(self.typeImg.currentIndex() == 3):
            image = cv2.medianBlur(self.ffImage,value)
        # cv2.imshow('test',image)
        self.labelImg.setPixmap(QPixmap(image))

    def light(self, Img,value):
        return Img+value
    def dark(self,Img,value):
        return Img+value
    def multiple(self,Img,value):
        return Img*value
    def log(self,Img):
        c=255/np.log(1+np.max(Img))
        log_Img = c*(np.log(Img+1))
        log_Img = np.array(log_Img,dtype=np.uint8)
        return log_Img

    def gamma(self,Img,gamma_vl=1.0):
        gamma_img = np.array(255*(Img/255)**gamma_vl,dtype='uint8')
        return gamma_img
    def power(self,Img,c,gamma_vl):
        gamma_img = np.array(c * (Img / 255) ** gamma_vl, dtype='uint8')
        return gamma_img

    def plotting_histogram(self,Img):
        plt.hist(Img.ravel(),256,[0,256])
        plt.show()
    def equal_histogram(self,Img):
        equal_hist_img = cv2.equalizeHist(Img)
        res = np.hstack((Img,equal_hist_img))
        return res
    def Ver_Ho(self):
        matrix_X = np.array([[0,0,0],
                          [-1,2,-1],
                          [0,0,0]])
        matrix_Y = np.array([[0,-1,0],
                             [0,2,0],
                             [0,-1,0]])
        Gx_image = cv2.filter2D(self.resize_img,-1,matrix_X)
        GY_image = cv2.filter2D(self.resize_img,-1,matrix_Y)
        XY_image = np.arctan(GY_image+Gx_image)
    def filter2D(self, Img, Matrix):
        ma = np.array([[0, 0, 0],
                       [1, 1, 1],
                       [0, 0, 0]])
        if Matrix == 5:
            ma = np.array([[0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0]])
        elif Matrix == 7:
            ma = np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]])
        reImg = cv2.filter2D(Img, -1, ma / Matrix)
        return reImg

    def gaussian_blur(self,Img,ksize=(5,5)):
        gau_blur_img = cv2.GaussianBlur(Img,ksize=ksize,dst=0)
        return gau_blur_img
    def blur(self):
        ksize = (5, 5)
        Img = self.ffImage
        blur_img = cv2.blur(Img,ksize=ksize)
        self.labelImg.setPixmap(QPixmap(blur_img))
    def median(self,Img,ksize=(5,5)):
        median_img = cv2.medianBlur(Img,ksize=ksize,dst=0)
    def sharpen(self):
        Img = self.ffImage
        filter = np.array([[-1, -1, -1],
                           [-1, 9, -1],
                           [-1, -1, -1]])
        sharpen_img = cv2.filter2D(Img,-1,filter)
        qimg = self.cv_to_pixmap(sharpen_img)
        self.labelImg.setPixmap(QPixmap(qimg))

    def ideal_lp(self,Img):
        sx, sy = Img.shape[:2]
        x = np.arange(-(sx) / 2, (sx) / 2)  # tâm là (0,0)
        y = np.arange(-(sy) / 2, (sy) / 2)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = d.copy()
        for i in range(0, d.shape[0]):
            for j in range(0, d.shape[1]):
                if d[i, j] <= 40:  # d0 = 100
                    H[i, j] = 1
                else:
                    H[i, j] = 0

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_ideal_lp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_ideal_lp = np.uint8(img_ideal_lp)
        return img_ideal_lp
    def butterworth_lp(self,Img,d0=50,n=2):
        sx, sy = Img.shape[:2]
        x = np.arange(-sx / 2, sx / 2)  # tâm là (0,0)
        y = np.arange(-sy / 2, sy / 2)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = d.copy()
        for i in range(0, d.shape[0]):
            for j in range(0, d.shape[1]):
                H[i, j] = 1 / (1 + (d[i, j] / d0) ** (2 * n))  # cho Do = 5, n =2

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_butterworth_lp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_butterworth_lp = np.uint8(img_butterworth_lp)
        return img_butterworth_lp
    def gaussian_lp(self,Img,sigma=50):
        sx, sy = Img.shape[:2]
        x = np.arange(-sy / 2, sy / 2)
        y = np.arange(-sx / 2, sx / 2)  # tâm là (0,0)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = pow(math.e, (-d ** 2 / (2 * (sigma ** 2))))  # cho sigma=50

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_gaussian_lp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_gaussian_lp = np.uint8(img_gaussian_lp)
        return img_gaussian_lp

    def ideal_hp(self,Img):
        sx, sy = Img.shape[:2]
        x = np.arange(-(sx) / 2, (sx) / 2)  # tâm là (0,0)
        y = np.arange(-(sy) / 2, (sy) / 2)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = d.copy()
        for i in range(0, d.shape[0]):
            for j in range(0, d.shape[1]):
                if d[i, j] <= 40:  # d0 = 100
                    H[i, j] = 0
                else:
                    H[i, j] = 1

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_ideal_hp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_ideal_hp = np.uint8(img_ideal_hp)
        return img_ideal_hp
    def butterworth_hp(self,Img,d0=50,n=2):
        sx, sy = Img.shape[:2]
        x = np.arange(-sx / 2, sx / 2)  # tâm là (0,0)
        y = np.arange(-sy / 2, sy / 2)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = d.copy()
        for i in range(0, d.shape[0]):
            for j in range(0, d.shape[1]):
                H[i, j] = 1 / (1 + (d0 / d[i, j]) ** (2 * n))  # cho Do = 5, n =2

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_butterworth_hp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_butterworth_hp = np.uint8(img_butterworth_hp)
        return img_butterworth_hp
    def gaussian_hp(self,Img,d0=50,sigma =50):
        sx, sy = Img.shape[:2]
        x = np.arange(-sx / 2, sx / 2)  # tâm là (0,0)
        y = np.arange(-sy / 2, sy / 2)

        x, y = np.meshgrid(x, y)
        d = np.sqrt(x ** 2 + y ** 2)

        H = 1 - pow(math.e, (-d ** 2 / (2 * (50 ** 2))))  # cho sigma=50

        g = np.fft.fftshift(np.fft.fft2(Img))  # fft and shift to center
        img_apply = g * H  # apply filter
        img_gaussian_hp = abs(np.fft.ifft2(np.fft.ifftshift(img_apply)))
        img_gaussian_hp = np.uint8(img_gaussian_hp <= d0)
        return img_gaussian_hp

    def threshold_binary(self,Img):
        ret, img_binary = cv2.threshold(Img, 127, 255, cv2.THRESH_BINARY)
        return img_binary
    def threshold_tozero(self,Img):
        ret, img_tozero = cv2.threshold(Img, 127, 255, cv2.THRESH_TOZERO)
        return img_tozero
    def threshold_trunc(self,Img):
        ret, img_trunc = cv2.threshold(Img, 127, 255, cv2.THRESH_TRUNC)
        return img_trunc
    def threshold_otsu(self,Img):
        ret, img_otsu = cv2.threshold(Img, 0, 255, cv2.THRESH_OTSU)
        return img_otsu
    def threshold_mean_C(self,Img):
        img_threshold = cv2.adaptiveThreshold(Img, 255, cv2.ADAPTIVE_THRESH_MEAN_C, \
                                              cv2.THRESH_BINARY, 11, 2)
        return img_threshold
    def threshold_gaussian_C(self,Img):
        img_gaussian = cv2.adaptiveThreshold(Img, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, \
                                             cv2.THRESH_BINARY, 11, 2)
        return img_gaussian
    def sobel(self,Img):
        hx = np.array([[1,0,-1],
                       [2,0,-2],
                       [1,0,-1]])
        hy = np.array([[1,2,1],
                       [0,0,0],
                       [-1,-2,-1]])
        sobelX = cv2.Sobel(Img, cv2.CV_8U,1,0,hx)
        sobelY = cv2.Sobel(Img, cv2.CV_8U,0,1,hy)
        sum = np.abs(sobelX) + np.abs(sobelY)
        Image_sobel = sum.astype(np.unit8)
        return Image_sobel
    def prewitt(self,Img):
        hx = np.array([[-1,0,1],
                       [-1,0,1],
                       [-1,0,1]])
        hy = np.array([[-1,-1,-1],
                       [0,0,0],
                       [1,1,1]])
        prewittX = cv2.filter2D(Img, -1, hx)
        prewittY = cv2.filter2D(Img, -1, hy)
        sum = np.abs(prewittX) + np.abs(prewittY)
        Image_prewitt = sum.astype(np.unit8)
        return Image_prewitt

app = QApplication(sys.argv)
go = MyWindow()
app.exec_()







