from PIL import Image
from io import BytesIO
import time
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By

def open_url(url):

    options = Options()

    options.headless = True
    CHROMEDRIVER_PATH="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe"
    driver = webdriver.Chrome(CHROMEDRIVER_PATH, options=options)
    driver.get(url)
    time.sleep(15)
    driver.fullscreen_window()
    driver.save_screenshot('t1.png')
    driver = driver.find_element(By.TAG_NAME, "body")
    driver.save_screenshot('t2.png')
    print("end")




open_url("https://babyanimalz.com/")