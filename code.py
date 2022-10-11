from selenium import webdriver
import base64
import time
import os
import codecs
driver = webdriver.Chrome(executable_path="C:\\Users\\FabTechSol\\Downloads\\chromedriver_win32\\chromedriver.exe")
from selenium.webdriver.common.by import By





driver.get('https://www.allbreedpedigree.com/')
print("page loadded")
time.sleep(10)


page_rect = driver.execute_cdp_cmd("Page.getLayoutMetrics", {})
print("matrices get")
time.sleep(5)
screenshot = driver.execute_cdp_cmd(
            "Page.captureScreenshot",
            {
                "format": "png",
                "captureBeyondViewport": True,
                "clip": {
                    "width": page_rect["contentSize"]["width"],
                    "height": page_rect["contentSize"]["height"],
                    "x": 0,
                    "y": 0,
                    "scale": 1
                }
            })
print("screenshot is taken")

with open('C:\\Users\\FabTechSol\\Desktop\\screenshot\\New folder\\new.png', "wb") as file:
    file.write(base64.urlsafe_b64decode(screenshot["data"]))

html = driver.page_source
n = os.path.join("C:\\Users\\FabTechSol\\Desktop\\screenshot\\html", "PageSave.html")
f = codecs.open(n, "w", "utf−8")
f.write(html)
driver.save_screenshot('screenshot.png')

getstyle = driver.find_elements(By.TAG_NAME, 'iframe')
result = []
for style in getstyle:
    iframe = style.get_attribute("name")
    if "google_ads_iframe" in iframe:
        print("-------------------------------")
        a = style.get_attribute("name")
        result.append(a)
        print(style.get_attribute("name"))
        print(style.get_attribute("height"))
        print(style.get_attribute("width"))
        print(style.get_attribute("style"))
        print("-------------------------------")
    elif "aswift" in iframe:
        print("-------------------------------")
        a = style.get_attribute("name")
        result.append(a)
        print(style.get_attribute("name"))
        print(style.get_attribute("height"))
        print(style.get_attribute("width"))
        print(style.get_attribute("style"))
        print("-------------------------------")
    else:
        print('no add found')



print(result)
def apply_style(s,element):
        driver.execute_script("arguments[0].setAttribute('style', arguments[1]);",element, s)

def highlight(element, effect_time, color, border):
    """Highlights (blinks) a Selenium Webdriver element"""
    driver = element._parent
    original_style = element.get_attribute('style')
    apply_style("border: {0}px solid {1};".format(border, color),element)
    time.sleep(effect_time)
    apply_style(original_style,element)


for ad in result:
    print(ad)
    content = driver.find_element(By.ID, ad)
    highlight(content, 30, "red", 2)
print("end")