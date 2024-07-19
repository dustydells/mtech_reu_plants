import numpy as np
import cv2
import re
import os
import sys
import glob
import napari
import spyndex
from matplotlib import pyplot as plt
from skimage import img_as_float, img_as_ubyte
import skimage.filters as skfil

# MAIN PROCESS FUNCTIONS
'''

1. Crop every image to its quadrat using the napari gui
2. Resize every image to the smallest length in the folder of photos
3. denoise images
4. Apply vegetation index
5. Convert pixel information into a csv

'''

# CROP TO QUADRAT
def crop_to_square(img):
    '''
    This function takes an image containing a quadrat or square object and crops the image
    into the square using a perspective transform.
    It uses the napari GUI to present a window in which the user can place points
    on the four corners. 
    Note that if you use this function on multiple images, they
    won't necessarily be the same size. 

    Parameters:
        img:
            An image of the ground that contains a square shape or quadrat
    Returns:
        cropped_img:
            The same image, but only the pixels within the square
    '''

    # Give array_length initial value to kick off while loop
    array_length = 0

    # Keep looping until user inputs the correct amount of points
    while array_length != 4:

        print('Loading napari...')

        # Open image in napari viewer
        viewer = napari.view_image(img, rgb=True)
                
        # Add a points layer
        points_layer = viewer.add_points()

        '''
        At this point, the napari GUI should open. Use the add point tool
        (hotkey is 2) to place a point on every corner of the square.
        Close the window when you're finished. 
        '''

        input('Use the add point tool (hotkey is 2) to place a point on every corner of the square. Close the window and press enter here when you\'re finished. ')

        # Retrieve points from the GUI
        corners = points_layer.data

        # Convert it into a np matrix
        corners = np.array(corners, dtype = np.float32)

        # Save the amount of points in the array into a variable
        array_length = corners.shape[0]

        if array_length != 4:
            print('\nPlease enter 4 points - one for each corner of the square.')  

    # Swap the x and y to convert from napari coordinates to python coordinates
    corners_swapped = matrix_xy_swap(corners)

    # Ensure that the points are in the correct order (clockwise starting at top left)
    corners_reordered = reorder_quadrat_corners(corners_swapped)

    # Get a side length based on the top pipe of the quadrat
    distance = corners_reordered[0] - corners_reordered[1]
    side_length = abs(int(np.linalg.norm(distance))) # absolute value of the Euclidean distance

    # Define the new locations of each point based on side length
    corner_destinations = np.array([
        [0, 0], # top left
        [side_length, 0], # top right
        [side_length, side_length], # bottom right
        [0, side_length] # bottom left
    ], dtype=np.float32)

    # Get perspective transformation matrix 
    matrix = cv2.getPerspectiveTransform(corners_reordered, corner_destinations)

    # Apply perspective transformation
    img_transformed = cv2.warpPerspective(img, matrix, (side_length, side_length))

    print(f'Image has been cropped.')

    return img_transformed






# VEGETATION INDECES
def apply_vegetation_index(img, index_type):
    '''
    Calculate the specified vegetation index and apply it to the image. 
    Note that "+ 1e-6" is added any time it could help prevent divide-by-zero errors. 

    Parameters:
        img: The image for which you want the vegetation index of each pixel, 
            in BGR (This function assumes that you have used cv2.imread() in order to load in this photo)
        index_type: The vegetation index you'd like to use. Options: exg, exr, grvi, rgbvi, exg-exr
    Returns:
        vegetated_img: A grayscale image that maps value to vegetation index of each pixel
        
    '''
    # Make sure index is lowercase
    index_type = index_type.lower()

    # Extract the red, green, and blue channels. Note that it expects BGR images. 
    r = img[:, :, 2].astype(float)
    g = img[:, :, 1].astype(float)
    b = img[:, :, 0].astype(float)

    # Excess Green (ExG)
    if index_type == 'exg':
        index = 2 * g - r - b

    # Excess Red (ExR)
    elif index_type == 'exr':
        index = (1.4 * r - g) / (g + r + b + 1e-6)

    # Green-Red Vegetation Index (GRVI)
    elif index_type == 'grvi':
        index = (g - r) / (g + r + 1e-6)

    # Visible Atmospherically Resistant Index (VARI)
    # It would be nice to include the VARI in this function but I spent multiple hours
    # trying to figure out what's wrong with it and got nowhere. Gonna move on with my life.
    # elif index_type == 'vari':
    #     index = (g - r) / (g + r - b - 1e-6)
        # index = spyndex.computeIndex(
        #     index = ['VARI'],
        #     params = {
        #         'R':r,
        #         'G':g,
        #         'B':b
        #     }
        # )
        
    # Red-Green-Blue Vegetation Index (RGBVI)
    elif index_type == 'rgbvi':
        index = (g**2 - r * b) / (g**2 + r * b + 1e-6)

    # ExG - ExR
    elif index_type == 'exg-exr':
        exg = 2 * g - r - b
        exr = (1.4 * r - g) / (g + r + b + 1e-6)
        index = exg - exr

    else:
        message = 'The index_type you supplied didn\'t match up with any of these options: exg, exr, grvi, rgbvi, exg-exr'
        print(message)
        
    # Normalize index to range [0, 255] for visualization
    normalized = cv2.normalize(index, None, 0, 255, cv2.NORM_MINMAX)

    # Convert normalized index to an 8-bit image
    vegetated_img = normalized.astype(np.uint8)

    return vegetated_img

