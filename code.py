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

options = Options()

options.headless = True
options.add_argument("window-size=1400,600")
CHROMEDRIVER_PATH="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe"
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
driver.get("https://doggies.com/")
print("page loadded")
time.sleep(15)




html = driver.page_source
n = os.path.join("C:\\Users\\FabTechSol\\Desktop\\screenshot\\html", "PageSave.html")
f = codecs.open(n, "w", "utf−8")
f.write(html)


getstyle = driver.find_elements(By.TAG_NAME, 'iframe')
result = []

def apply_style(s,element):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)

def highlight(element, effect_time, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color),element)
    time.sleep(effect_time)
    driver.save_screenshot('screenshot.png')
    apply_style(original_style,element)


for style in getstyle:
    iframe = style.get_attribute("name")
    if "google_ads_iframe" in iframe:
        print("-------------------------------")
        print(style)
        a = style.get_attribute("name")
        result.append(a)
        print(style.get_attribute("name"))
        print(style.get_attribute("height"))
        width= style.get_attribute("width")
        print(width)
       
        print(style.get_attribute("style"))
        if width !='':
            content = driver.find_element(By.ID, a)
            driver = content._parent
            driver.execute_script("arguments[0].scrollIntoView(true);", content);
            highlight(content, 5, 'red', 1)
            
            x,y = content.location.values()
            h,w = content.size.values()
            print(x,y,w, h)
            img = Image.open('screenshot.png')
            rimg = img.copy()
            
            random_name = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=7))
            saved_name='./scraped_images'+'/'+random_name+'.png'                     
            rimg.save(saved_name)
        print("-------------------------------")
    elif "aswift" in iframe:
        print("-------------------------------")
        print(style)
        a = style.get_attribute("name")
        result.append(a)
        print(style.get_attribute("name"))
        print(style.get_attribute("height"))
        width=style.get_attribute("width")
        print(style.get_attribute("style"))

        print(width)
        if width !='':
            content = driver.find_element(By.ID, a)
            driver = content._parent
            driver.execute_script("arguments[0].scrollIntoView(true);", content);
            highlight(content, 5, 'red', 1)
            
            x,y = content.location.values()
            h,w = content.size.values()
            print(x,y,w, h)
            img = Image.open('screenshot.png')
            rimg = img.copy()
            
            random_name = ''.join(random.choices(string.ascii_uppercase +
                                string.digits, k=7))
            saved_name='./scraped_images'+'/'+random_name+'.png'                     
            rimg.save(saved_name)
        print("-------------------------------")
    else:
        print('no add found')



print(result)

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
    resized_down = cv2.resize(img2, (w,h), interpolation= cv2.INTER_LINEAR)
    cv2.imwrite('resize.png', resized_down)
    # Show result
    resize_image = cv2.imread('resize.png')
    img[y:y+h,x:x+w]=resize_image
    random_name = ''.join(random.choices(string.ascii_uppercase +
                            string.digits, k=7))
    saved_name='./results'+'/'+random_name+'.png'
    cv2.imwrite(saved_name, img)
    # cv2.imshow('gray', gray)
    # cv2.imshow('img', img)
    # cv2.imshow('img2', img2)
    # cv2.imshow('img3', img3)
    # cv2.waitKey(0)
    # cv2.destroyAllWindows()



screenshots =glob.glob("scraped_images*/*.png") 


for image in screenshots:
    opencv_handler(image)

print("end")