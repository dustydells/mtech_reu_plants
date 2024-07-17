'''
Run this script to get the vegetative index information from images. 
Specify your parameters in the main function.
'''

import cv2
import pandas as pd
import plotnine as pn
from skimage import img_as_ubyte
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



def run_script(path, output_path, index_type, green_threshold, denoise=False, crop=False):
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
    og_img = img # Save the original image so it can be included in the grid later

    # CROP TO SQUARE
    if crop == True:
        img = crop_to_square(img)
        cropped_img = img # Save the cropped image so it can be included in the grid later

    # DENOISE IMAGE
    if denoise == True:
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    # APPLY VEGETATIVE INDEX
    vi_img = apply_vegetative_index(img, index_type)

    # THRESHOLD IMAGE
    binary = vi_img >= green_threshold

    # Calculate a percentage of pixels that are green according to your threshold cutoff
    percent_green_pixels = calc_live_plants_percentage(binary)

    print(f'Percentage of pixels considered green based on a {green_threshold} threshold of {index_type} image: {percent_green_pixels}')

    # Convert binary into ubyte so it can be used as a mask and displayed
    binary = img_as_ubyte(binary)

    # Apply the binary mask to the VI image
    # Only keep the pixels where the binary mask is white (255)
    img_masked = cv2.bitwise_and(vi_img, vi_img, mask = binary)

    # Convert image into dataframe
    print('Converting image to dataframe...')
    df = pd.DataFrame(img_masked.flat, columns=['intensity'])

    # Filter out all the zero values
    df = df[df['intensity'] != 0]

    # Create the plot
    print('Constructing plot...')
    plot = (pn.ggplot(df) + 
            pn.aes(x='intensity') + 
            pn.geom_histogram(bins = 100, fill = 'lightseagreen') +
            pn.labs(
                 x = 'Intensity',
                 y = 'Count',
                 title = f'Distribution of pixel intensity of {index_type} image'
            ) +
            pn.theme_classic()
    )

    # Render the plotnine plot to an image
    fig = plot.draw()
    fig.savefig('results/plotnine_plot.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plot_image = plt.imread('results/plotnine_plot.png')
    
    # Display images in a 2x3 grid
    fig, axs = plt.subplots(nrows=3, ncols=2, figsize=(12, 18))

    # Original Image
    axs[0, 0].imshow(og_img, cmap='gray')
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

    # Masked image
    axs[2, 0].imshow(img_masked)
    axs[2, 0].set_title(f'Masked image with only green pixels visible')
    axs[2, 0].axis('off')

    # Histogram
    axs[2, 1].imshow(plot_image)
    axs[2, 1].axis('off')

    # Turn the percent into an actual percent
    percent = percent_green_pixels * 100

    # Add text to the figure (outside the subplots)
    fig.text(0.5, 0.04, f'Percent of green pixels (green pixels / total pixels): {percent:.2f}%', ha='left', fontsize=12)


    plt.tight_layout()

    # Save the grid to file
    plt.savefig(output_path)


main()