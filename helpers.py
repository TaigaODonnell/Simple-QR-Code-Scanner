

def isBlackModule(x, y, moduleLength, thresh):
    cx = int(x + moduleLength / 2)
    cy = int(y + moduleLength / 2)

    r = int(moduleLength * .2)  # radius for sampling points
    roi = thresh[cy - r:cy + r, cx - r:cx + r]

    return roi.mean() < 127