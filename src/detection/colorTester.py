import numpy as np
import cv2
import os
from colorRanges import colorRanges

imagesDir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images"
)

# Script for finding color ranges so I can use them in my detection later

def nothing(x):
    print(f"lower_threshold={lowerThreshold} \n upper_threshold={upperThreshold}")

def initialiseTrackbars(range):
    # Create trackbars for adjusting HSV values
    cv2.createTrackbar("MinHue", "image", range[0][0], 179, nothing)
    cv2.createTrackbar("MaxHue", "image", range[1][0], 179, nothing)

    cv2.createTrackbar("MinSaturation", "image", range[0][1], 255, nothing)
    cv2.createTrackbar("MaxSaturation", "image", range[1][1], 255, nothing)

    cv2.createTrackbar("MinValue", "image", range[0][2], 255, nothing)
    cv2.createTrackbar("MaxValue", "image", range[1][2], 255, nothing)


def extractColor(image):
    global lowerThreshold, upperThreshold
    image = cv2.medianBlur(image, ksize=11)

    lowerThreshold = []
    upperThreshold = []
    cv2.namedWindow("image")

    # The color you want to initialise your trackbars with
    initialiseTrackbars(colorRanges["yellow"])

    while True:
        # Get current trackbar positions
        minHue = cv2.getTrackbarPos("MinHue", "image")
        minSaturation = cv2.getTrackbarPos("MinSaturation", "image")
        minValue = cv2.getTrackbarPos("MinValue", "image")

        maxHue = cv2.getTrackbarPos("MaxHue", "image")
        maxSaturation = cv2.getTrackbarPos("MaxSaturation", "image")
        maxValue = cv2.getTrackbarPos("MaxValue", "image")

        hsv_threshold = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lowerThreshold = np.array([minHue, minSaturation, minValue])
        upperThreshold = np.array([maxHue, maxSaturation, maxValue])

        # Create mask and mask image
        mask = cv2.inRange(hsv_threshold, lowerThreshold, upperThreshold)
        maskedImage = cv2.bitwise_and(image, image, mask=mask)

        # Display the image
        cv2.imshow("image", maskedImage)
        cv2.imshow("og", image)

        if cv2.waitKey(1) == ord("a"):
            cv2.destroyAllWindows()
            break


def main():
    img = cv2.imread(os.path.join(imagesDir, "yellow.jpg"))
    extractColor(img)


if __name__ == "__main__":
    main()
