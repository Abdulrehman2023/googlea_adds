# from selenium import webdriver
# import base64
# import time
# import os
# import codecs
# driver = webdriver.Chrome(executable_path="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe")
# from selenium.webdriver.common.by import By
# from threading import Thread
# from multiprocessing import Process
# import cv2


# driver.get('https://babyanimalz.com/')
# print("page loadded")
# time.sleep(15)
# driver.fullscreen_window()

# content = driver.find_element(By.TAG_NAME, 'body')
# content.screenshot('content-body.png')
from selenium.webdriver.common.by import By
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options


CHROMEDRIVER_PATH="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe"
    
options = webdriver.ChromeOptions()
options.headless = True
driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)

URL = 'https://animalfactguide.com/'

driver.get(URL)
time.sleep(10)

S = lambda X: driver.execute_script('return document.body.parentNode.scroll'+X)
driver.set_window_size(S('Width'),S('Height')) # May need manual adjustment                                                                                                                
driver.find_element(By.TAG_NAME , "body").screenshot('web_screenshot.png')

driver.quit()