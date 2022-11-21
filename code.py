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


flag=1
mobile_emulation = {
    "deviceMetrics": { "width": 350, "height": 600, "pixelRatio": 1.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_argument("window-size=400,600")
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
CHROMEDRIVER_PATH="F:\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options = chrome_options)



sites=['https://inspectapedia.com/']

for site in sites:

    try:
        driver.get(site)


        print("page loadded")
        time.sleep(15)

        

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
                
                try:
                    
                    path_class = driver.find_element(By.CLASS_NAME, "grippy-host")
                    # print(type(path_class))
                    element=path_class.get_attribute('innerHTML')
                    print(element)

                   
                    

                except:
                    print("not found popup")

               
                print("-------------------------------")
                print(style)
                a = style.get_attribute("name")
                result.append(a)
                # print(style.get_attribute("name"))
                # print(style.get_attribute("height"))
                width= style.get_attribute("width")
                # print(width)
            
                # print(style.get_attribute("style"))
                if width !='':
                    content = driver.find_element(By.ID, a)
                    find_parent = content.find_element(By.XPATH,'..')
                    driver = content._parent
                    driver.execute_script("arguments[0].scrollIntoView(true);", find_parent);
                    highlight(content, 5, 'red', 3)
                    img = Image.open('screenshot.png')
                    rimg = img.copy()
                    name=site[8:-1]
                    making_name = 'pic'+'_'+str(flag)+'.png' 
                    flag = flag+1
                    # saved_name='./scraped_images'+'/'+making_name+'.png'                     
                    rimg.save(making_name)
                # print("-------------------------------")
            elif "aswift" in iframe:
                
                print("-------------------------------")
                

                
               
                print("-------------------------------")
                a = style.get_attribute("name")
                result.append(a)
                # print(style.get_attribute("name"))
                # print(style.get_attribute("height"))
                width=style.get_attribute("width")
                print(width)
                # print(style.get_attribute("style"))

                # print(width)
                if width !='':
                    content = driver.find_element(By.ID, a)
                    find_parent = content.find_element(By.XPATH,'..')
                    driver = content._parent
                    driver.execute_script("arguments[0].scrollIntoView(true);", find_parent);
                    time.sleep(5)
                    try:

                        if style==getstyle[-1]:
                            path_class = driver.find_element(By.CLASS_NAME, "grippy-host").click()

                        path_class = driver.find_element(By.CLASS_NAME, "grippy-host").click()
                        



                    except:
                        print("not found popup")
                    
                    highlight(content, 5, 'red', 3)
                    img = Image.open('screenshot.png')
                    rimg = img.copy()
                    name=site[8:-1]
                    making_name = 'pic'+'_'+str(flag)+'.png' 
                    flag = flag+1
                    # saved_name='./scraped_images'+'/'+making_name+'.png'                     
                    rimg.save(making_name)
                # print("-------------------------------")
            else:
                print('no add found')



        

        # def opencv_handler(img):
        #     # Read input image
        #     get_image = img
        #     img = cv2.imread(img)
        

        #     # Gel all pixels in the image - where BGR = (34, 33, 33), OpenCV colors order is BGR not RGB
        #     gray = np.all(img == (0, 0, 255), 2)  # gray is a logical matrix with True where BGR = (34, 33, 33).

        #     # Convert logical matrix to uint8
        #     gray = gray.astype(np.uint8)*255

        #     # Find contours
        #     cnts = cv2.findContours(gray, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)[-2]  # Use index [-2] to be compatible to OpenCV 3 and 4

        #     # Get contour with maximum area
        #     c = max(cnts, key=cv2.contourArea)

        #     x, y, w, h = cv2.boundingRect(c)
        #     print(get_image+'=',w,h)
            
            
            


        # screenshots =glob.glob("scraped_images*/*.png")
        # print(screenshots) 


        # for image in screenshots:
        #     if site[8:-1] in image:
        #         opencv_handler(image)
       

    except WebDriverException:
        print("page down")