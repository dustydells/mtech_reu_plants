import glob
from matplotlib import pyplot as plt
from functions import extract_filename_number

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
    axs[0, 0].imshow(cropped_img)
    axs[0, 1].imshow(raw_img)

    plt.savefig(f'results/alignment_test/image_{cropped_photo_num}.jpg')

    print(f'figure saved for image {cropped_photo_num}')