# Calculate percent of ground covered by live (green plants) given a VI image
def calc_live_plants_percentage(binary):
    '''
    This function takes an image that has been modified by a vegetation index and
    converted into a binary image with a threshold operation, and calculates the 
    percentage of the pixels in that image which meet a threshold. 
    It can be used to estimate how much of an image contains plants that are live. 

    Parameters:
        binary: 
            A binary image that has been modified by a threshold operation with 
            a vegetation index
    Returns:
        percent_green_pixels:
            The percent of all pixels in the image which are considered green based on a 
            given threshold as saved in the binary image 
    '''

    # Get the total amount of pixels
    total_pixels = binary.size

    # Count how many pixels are considered green
    green_pixels = np.count_nonzero(binary)

    # Calculate percentage of green pixels
    percent_green_pixels = green_pixels / total_pixels

    return percent_green_pixels

# OUTPUT SEGMENTATION INFO INTO CSV


# MISCELLANEOUS FUNCTIONS

# Resize all square photos to the same size as the smallest image.
def resize_square_imgs(path, outputdir):
    '''
    This function is designed to make all photos cropped into a square
    a consistent size. It resizes them all to the dimensions of the smallest
    photo in the folder. 

    Parameters:
        path:
            A path to a folder that contains square images
    Returns:
        outputdir:
            Output directory. Enter the path to the folder into which
            you want the resized images to be saved. 
    ''' 
    # Establish high minimum for min calculation later
    min = 9999999

    for file in glob.glob(path):
        # Read in image
        img = cv2.imread(file)

        side_length = img.shape[0]

        # Find minimum image size length
        if side_length < min: 
            min = side_length

    for i, file in enumerate(glob.glob(path)):
        # Read in image
        img = cv2.imread(file)

        # Resize all images to have previously established minimum length
        resized = cv2.resize(img, (min, min))

        cv2.imwrite(f'{outputdir}/image_{i}.jpg', resized) 


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
        corners: a numpy array of points of the quadrat corners
    Returns:
        corners_array: a numpy array containing the points in clockwise order
        starting from the top left point
    '''

    # Calculate the sum and difference of the points
    s = corners.sum(axis=1)
    diff = np.diff(corners, axis=1)

    # The top-left point will have the smallest sum
    top_left = corners[np.argmin(s)]
    # The bottom-right point will have the largest sum
    bottom_right = corners[np.argmax(s)]
    # The top-right point will have the smallest difference
    top_right = corners[np.argmin(diff)]
    # The bottom-left point will have the largest difference
    bottom_left = corners[np.argmax(diff)]

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

def calc_pixels_to_cm(img):
    '''
    Assuming that your image is cropped to cover a square meter of ground, 
    This function provides a conversion rate from pixels to centimeters. 
    The number it returns can be multiplied with a pixel value to give you
    its value in centimeters. 

    Parameters:
        img:
            An image that is cropped to a square meter. 
    Returns:
        pixels_to_cm:
            The pixels to centimeters conversion rate. 
    '''

    pixels_to_cm = 100 / img.shape[0]

    return pixels_to_cm

def list_all_paths(folder_path):
    '''
    Get a list of all the files in a folder

    Parameters:
        folder_path:
            Str. Path to the folder you want the paths for
    Returns:
        paths:
            List. List of paths in the folder you specified
    '''
    paths = []
    for root, directories, files in os.walk(folder_path):
        for directory in directories:
            paths.append(os.path.join(root, directory))
        for file in files:
            paths.append(os.path.join(root, file))
    return paths