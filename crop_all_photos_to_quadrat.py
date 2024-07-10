'''
This file contains a loop that will crop all photos in the test_photos folder. Note that it
requires user input - the user places all the quadrat corners in the napari
GUI, and the code will crop it according to those corners. 
'''

import napari
from matplotlib import pyplot as plt
import numpy as np
import cv2
from functions import extract_filename_number, matrix_xy_swap, reorder_file_paths


# Determine the folder of images that will be looped through
path = 'test_photos/*'

# Get list of files for looping through
filenames = reorder_file_paths(path)

# Determine the files that will be looped through
specific_filenames = ['test_photos\\image_0.jpg', 'test_photos\\image_1.jpg', 'test_photos\\image_2.jpg', 'test_photos\\image_3.jpg', 'test_photos\\image_4.jpg']

for filename in specific_filenames:
    # Extract the number in the filename for saving the proper name later
    file_number = extract_filename_number(filename)

    # Read in the file in RGB with pyplot
    img = plt.imread(filename)
            
    # Open it in napari viewer
    viewer = napari.view_image(img, rgb=True)
            
    # Add a points layer
    points_layer = viewer.add_points()

    kill_switch = input('\nUse the add points button in the GUI that just popped up (or select the tool by pressing 2) to place one point on every corner of the quadrat. Place them in clockwise order starting at top left. Type "ready" when you\'re ready to move on to the next photo, and "quit" to quit. ')

    # Quit the loop if the user types "quit"
    if kill_switch == 'quit':
        break
    else:
        # Retrieve points from the GUI
        corners = points_layer.data

        # Convert it into a np matrix
        corners = np.array(corners, dtype = np.float32)

        # Swap the x and y to convert from napari coordinates to python coordinates
        corners_swapped = matrix_xy_swap(corners)

        # Get a side length based on the top pipe of the quadrat
        distance = corners_swapped[0] - corners_swapped[1]
        side_length = abs(int(np.linalg.norm(distance))) # absolute value of the Euclidean distance

        # Define the new locations of each point based on side length
        corner_destinations = np.array([
            [0, 0], # top left
            [side_length, 0], # top right
            [side_length, side_length], # bottom right
            [0, side_length] # bottom left
        ], dtype=np.float32)

        # Get perspective transformation matrix 
        matrix = cv2.getPerspectiveTransform(corners_swapped, corner_destinations)

        # Apply perspective transformation
        img_transformed = cv2.warpPerspective(img, matrix, (side_length, side_length))

        # Save the image to file
        plt.imsave(f'test_photos_cropped/image_{file_number}.jpg', img_transformed)
