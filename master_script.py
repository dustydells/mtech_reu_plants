import cv2
from matplotlib import pyplot as plt
from functions import crop_to_square

# Enter path to folder that contains quadrat images here
path = 'raw_photos\\20240531_103541.jpg'

# CROP IMAGES
cropped_img = crop_to_square(path)

cv2.imshow('cropped image', cropped_img)

cv2.waitKey(0)
cv2.destroyAllWindows()