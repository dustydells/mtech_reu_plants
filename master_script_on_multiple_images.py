import glob
from matplotlib import pyplot as plt
from master_script import run_script, list_all_paths


# Enter path to folder that contains all photos that will be sent through the loop
folder = 'raw_photos_cropped\\*'
# Get a list of all the files in that folder 
files = list_all_paths(folder)
print(files)

# If your images have already been cropped and save, enter a folder here that contains the original photos before they were cropped. 
raw_imgs_folder = 'raw_photos\\*'
run_w_already_cropped = True

# Determine parameters
index_type = 'rgbvi'
green_threshold = 135
crop = True
keep_cropped_image = False

# for i, path in enumerate(glob.glob(folder)):
#     # Skip the ones I've already done
#     # if i <= 57: # suffering
#     #     continue
#     # else:
#         output_path = f'results/master_script_output/all_photos/grid_{i}.jpg'

#         if crop == True: # if the images are getting cropped, save it to file
#             cropped_img = run_script(path, output_path, index_type, green_threshold, crop)

#             if keep_cropped_image == True:
#                 # Save the cropped images so you never have to go through that process again
#                 plt.imsave(f'raw_photos_cropped/image_{i}.jpg', cropped_img)

#         elif run_w_already_cropped == True:
#             raw_imgs_path = f'{raw_imgs_folder}'
#             run_script()

#         else:
#             run_script(path, output_path, index_type, green_threshold, crop)

#         print(f'function has run for image {i}: {path}')

