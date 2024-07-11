import cv2
from matplotlib import pyplot as plt
from functions import crop_to_square, apply_vegetative_index, calc_live_plants_percentage

# Enter path to folder that contains quadrat images here
path = 'raw_photos\\20240531_103541.jpg'

# Read in the file in RGB with pyplot (must be in RGB for quadrat crop to work)
img = plt.imread(path)

# CROP TO QUADRAT SQUARE
cropped_img = crop_to_square(img)

# DENOISE IMAGE
# denoised_img = cv2.bilateralFilter(cropped_img, d=9, sigmaColor=75, sigmaSpace=75)

# APPLY VEGETATIVE INDEX
rgbvi_img = apply_vegetative_index(cropped_img, 'rgbvi')

# WRITE VI DATA INTO A CSV
# Calculate a percentage of pixels that are green according to an rgbvi threshold of 130
percent_green_pixels = calc_live_plants_percentage(vi_img=rgbvi_img, green_threshold=130)