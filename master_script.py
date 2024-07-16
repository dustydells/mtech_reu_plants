from matplotlib import pyplot as plt
from functions import crop_to_square, apply_vegetative_index, calc_live_plants_percentage

# Enter path to quadrat image here.
path = 'raw_photos\\20240531_103740.jpg'

# Enter output path and filename here.
output_path = 'results/master_script_output/20240531_103740_grid.jpg'

# Read in the file in RGB with pyplot (must be in RGB for quadrat crop to work)
img = plt.imread(path)

# CROP TO QUADRAT SQUARE
cropped_img = crop_to_square(img)

# DENOISE IMAGE
# denoised_img = cv2.bilateralFilter(cropped_img, d=9, sigmaColor=75, sigmaSpace=75)

# APPLY VEGETATIVE INDEX
# Determine vegetative index that will be used
index_type = 'rgbvi'

vi_img = apply_vegetative_index(cropped_img, index_type)

# CALCULATE PERCENTAGE OF GREEN PIXELS
'''
You can find out what threshold to use by uncommenting this code and checking out the histogram
made from the values in your image. Try different values and see what works.
'''
# plt.hist(vi_img.flatten(), bins = 100)
# plt.show()

# Determine threshold that will differentiate between live and dead plants
green_threshold = 130

# Calculate a percentage of pixels that are green according to an rgbvi threshold of 130
percent_green_pixels, binary = calc_live_plants_percentage(vi_img, green_threshold)

print(f'Percentage of pixels considered green based on a {green_threshold} threshold of {index_type} image: {percent_green_pixels}')


# Display images in a 2x2 grid
fig, axs = plt.subplots(2, 2, figsize=(12, 12))

# Original Image
axs[0, 0].imshow(img, cmap='gray')
axs[0, 0].set_title('Original Image')
axs[0, 0].axis('off')

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


