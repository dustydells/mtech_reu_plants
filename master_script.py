import array
import cv2
import sys
import glob
import napari
import numpy as np
from pathlib import Path
from matplotlib import pyplot as plt
from functions import matrix_xy_swap, reorder_quadrat_corners

# Enter path to folder that contains quadrat images here
path = 'raw_photos\\*'

# Enter path to output folder
output_dir = 'results\\master_script_output'

# Default setting for this variable
image_saved = False

# CROP IMAGES TO THE QUADRAT
print('CROP IMAGES TO THE QUADRAT')
# Define the path where you want to create the folder
folder_path = Path(output_dir + '\\cropped_images')

# Loop through every image in the folder
for i, file in enumerate(glob.glob(path)):
    # Read in the file in RGB with pyplot
    img = plt.imread(file)

    # Give array_length initial value to kick off while loop
    array_length = 0

    while array_length != 4:
                
        # Open image in napari viewer
        viewer = napari.view_image(img, rgb=True)
                
        # Add a points layer
        points_layer = viewer.add_points()

        # Pause for loop and present user with options
        kill_switch = input('\nUse the add points button in the GUI that just popped up (or select the tool by pressing 2) to place one point on every corner of the quadrat. You should place 4 points. Press "enter" when you\'re ready to move on to the next photo, and type "quit" to quit. \n')

        # Quit the loop if the user types "quit"
        if kill_switch == 'quit':
            quit = True
            break
        else:
            # Retrieve points from the GUI
            corners = points_layer.data

            # Convert it into a np matrix
            corners = np.array(corners, dtype = np.float32)

            # Save the amount of points in the array into a variable
            array_length = corners.shape[0]

            if array_length != 4:
                print('\nPlease enter 4 points - one for each corner of the quadrat.')  

    if quit == True:
        break
    else:

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

        # Create the folder if it doesn't already exisst
        try:
            folder_path.mkdir(parents=True, exist_ok=True)
            print(f"Folder '{folder_path}' created successfully.")
        except Exception as e:
            print(f"Error creating folder: {e}")

        # Save the image to file
        plt.imsave(f'{output_dir}\\cropped_images\\image_{i}.jpg', img_transformed)

        # Flip the switch if image saving was successful
        image_saved = True

        # Print out a message that your file was saved
        print(f'Image {i}, {file}, was cropped and saved in the folder "cropped_images" within your output directory.')

# If no images have been saved, terminate the program
if image_saved == False:
    print('No new images were saved. Program terminated.')
    sys.exit(0)

