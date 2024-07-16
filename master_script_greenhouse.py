'''
This script creates a g r  i d yippee
It works best on images of plant leaves and stems on a plain background.
'''

from email.mime import application
import cv2

from functions import apply_vegetative_index

# Enter path to image of plants on a blank background here
path = 'test_photos_greenhouse/image_10.jpg'

# Enter output path and filename here.
output_path = 'results/master_script_output/image_10_greenhouse_grid.jpg'

# Read in the image in color
img = cv2.imread(path, 0)

# APPLY VEGETATIVE INDEX
# Determine vegetative index that will be used
index_type = 'exg'

vi_img = apply_vegetative_index(img, index_type)