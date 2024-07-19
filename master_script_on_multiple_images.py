import glob
from matplotlib import pyplot as plt
from functions import reorder_file_paths
from master_script import run_script

# Enter path to folder that contains all photos that will be sent through the loop
folder = 'raw_photos_cropped\\*'
# Get a list of all the files in that folder in order of number
files = reorder_file_paths(folder)

# If your images have already been cropped and save, enter a folder here that contains the original photos before they were cropped. 
run_w_already_cropped = True
# Save the filenames in a list
if run_w_already_cropped == True:
    raw_imgs_folder = 'raw_photos_numbered\\*' # Put the path to the raw images here
    raw_files = reorder_file_paths(raw_imgs_folder)

# Check ur filenames
# for i in range(len(files)):
#     print(files[i], raw_files[i])

# Determine parameters
index_type = 'rgbvi'
green_threshold = 135
crop = False
keep_cropped_image = False

for i in range(len(files)):
    # Skip the ones I've already done
    # if i <= 57: # suffering
    #     continue
    # else:
        path = files[i]
        output_path = f'results/master_script_output/all_photos/grid_{i}.jpg'

        # if the images are getting cropped, save it to file
        if crop == True: 
            cropped_img = run_script(path, output_path, index_type, green_threshold, crop)

            # If you want to save the cropped images in a folder 
            if keep_cropped_image == True:
                # Save the cropped images so you never have to go through that process again
                plt.imsave(f'raw_photos_cropped/image_{i}.jpg', cropped_img)

        # If the files have already been cropped and saved in a folder
        elif run_w_already_cropped == True:
            raw_imgs_path = raw_files[i]
            run_script(path, output_path, index_type, green_threshold, crop, raw_imgs_path=raw_imgs_path)
            print(f'script ran for image {i}')

        # Otherwise, just run the function like normal!!
        else:
            run_script(path, output_path, index_type, green_threshold, crop)

        print(f'function has run for image {i}: {path}')

