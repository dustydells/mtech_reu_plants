import numpy as np
import cv2

# Non-local means de-noising
def nl_means_denoise():
    pass

# Make array of HSV (maybe also include RGB) histograms
def histogram_array():
    pass


# VEGETATIVE INDECES
# Excess Green
def exg(img):
    '''
    Calculate the Excess Green (ExG) vegetative index. 

    Parameters:
        img: The image for which you want the vegetative index of each pixel, 
        in BGR (This function assumes that you have used cv2.imread() in order to load in this photo)
    Returns:
        exg_img: 
        
    '''

    # Extract the red, green, and blue channels
    r = img[:, :, 2].astype(float)
    g = img[:, :, 1].astype(float)
    b = img[:, :, 0].astype(float)

    # Calculate the index
    exg = 2 * g - r - b

    # Normalize index to range [0, 255] for visualization
    exg_normalized = cv2.normalize(exg, None, 0, 255, cv2.NORM_MINMAX)

    # Convert normalized index to an 8-bit image
    exg_img = exg_normalized.astype(np.uint8)

    return exg_img

