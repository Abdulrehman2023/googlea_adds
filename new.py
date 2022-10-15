import numpy as np
import cv2

# Read input image
img = cv2.imread('pillow.png')
img2 = cv2.imread('testing.png')

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
cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), thickness = 2)

# Show result
img3 = img.copy()
img3[y:y+h,x:x+w]=img2
cv2.imshow('gray', gray)
cv2.imshow('img', img)
cv2.imshow('img2', img2)
cv2.imshow('img3', img3)
cv2.waitKey(0)
cv2.destroyAllWindows()

