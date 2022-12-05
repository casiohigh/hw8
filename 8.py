import numpy as np
import matplotlib.pyplot as plt
from skimage.measure import regionprops, label
from skimage.morphology import erosion, dilation

def count_lakes_and_bays(region):
    symbol = ~region.image
    labeled = label(symbol)
    lakes = 0
    bays = 0
    for reg in regionprops(labeled):
        is_lake = True
        for y, x in reg.coords:
            if (y == 0 or x == 0 or y == region.image.shape[0]-1 or x == region.image.shape[1]-1):
                is_lake = False
                break
        lakes += is_lake
        bays += not is_lake
    return lakes, bays

def has_vline(image):
    return 1 in erosion(np.mean(image, 0), [1, 1, 1])

def has_hline(image):
    return 1 in np.mean(image, 1)

def recognize(im_region):
    lakes, bays = count_lakes_and_bays(im_region)
    if lakes == 2:
        if has_vline(im_region.image):
            return 'B'
        else:
            return '8'
    elif lakes == 1:
        if bays == 4:
            return '0'
        elif bays == 3:
            return 'A'
        else:
            if im_region.eccentricity <= 0.65:
                return 'D'
            else:
                return 'P'
    elif lakes == 0:
        if np.mean(im_region.image) == 1.0:
            return '-'
        elif has_vline(im_region.image):
            return '1'
        elif bays == 2:
            return '/'
        elif has_hline(im_region.image):
            return '*'
        elif bays == 4:
            return 'X'
        else:
            return 'W'


image = plt.imread("symbols.png")
image = np.mean(image, 2)
image[image > 0] = 1
# plt.imshow(image)

labeled = label(image)
regions = regionprops(labeled)
for reg in regions:
    symbol = recognize(reg)
    if symbol:
        if symbol == 'P':
            plt.figure()
            plt.imshow(reg.image)

# print(count_lakes_and_bays(regions[50]))

plt.show()