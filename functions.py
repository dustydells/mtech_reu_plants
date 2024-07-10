import numpy as np
import cv2
import re
import glob
from skimage import img_as_float, img_as_ubyte
import skimage.filters as skfil


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



def matrix_xy_swap(matrix):
    '''
    When you establish your points in napari, they come in in (y, x) order. 
    In order to use these points with normal Python functionalities, x and y
    need to be switched. I love, love, love being a programmer.

    Parameters:
        matrix:
            A numpy array of coordinates as retreived from napari interface
    Returns: 
        swapped_matrix:
            The same matrix, but with the x and y switched for each vector
    '''
    swapped_matrix = np.array([[y, x] for x, y in matrix], dtype=np.float32)

    return swapped_matrix

def reorder_quadrat_corners(corners):
    '''
    In order for napari cropping to work, the points of the quadrat need to be in
    clockwise order starting from the top left point. 

    Parameters:
        corners: a list of points of the quadrat corners
    Returns:
        corners_array: a numpy array containing the points in clockwise order
        starting from the top left point
    '''
    # Convert the list of points to a numpy array
    pts = np.array(corners)

    # Calculate the sum and difference of the points
    s = pts.sum(axis=1)
    diff = np.diff(pts, axis=1)

    # The top-left point will have the smallest sum
    top_left = pts[np.argmin(s)]
    # The bottom-right point will have the largest sum
    bottom_right = pts[np.argmax(s)]
    # The top-right point will have the smallest difference
    top_right = pts[np.argmin(diff)]
    # The bottom-left point will have the largest difference
    bottom_left = pts[np.argmax(diff)]

    # Return the ordered points
    corners_array = np.array([top_left, top_right, bottom_right, bottom_left])
    
    return corners_array



def extract_filename_number(filename):
    '''
    For when you just want the number in your filename.

    Parameters:
        filename: name of a file (preferably not the whole path)

    Returns:
        number: The number in the filename
    '''
    # Grab the number in the filename
    number = re.search('\d+', filename).group() # .group() function returns the match of the regexp, rather than a big silly string of junk

    return number

