import numpy as np
import cv2
import re

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
    Note that "+ 1e-6" is added any time it could help prevent divide-by-zero errors. 

    Parameters:
        img: The image for which you want the vegetative index of each pixel, 
            in BGR (This function assumes that you have used cv2.imread() in order to load in this photo)
        index_type: The Vegetative index you'd like to use. Options: exg, exr, grvi, vari, rgbvi, exg-exr
    Returns:
        vegetated_img: A grayscale image that maps value to vegetative index of each pixel
        
    '''
    # Extract the red, green, and blue channels
    r = img[:, :, 2].astype(float)
    g = img[:, :, 1].astype(float)
    b = img[:, :, 0].astype(float)

    # Excess Green (ExG)
    if index_type == 'exg':
        index = 2 * g - r - b

    # Excess Red (ExR)
    elif index_type == 'exr':
        index = (1.4 * r - g) / g + r + b + 1e-6

    # Green-Red Vegetation Index (GRVI)
    elif index_type == 'grvi':
        index = (g - r) / (g + r + 1e-6)

    # Visible Atmospherically Resistant Index (VARI)
    elif index_type == 'vari':
        index = (g - r) / (g + r - b + 1e-6)

    # Red-Green-Blue Vegetation Index (RGBVI)
    elif index_type == 'rgbvi':
        index = (g**2 - r * b) / (g**2 + r * b + 1e-6)

    # ExG - ExR
    elif index_type == 'exg-exr':
        exg = 2 * g - r - b
        exr = (1.4 * r - g) / g + r + b + 1e-6
        index = exg - exr


    else:
        print('The index_type you supplied didn\'t match up with any of these options: exg, exr, grvi, vari, rgbvi, exg-exr')


    # Normalize index to range [0, 255] for visualization
    normalized = cv2.normalize(index, None, 0, 255, cv2.NORM_MINMAX)

    # Convert normalized index to an 8-bit image
    vegetated_img = normalized.astype(np.uint8)

    return vegetated_img

# Reorder the list of files for looping through
def reorder_test_photos(path):
    '''
    This function exists because I've rearranged the images so often that the operating system
    no longer stores them in number order (image_0, image_1, and so on). This function returns
    an ordered list of all the files that are currenty in the specified folder. It should be able
    to handle additions to the folder. 

    Parameters:
        path of the folder you want to loop through 
    Returns: 
        List of file paths to be run from the main project directory. It is in order of whatever
        number is in the filename. 
    '''
