'''
This script creates a g r  i d yippee
It works best on images of plant leaves and stems on a plain background.
Specify your parameters in the main function.
'''

import cv2
import pandas as pd
from matplotlib import pyplot as plt
from functions import apply_vegetative_index
from skimage import img_as_ubyte
import plotnine as pn

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

    # Determine threshold that will differentiate between live and dead plants
    green_threshold = 160

    run_script(path, output_path, index_type, green_threshold)


def run_script(path, output_path, index_type, green_threshold):
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
        green_threshold:
            Integer. The cutoff VI value that differentiates between green 
            and not green.
 
    '''
    
    # Read in the image in color
    img = cv2.imread(path, 1)

    # APPLY VEGETATIVE INDEX
    vi_img = apply_vegetative_index(img, index_type)

    # THRESHOLD IMAGE
    thresh_img = vi_img >= green_threshold

    # Convert back to ubyte
    mask = img_as_ubyte(thresh_img)

    # Invert the mask because the bitwise_and operation replaces white pixels
    # mask = cv2.bitwise_not(img_ubyte)

    # Apply the binary mask to the VI image
    # Only keep the pixels where the binary mask is white (255)
    img_masked = cv2.bitwise_and(vi_img, vi_img, mask = mask)

    # Convert image into dataframe
    df = pd.DataFrame(img_masked.flat, columns=['intensity'])

    # Filter out all the zero values
    df = df[df['intensity'] != 0]

    plot = (pn.ggplot(df) + 
            pn.aes(x='intensity') + 
            pn.geom_histogram(bins = 100))

    plot.show()

    # cv2.imshow('mask', img_masked)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


main()