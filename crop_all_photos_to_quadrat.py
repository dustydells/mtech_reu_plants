'''
This file contains a loop that will crop all photos. Note that it
requires user input - the user places all the corners in the napari
GUI, and the code will crop it according to those corners. 
'''

import napari
from matplotlib import pyplot as plt
import numpy as np
import cv2
from functions import matrix_xy_swap, reorder_file_paths


# Determine the folder of images that will be looped through
path = 'test_photos/*'

# Get list of files for looping through
filenames = reorder_file_paths(path)

# Put the names of the greenhouse files in a list so they can be skipped in the loop
greenhouse_test_filenames = ['test_photos\\image_6.JPG', 'test_photos\\image_7.JPG', 'test_photos\\image_8.JPG', 'test_photos\\image_9.JPG', 'test_photos\\image_10.JPG']

for i, filename in enumerate(filenames):
    # Skip the greenhouse images
    if filename in greenhouse_test_filenames:
        pass
    else:
        # Read in the file in RGB with plt
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
            plt.imsave(f'test_photos_cropped/image_{i}.jpg', img_transformed)
