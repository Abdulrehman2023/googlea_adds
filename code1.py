from selenium import webdriver
import base64
import time
import os
import codecs
from selenium.webdriver.common.by import By
from threading import Thread
from multiprocessing import Process
import cv2
import math
from PIL import Image, ImageDraw
import string
import random
from selenium.webdriver.chrome.options import Options
import glob
import numpy as np
from selenium.common.exceptions import WebDriverException



def opencv_handler(img):
    # Read input image
    img = cv2.imread(img)
    img2 = cv2.imread('image.png')

    # Gel all pixels in the image - where BGR = (34, 33, 33), OpenCV colors order is BGR not RGB
    gray = np.all(img == (0, 0, 255), 2)  # gray is a logical matrix with True where BGR = (34, 33, 33).

    # Convert logical matrix to uint8
    gray = gray.astype(np.uint8)*255

    # Find contours
    cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Use index [-2] to be compatible to OpenCV 3 and 4

    # Get contour with maximum area
    c = max(cnts, key=cv2.contourArea)

    x, y, w, h = cv2.boundingRect(c)
    print(x,y,w,h)
    # Draw green rectangle for testing
    # cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness = 2)
    # resized_down = cv2.resize(img2, (w,h), interpolation= cv2.INTER_LINEAR)
    # cv2.imwrite('resize.png', resized_down)
    # # Show result
    # resize_image = cv2.imread('resize.png')
    # img[y:y+h,x:x+w]=resize_image
    # random_name = ''.join(random.choices(string.ascii_uppercase +
    #                         string.digits, k=7))
    # saved_name='./results'+'/'+random_name+'.png'
    # cv2.imwrite(saved_name, img)
    


screenshots =glob.glob("scraped_images*/*.png") 


for image in screenshots:
    opencv_handler(image)
files = glob.glob('scraped_images/*')
        

