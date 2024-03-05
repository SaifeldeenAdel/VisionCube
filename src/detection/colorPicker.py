import numpy as np
import cv2
import os

from Utils import Utils
from Colors import Colors

imagesDir = os.path.join(
    os.path.dirname(os.path.dirname(os.path.dirname(__file__))), "images"
)

# Helper Script for finding color ranges so I can use them in my detection later


def nothing(x):
    print(f"lower_threshold={lowerThreshold} \n upper_threshold={upperThreshold}")


def initialiseTrackbars(color: Colors):
    # Create trackbars for adjusting HSV values with custom initial values
    cv2.createTrackbar("MinHue", "Color Picker", color.getMinRange()[0], 179, nothing)
    cv2.createTrackbar("MaxHue", "Color Picker", color.getMaxRange()[0], 179, nothing)

    cv2.createTrackbar(
        "MinSaturation", "Color Picker", color.getMinRange()[1], 255, nothing
    )
    cv2.createTrackbar(
        "MaxSaturation", "Color Picker", color.getMaxRange()[1], 255, nothing
    )

    cv2.createTrackbar("MinValue", "Color Picker", color.getMinRange()[2], 255, nothing)
    cv2.createTrackbar("MaxValue", "Color Picker", color.getMaxRange()[2], 255, nothing)


def colorPicker(image):
    global lowerThreshold, upperThreshold
    image = cv2.medianBlur(image, ksize=11)

    lowerThreshold = []
    upperThreshold = []
    cv2.namedWindow("Color Picker")

    # The color you want to initialise your trackbars with
    initialiseTrackbars(Colors.RED)

    while True:
        # Get current trackbar positions
        minHue = cv2.getTrackbarPos("MinHue", "Color Picker")
        minSaturation = cv2.getTrackbarPos("MinSaturation", "Color Picker")
        minValue = cv2.getTrackbarPos("MinValue", "Color Picker")

        maxHue = cv2.getTrackbarPos("MaxHue", "Color Picker")
        maxSaturation = cv2.getTrackbarPos("MaxSaturation", "Color Picker")
        maxValue = cv2.getTrackbarPos("MaxValue", "Color Picker")

        hsv_threshold = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
        lowerThreshold = np.array([minHue, minSaturation, minValue])
        upperThreshold = np.array([maxHue, maxSaturation, maxValue])

        # Create mask and mask image
        mask = cv2.inRange(hsv_threshold, lowerThreshold, upperThreshold)
        maskedImage = cv2.bitwise_and(image, image, mask=mask)

        # Display the image
        cv2.imshow("Color Picker", maskedImage)
        # cv2.imshow("og", image)

        if cv2.waitKey(1) == ord("a"):
            cv2.destroyAllWindows()
            break


def main():
    img = cv2.imread(os.path.join(imagesDir, "RO.jpg"))
    red = Utils.extractColor(img, Colors.RED)
    orange = Utils.extractColor(img, Colors.ORANGE)
    Utils.displayImage("Red", cv2.bitwise_or(red, orange))

    # colorPicker(img)

if __name__ == "__main__":
    main()
