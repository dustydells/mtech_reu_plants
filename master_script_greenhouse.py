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

    # Convert image to RGB for display later
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

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
            pn.geom_histogram(bins = 100) +
            pn.labs(
                 x='Intensity',
                 y='Count',
                 title=f'Distribution of pixel intensity of {index_type} image'
            ) +
            pn.theme_classic()
    )

    # plot.show()

    # Render the plotnine plot to an image
    fig = plot.draw()
    fig.savefig('plotnine_plot.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plot_image = plt.imread('plotnine_plot.png')
    
    # Display images in a 2x2 grid
    fig, axs = plt.subplots(2, 2, figsize=(12, 12))

    # Original Image
    axs[0, 0].imshow(img, cmap='gray')
    axs[0, 0].set_title('Original Image')
    axs[0, 0].axis('off')

    # Image modified by vegetative index
    axs[1, 0].imshow(vi_img, cmap='viridis')
    axs[1, 0].set_title(f'Image modified by {index_type}')
    axs[1, 0].axis('off')

    # Masked image
    axs[1, 0].imshow(img_masked, cmap='viridis')
    axs[1, 0].set_title(f'Image masked by {green_threshold} threshold')
    axs[1, 0].axis('off')

    # Plot
    axs[1, 1].imshow(plot_image)
    axs[1, 1].axis('off')

    plt.tight_layout()
    plt.show()

    # cv2.imshow('mask', img_masked)

    # cv2.waitKey(0)
    # cv2.destroyAllWindows()


main()