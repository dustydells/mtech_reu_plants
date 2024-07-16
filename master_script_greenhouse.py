'''
This script creates a g r  i d yippee
It works best on images of plant leaves and stems on a plain background.
Specify your parameters in the main function.
'''

import cv2
from functions import apply_vegetative_index

def main():
    '''
    Determine your paramteters here. 
    '''
    
    # Enter path to image of plants on a blank background here
    path = 'test_photos_greenhouse/image_10.jpg'

    # Enter output path and filename here.
    output_path = 'results/master_script_output/image_10_greenhouse_grid.jpg'

    # Determine vegetative index that will be used
    index_type = 'exg' # ExG (Excess Green) worked well on greenhouse photos, which are of willow leaves and stems on a gray background.

    run_script(path, output_path, index_type)


def run_script(path, output_path, index_type):
    '''
    Run the entire process with the parameters you specified.

    Parameters:
        path:
            String. Path to the input image
        output_path:
            String. Path of the output image that will be saved
        index_type:
            String. The Vegetative index you'd like to use. 
            Options: exg, exr, grvi, vari, rgbvi, exg-exr
    '''
    
    # Read in the image in color
    img = cv2.imread(path, 0)

    # APPLY VEGETATIVE INDEX
    vi_img = apply_vegetative_index(img, index_type)


main()