import cv2 as cv
from helpers import isBlackModule

img = cv.imread("./mcdonaldsYT.png")
img2 = img.copy()

## Turns it to gray scale
imgGS = cv.cvtColor(img, cv.COLOR_BGR2GRAY)

## Gives me a thresholded image, so that its binary: black and white
ret, thresh = cv.threshold(imgGS, 127, 255, cv.THRESH_BINARY)

##
## Stage 1: Find the corners
##

## This helps me find the contours in the image so it can find the square patterns in the corners
contours, hierarchy = cv.findContours(thresh, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)

## We also need to know the height of the outer big box so that we can divide it by 7
## This is because the big box is divided into a 7x7 grid
maxHeight = 0
pixelLength = 0

cornerSquares = []
## Get the contours of the 3 squares in the corner 
for cnt in contours:
    approx = cv.approxPolyDP(cnt, 0.02*cv.arcLength(cnt, True), True)
    if len(approx) == 4:
        area = cv.contourArea(cnt)
        if area > 1000 and area < 10000:
            x, y, w, h = cv.boundingRect(approx)
            cornerSquares.append((x, y, w, h))
            if h > maxHeight:
                maxHeight = h

## Calculate the pixel length of one square in the 7x7 grid
pixelLength = maxHeight / 7

## Get rid of the inside corner square that are not pixellength and label TL, TR, BL
filteredCornerSquares = []
for (x, y, w, h) in cornerSquares:
    if w/7 == pixelLength and h/7 == pixelLength:
        # Limitation : assuming that the qr code is not shifted at all at any angle and is near perfectly aligned
        if x == y:
            label = "TL"
        elif x > y:
            label = "TR"
        else:
            label = "BL"
        filteredCornerSquares.append((x, y, w, h, label))
        cv.rectangle(img2, (x, y), (x + w, y + h), (0, 255, 0), 1)
        # cv.putText(img2, label, (x + w//2, y + h//2), cv.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 1)
        # print(f"Found corner square at x:{x}, y:{y}, w:{w}, h:{h}")

# print(f"Top Left: ({filteredCornerSquares[2][0]}, {filteredCornerSquares[2][1]})")
# print(f"Bottom Right: ({filteredCornerSquares[1][0] + pixelLength * 7}, {filteredCornerSquares[0][1] + pixelLength * 7})")

##
## Stage 2: Finding the Timing Patterns
##

# ***Timing patterns are the lines of alternating black and white squares between the corner squares

# Now that we know the cordinates and pixel lengths, we find the timing pattern so that we can find 
# the version of qr code to know how many modules there are / how big our list needs to be



# =================================================================================================================================


# cv.imshow("Image", img)
cv.imshow("Image w/ Contours", img2)
k = cv.waitKey(0)
if k == 27:
    cv.destroyAllWindows()

