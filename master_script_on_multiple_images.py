import glob
from matplotlib import pyplot as plt
from master_script import run_script


# Enter path to folder that contains all photos that will be sent through the loop
folder = 'test_photos_greenhouse\\*'

# Determine parameters
index_type = 'exg'
green_threshold = 155
crop = False

for i, path in enumerate(glob.glob(folder)):
    # # Skip the ones I've already done
    # if i <= 19:
    #     continue
    # else:
        output_path = f'results/master_script_output/all_photos/greenhouse_grid_{i}.jpg'

        if crop == True: # if the images are getting cropped, save it to file
            cropped_img = run_script(path, output_path, index_type, green_threshold, crop)

            # Save the cropped images so you never have to go through that process again
            plt.imsave(f'raw_photos_cropped/image_{i}.jpg', cropped_img)

        else:
            run_script(path, output_path, index_type, green_threshold, crop)

        print(f'function has run for image {i}: {path}')

