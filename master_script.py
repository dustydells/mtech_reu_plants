from matplotlib import pyplot as plt
from functions import crop_to_square

# Enter path to folder that contains quadrat images here
path = 'raw_photos\\20240531_103541.jpg'

# CROP IMAGES
cropped_img = crop_to_square(path)

plt.imshow(cropped_img)