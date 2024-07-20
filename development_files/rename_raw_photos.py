import glob
from matplotlib import pyplot as plt

# IMPORTING FUNCTIONS FROM DIFFERENT DIRECTORY
import sys
import os

# Add the directory containing your module to the Python path
module_path = os.path.abspath(os.path.join("C://Users//dusty//Documents//REU_2024//mtech_reu_plants"))
if module_path not in sys.path:
    sys.path.append(module_path)

from functions import extract_filename_number, reorder_file_paths

# Enter path to folder that contains all photos that will be sent through the loop
folder = '..\\photos\\raw_photos_cropped\\*'
# Arrange the files by the number in the name
files = reorder_file_paths(folder)

# If your images have already been cropped and save, enter a folder here that contains the original photos before they were cropped. 
run_w_already_cropped = True

# Save the filenames in a list - should be in the same order as other reordered folder
if run_w_already_cropped == True:
    raw_imgs_folder = '..\\photos\\raw_photos\\*' # Put the path to the raw images here
    raw_files = reorder_file_paths(raw_imgs_folder) # rearrange the files by key 

for i in range(len(files)):
    print(files[i], raw_files[i])

    # Get number in cropped photo filename so it can be used as the index for the test
    cropped_photo_num = extract_filename_number(files[i])

    # Load in images
    cropped_img = plt.imread(files[i])
    raw_img = plt.imread(raw_files[i])

    # slapdash grid
    fig, axs = plt.subplots(nrows=1, ncols=2, figsize=(12, 6))

    # Arrange images in a side by side grid
    axs[0].imshow(cropped_img)
    axs[1].imshow(raw_img)

    plt.savefig(f'../results/alignment_test/image_{i}.jpg')
    
    # Close the plot so it doesn't slurp up all the memory
    plt.close()

    print(f'figure saved for image {i}')
