'''
Run this script to get the vegetative index information from images. There are a few 
options - if you don't want your image to be cropped to a square, then comment out the
"CROP TO SQUARE" line. If you want to denoise the image, uncomment the "DENOISE IMAGE"
code. In order to find out what threshold to use, you can uncomment the "INVESTIGATE HISTOGRAM"
code.
'''

import cv2
from operator import index
from matplotlib import pyplot as plt
from functions import crop_to_square, apply_vegetative_index, calc_live_plants_percentage

def main():
    '''
    Determine your parameters here. 
    '''

    # Enter path to input image here.
    path = 'raw_photos\\20240531_103740.jpg'

    # Enter output path and filename here.
    output_path = 'results/master_script_output/20240531_103740_grid.jpg'

    # Determine vegetative index that will be used
    index_type = 'rgbvi' # RGBVI worked well for my quadrat photos on sunny days - feel free to experiment

    # INVESTIGATE HISTOGRAM
    '''
    You can find out what threshold to use by uncommenting this code and checking out the histogram
    made from the values in your image. Try different values and see what works.
    '''
    # plt.hist(vi_img.flatten(), bins = 100)
    # plt.show()

    # Determine threshold that will differentiate between live and dead plants
    green_threshold = 130

    # Run the process
    run_script(path, output_path, index_type, green_threshold)



def run_script(path, output_path, index_type, green_threshold, denoise=False, crop=True):
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
            and not green. Example: 130 works well for images on RGBVI scale. 
        denoise:
            Boolean. whether you want to denoise the image or not (default: False)
    '''

    # Read in the file in RGB with pyplot (must be in RGB for quadrat crop to work)
    img = plt.imread(path)

    # CROP TO SQUARE
    if crop == True:
        img = crop_to_square(img)
        cropped_img = img # Save the cropped image so it can be included in the grid later

    # DENOISE IMAGE
    if denoise == True:
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    # APPLY VEGETATIVE INDEX
    vi_img = apply_vegetative_index(img, index_type)

    # Calculate a percentage of pixels that are green according to your threshold cutoff
    percent_green_pixels, binary = calc_live_plants_percentage(vi_img, green_threshold)

    print(f'Percentage of pixels considered green based on a {green_threshold} threshold of {index_type} image: {percent_green_pixels}')

    # Display images in a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Original Image
    axs[0, 0].imshow(img, cmap='gray')
    axs[0, 0].set_title('Original Image')
    axs[0, 0].axis('off')

    if crop == True:
        # Cropped image
        axs[0, 1].imshow(cropped_img, cmap='gray')
        axs[0, 1].set_title('Cropped image')
    axs[0, 1].axis('off')

    # Image modified by vegetative index
    axs[1, 0].imshow(vi_img, cmap='viridis')
    axs[1, 0].set_title(f'Image modified by {index_type}')
    axs[1, 0].axis('off')

    # Binary image of pixels considered green
    axs[1, 1].imshow(binary, cmap='gray')
    axs[1, 1].set_title(f'Binary image of pixels considered green by {green_threshold} threshold')
    axs[1, 1].axis('off')

    plt.tight_layout()

    # Save the grid to file
    plt.savefig(output_path)


main()