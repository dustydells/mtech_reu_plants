'''
Run this script to get the vegetation index information from images. 
Specify your parameters in the main function.
'''

import cv2
import pandas as pd
import plotnine as pn
from skimage import img_as_ubyte
from matplotlib import pyplot as plt
from functions import crop_to_square, apply_vegetation_index, calc_live_plants_percentage

def main():
    '''
    Determine your parameters here. 
    '''

    # Enter path to input image here.
    path = 'raw_photos/20240613_124445.jpg'

    # Enter output path and filename here.
    output_path = 'results/master_script_output/example.jpg'

    # Determine vegetation index that will be used
    index_type = 'RGBVI' # RGBVI worked well for my quadrat photos, ExG worked well on the willow leaf photos - feel free to experiment

    # INVESTIGATE HISTOGRAM
    '''
    You can find out what threshold to use by uncommenting this code and checking out the histogram
    made from the values in your image. Try different values and see what works.
    '''
    # plt.hist(vi_img.flatten(), bins = 100)
    # plt.show()

    # Determine threshold that will differentiate between live and dead plants.
    # Or experiment with skimage filters like otsu and median.
    green_threshold = 135 # 130 worked well on quadrat photos. 160 worked well on willow leaf photos. 

    # Determine whether your photos need to be cropped or not. 
    crop = True

    # Run the process
    if crop == False:
        run_script(path, output_path, index_type, green_threshold, crop)
    elif crop == True: # If the image gets cropped, you can output it to a file so you only have to crop it once
        cropped_img = run_script(path, output_path, index_type, green_threshold, crop)
        plt.imsave(f'results/image_cropped.jpg', cropped_img)




def run_script(path, output_path, index_type, green_threshold, crop, denoise=False,):
    '''
    Run the entire process with the parameters you specified.

    Parameters:
        path:
            String. Path to the input image
        output_path:
            String. Path of the output image that will be saved
        index_type:
            String. The vegetation index you'd like to use. 
            Options: exg, exr, grvi, vari, rgbvi, exg-exr
        green_threshold:
            Integer. The cutoff VI value that differentiates between green 
            and not green. Example: 130 works well for images on RGBVI scale. 
        crop:
            Boolean. Whether you want to crop your image to a square using the napari
            GUI or not.
        denoise:
            Boolean. Whether you want to denoise the image or not (default: False)
    '''

    # Read in the file in RGB with pyplot (must be in RGB for quadrat crop to work)
    img = plt.imread(path)
    og_img = img # Save the original image so it can be included in the grid and saved to file later

    # CROP TO SQUARE
    if crop == True:
        img = crop_to_square(img)
        cropped_img = img # Save the cropped image so it can be included in the grid later

    # DENOISE IMAGE
    if denoise == True:
        img = cv2.bilateralFilter(img, d=9, sigmaColor=75, sigmaSpace=75)

    # APPLY VEGETATION INDEX
    vi_img = apply_vegetation_index(img, index_type)

    # THRESHOLD IMAGE
    binary = vi_img >= green_threshold

    # Calculate a percentage of pixels that are green according to your threshold cutoff
    percent_green_pixels = calc_live_plants_percentage(binary)

    # Turn the percent into an actual percent
    percent_green_pixels = percent_green_pixels * 100

    # Convert binary into ubyte so it can be used as a mask and displayed
    binary = img_as_ubyte(binary)

    # Apply the binary mask to the VI image
    # Only keep the pixels where the binary mask is white (255)
    img_masked_display = cv2.bitwise_and(img, img, mask = binary)
    img_masked_calc = cv2.bitwise_and(vi_img, vi_img, mask = binary)

    # Convert image into dataframe
    df = pd.DataFrame(img_masked_calc.flat, columns=['intensity'])

    # Filter out all the zero values
    df = df[df['intensity'] != 0]

    # Create the plot
    plot = (pn.ggplot(df) + 
            pn.aes(x='intensity') + 
            pn.geom_histogram(bins = 100, fill = 'lightseagreen') +
            pn.labs(
                x = 'Vegetation Index Value (Pixel Intensity)',
                y = 'Count',
                title = f'Distribution of vegetation index values of green pixels in {index_type} image',
                caption = f'Percent of green pixels (green pixels / total pixels): {percent_green_pixels:.2f}%'
                ) +
            pn.theme_classic()
    )

    # Render the plotnine plot to an image
    fig = plot.draw()
    fig.savefig('results/plotnine_plot.png', dpi=300, bbox_inches='tight', pad_inches=0.1)
    plot_image = plt.imread('results/plotnine_plot.png')

    # Explicitly delete the plot object because it kept being referenced by something and slowing things down
    del plot
    # Close the plot so it doesn't slurp up all the memory
    plt.close()
    
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

    # Image modified by vegetation index
    axs[1, 0].imshow(vi_img, cmap='viridis')
    axs[1, 0].set_title(f'Image modified by {index_type}')
    axs[1, 0].axis('off')

    # Binary image of pixels considered green
    axs[1, 1].imshow(binary, cmap='gray')
    axs[1, 1].set_title(f'Binary image of pixels considered green by {green_threshold} threshold')
    axs[1, 1].axis('off')

    # Masked image
    axs[2, 0].imshow(img_masked_display)
    axs[2, 0].set_title(f'Masked image with only green pixels visible')
    axs[2, 0].axis('off')

    # Histogram
    axs[2, 1].imshow(plot_image)
    axs[2, 1].axis('off')

    # Add text to the figure (outside the subplots)
    # fig.text(0.5, 0.04, f'Percent of green pixels (green pixels / total pixels): {percent:.2f}%', ha='left', fontsize=12)

    plt.tight_layout()

    # Save the grid to file
    plt.savefig(output_path)

    # If the image was cropped, return that image so it can be saved to your files outside
    if crop == True: 
        return cropped_img


main()