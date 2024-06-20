import numpy as np
import cv2

# Non-local means de-noising
def nl_means_denoise():
    pass

# Make array of HSV (maybe also include RGB) histograms
def histogram_array():
    pass


# VEGETATIVE INDECES
def apply_vegetative_index(img, index_type):
    '''
    Calculate the specified vegetative index and apply it to the image. 

    Parameters:
        img: The image for which you want the vegetative index of each pixel, 
            in BGR (This function assumes that you have used cv2.imread() in order to load in this photo)
        index_type: The Vegetative index you'd like to use. Options: exg, exr
    Returns:
        vegetated_img: A grayscale image that maps value to vegetative index of each pixel
        
    '''

    # Extract the red, green, and blue channels
    r = img[:, :, 2].astype(float)
    g = img[:, :, 1].astype(float)
    b = img[:, :, 0].astype(float)

    # Excess Green (ExG)
    if index_type == 'exg':
        # Calculate the index
        index = 2 * g - r - b

    # Excess Red (ExR)
    elif index_type == 'exr':
        # Calculate the index
        index = (1.4 * r - g) / g + r + b

    # Normalize index to range [0, 255] for visualization
    normalized = cv2.normalize(index, None, 0, 255, cv2.NORM_MINMAX)

    # Convert normalized index to an 8-bit image
    vegetated_img = normalized.astype(np.uint8)

    return vegetated_img

