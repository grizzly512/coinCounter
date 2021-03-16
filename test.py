import numpy as np
import cv2

image = cv2.imread('./1.jpg')
output = image.copy()
gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
gray = cv2.GaussianBlur(gray, (15, 15), 0)
circles = cv2.HoughCircles(gray, cv2.HOUGH_GRADIENT, 2, 50)

print(len(circles[0]))
print(circles)
average_color = [image[:, :, i].mean() for i in range(image.shape[-1])]
print(average_color)
if circles is not None:
    # convert the (x, y) coordinates and radius of the circles to integers
    circles = np.round(circles[0, :]).astype("int")
    # loop over the (x, y) coordinates and radius of the circles
    for (x, y, r) in circles:
        # draw the circle in the output image, then draw a rectangle
        # corresponding to the center of the circle
        cv2.circle(output, (x, y), r, (0, 255, 0), 4)
        cv2.rectangle(output, (x - 5, y - 5), (x + 5, y + 5), (0, 128, 255), -1)
    # show the output image
    cv2.imshow("output", np.hstack([image, output]))
    cv2.waitKey(0)

# gray = cv2.GaussianBlur(gray, (15, 15), 0)

# gray = cv2.adaptiveThreshold(gray, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY_INV, 11, 1)
# (_,gray) = cv2.threshold(gray,0,255,cv2.THRESH_BINARY_INV+cv2.THRESH_OTSU)
# contours, hierarchy = cv2.findContours(gray, cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)

# for i,cnt in enumerate(contours):
#     ellipse = cv2.fitEllipse(cnt)
#     print(ellipse,type(ellipse))
#     cv2.ellipse(image, ellipse, (0,255,0), 2)