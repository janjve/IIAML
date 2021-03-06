#<!--------------------------------------------------------------------------->
#<!--                   ITU - IT University of Copenhagen                   -->
#<!--                   SSS - Software and Systems Section                  -->
#<!--       Introduction to Image Analysis and Machine Learning Course      -->
#<!-- File       : Ex03_masking.py                                          -->
#<!-- Description: Script to select a specific region in the input image    -->
#<!--            : using a binary mask                                      -->
#<!-- Author     : Fabricio Batista Narcizo                                 -->
#<!--            : Rued Langgaards Vej 7 - 4D25 - DK-2300 - Kopenhagen S.   -->
#<!--            : fabn[at]itu[dot]dk                                       -->
#<!-- Responsable: Dan Witzner Hansen (witzner[at]itu[dot]dk)               -->
#<!--              Fabricio Batista Narcizo (fabn[at]itu[dot]dk)            -->
#<!--              Zaheer Ahmed (zahm[at]itu[dot]dk)                        -->
#<!-- Information: No additional information                                -->
#<!-- Date       : 03/12/2016                                               -->
#<!-- Change     : 03/12/2016 - Development of this exercise                -->
#<!-- Review     : 10/02/2017 - Finalized                                   -->
#<!--------------------------------------------------------------------------->

__version__ = "$Revision: 2017021001 $"

########################################################################
import argparse
import cv2
import matplotlib.pyplot as plt
import numpy as np

########################################################################
# Construct the argument parse and parse the arguments.
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required=True, help="Path to the image")
#args = vars(ap.parse_args())



# Create the Matplotlib figure.
fig = plt.figure("Images")

# This function creates a Matplotlib window and shows four images.
def showImage(image, pos, title="Image", isGray=False):
    sub = fig.add_subplot(1, 3, pos)
    sub.set_title(title)
    sub.imshow(image)
    plt.axis("off")
    if isGray:
        sub.imshow(image, cmap="gray")
    else:
        sub.imshow(image)

#<!--------------------------------------------------------------------------->
#<!--                            YOUR CODE HERE                             -->
#<!--------------------------------------------------------------------------->
image = cv2.imread("zico.jpg", cv2.IMREAD_COLOR)
image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

mask_img = np.zeros(image.shape[:2], dtype="uint8")
cv2.rectangle(mask_img, (647, 40), (776, 195), (255,255,255), -1)
cv2.rectangle(mask_img, (128, 19), (305, 182), (255,255,255), -1)
cv2.circle(mask_img, (543, 620), 60, (255,255,255), -1)
result = cv2.bitwise_and(image, image, mask=mask_img)

showImage(image_rgb, 1)
showImage(mask_img, 2, isGray=True)
showImage(cv2.cvtColor(result, cv2.COLOR_BGR2RGB), 3)

#<!--------------------------------------------------------------------------->
#<!--                                                                       -->
#<!--------------------------------------------------------------------------->

# Show the Matplotlib windows.
plt.show()
