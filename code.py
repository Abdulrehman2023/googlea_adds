from selenium import webdriver
import base64
import time
import os
import codecs
driver = webdriver.Chrome(executable_path="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe")
from selenium.webdriver.common.by import By
from threading import Thread
from multiprocessing import Process
import cv2
import math
from PIL import Image, ImageDraw


driver.get("https://animalfactguide.com/")
print("page loadded")
time.sleep(10)
# driver.fullscreen_window()

# page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
# print("matrices get")
# time.sleep(5)
# screenshot = driver.execute_cdp_cmd(
#             "Page.captureScreenshot",
#             {
#                 "format": "png",
#                 "captureBeyondViewport": True,
#                 "clip": {
#                     "width": page_rect["contentSize"]["width"],
#                     "height": page_rect["contentSize"]["height"],
#                     "x": 0,
#                     "y": 0,
#                     "scale": 1
#                 }
#             })
# print("screenshot is taken")

# with open('C:\\Users\\FabTechSol\\Desktop\\screenshot\\list\\new.png', "wb") as file:
#     file.write(base64.urlsafe_b64decode(screenshot["data"]))

# html = driver.page_source
# n = os.path.join("C:\\Users\\FabTechSol\\Desktop\\screenshot\\html", "PageSave.html")
# f = codecs.open(n, "w", "utf−8")
# f.write(html)
# driver.save_screenshot('screenshot.png')

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
        print(style.get_attribute("width"))
        print(style.get_attribute("style"))
        content = driver.find_element(By.ID, a)
        driver.execute_script("arguments[0].scrollIntoView(true);", content);
        highlight(content, 5, 'red', 5)
        
        x,y = content.location.values()
        h,w = content.size.values()
        print(x,y,w, h)
        img = Image.open('screenshot.png')
        rimg = img.copy()
        rimg.show()
        rimg.save('pillow.png')
        print("-------------------------------")
    elif "aswift" in iframe:
        print("-------------------------------")
        print(style)
        a = style.get_attribute("name")
        result.append(a)
        print(style.get_attribute("name"))
        print(style.get_attribute("height"))
        print(style.get_attribute("width"))
        print(style.get_attribute("style"))
        content = driver.find_element(By.ID, a)
        driver.execute_script("arguments[0].scrollIntoView(true);", content);
        highlight(content, 5, 'red', 5)
        
        x,y = content.location.values()
        h,w = content.size.values()
        print(x,y,w, h)
        img = Image.open('screenshot.png')
        rimg = img.copy()
        rimg.show()
        rimg.save('pillow.png')
        print("-------------------------------")
    else:
        print('no add found')



print(result)



# content = driver.find_element(By.ID, result[0])
# p1 = Process(target = highlight(content, 30, "red", 2))
# p1.start()
# content = driver.find_element(By.ID, result[1])
# p2 = Process(target = highlight1(content, 30, "red", 2))
# p2.start()
# p1.join()
# p2.join()

print("end")