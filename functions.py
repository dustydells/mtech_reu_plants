import numpy as np
import cv2
import re
import glob
from skimage import img_as_float, img_as_ubyte
import skimage.filters as skfil

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
    # Extract the red, green, and blue channels. Note that it expects BGR images. 
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
def reorder_file_paths(path):
    '''
    This function exists because I've rearranged the images so often that the operating system
    no longer stores them in number order (image_0, image_1, and so on). This function returns
    an ordered list of all the files that are currenty in the specified folder. It should be able
    to handle additions to the folder. 

    Parameters:
        Path of the folder you want to loop through (In this format results/greenhouse_photos_thresholded/*
        for example. The asterisk is necessary or else the glob thingy won't work.)
    Returns: 
        List of file paths to be run from the main project directory. It is in order of whatever
        number is in the filename. 
    '''
    def sorting_function(path):
        # Grab a list containting the number found in the file path (includes multi-digit numbers)
        numbers = re.findall('\d+', path)

        # Return the numbers as integers if the list of numbers isn't empty. Return 0 otherwise
        return int(numbers[0]) if numbers else 0
         

    # Use the sorting_function on the list of paths so they will be sorted numerically.
    files = sorted(glob.glob(path), key=sorting_function)

    return files

# Apply otsu threshold to an image
def apply_otsu(img):
    '''
    Apply the otsu thresholding filter to an image. 

    Parameters:
        img: An image
    Returns: 
        img_ubyte: A binary image that has had the otsu threshold applied to it
    '''
        
    # Convert image into float
    img_float = img_as_float(img)

    # Apply otsu threshold
    thresh_otsu = skfil.threshold_otsu(img_float)

    # If image is <= to the threshold number, it's True. False otherwise.
    binary_otsu = img_float <= thresh_otsu

    # Convert back to ubyte
    img_ubyte = img_as_ubyte(binary_otsu)

    return img_ubyte


# path = 'quadrat_photos_raw/*'

# files = reorder_file_paths(path)

# for file in files:
#     print(file)
