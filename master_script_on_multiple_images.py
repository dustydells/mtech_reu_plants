import glob
from matplotlib import pyplot as plt
from master_script import run_script


# Enter path to folder that contains all photos that will be sent through the loop
folder = 'raw_photos_cropped\\*'
files = []
# Get a list of all the files in that folder 
for file in glob.glob(folder):
    files.append(file)


# If your images have already been cropped and save, enter a folder here that contains the original photos before they were cropped. 
run_w_already_cropped = True
# Save the filenames in a list
if run_w_already_cropped == True:
    raw_files = []
    raw_imgs_folder = 'raw_photos\\*' # Put the path to the raw images here
    for raw_file in glob.glob(raw_imgs_folder):
        raw_files.append(raw_file)


# Determine parameters
index_type = 'rgbvi'
green_threshold = 135
crop = True
keep_cropped_image = False

for i, path in enumerate(range(files)):
    # Skip the ones I've already done
    # if i <= 57: # suffering
    #     continue
    # else:
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
            run_script(path, output_path, index_type, green_threshold, crop, raw_imgs_path)

        # Just run the function like normal!!
        else:
            run_script(path, output_path, index_type, green_threshold, crop)

        print(f'function has run for image {i}: {path}')

