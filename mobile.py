from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import numpy as np
import time 
import cv2
mobile_emulation = {
    "deviceMetrics": { "width": 300, "height": 600, "pixelRatio": 3.0 },
    "userAgent": "Mozilla/5.0 (Linux; Android 4.2.1; en-us; Nexus 5 Build/JOP40D) AppleWebKit/535.19 (KHTML, like Gecko) Chrome/18.0.1025.166 Mobile Safari/535.19" }
chrome_options = Options()
chrome_options.add_argument("window-size=337,600")
chrome_options.add_experimental_option("mobileEmulation", mobile_emulation)
CHROMEDRIVER_PATH="F:\\chromedriver\\chromedriver.exe"
driver = webdriver.Chrome(CHROMEDRIVER_PATH,chrome_options = chrome_options)
driver.get('https://www.whatmobile.com.pk/')
time.sleep(15)
driver.save_screenshot('screenshotmobile.png')

# img = cv2.imread('screenshotmobile.png') # Read in the image and convert to grayscale
# gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
# gray = 255*(gray < 128).astype(np.uint8) # To invert the text to white
# coords = cv2.findNonZero(gray) # Find all non-zero points (text)
# x, y, w, h = cv2.boundingRect(coords) # Find minimum spanning bounding box
# rect = img[y:y+h, x:x+w] # Crop the image - note we do this on the original image
# cv2.imshow("Cropped", rect) # Show it
# cv2.waitKey(0)
# cv2.destroyAllWindows()
# cv2.imwrite("final.png", rect) # Save the image

