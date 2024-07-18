import glob
from master_script import run_script


# Enter path to folder that contains all photos that will be sent through the loop
folder = 'raw_photos\\*'

# Determine parameters
index_type = 'rgbvi'
green_threshold = 130

for i, path in enumerate(glob.glob(folder)):
    # Skip the ones I've already done
    if i <= 19:
        continue
    else:
        output_path = f'results/master_script_output/all_photos/grid_{i}.jpg'

        run_script(path, output_path, index_type, green_threshold, crop=True)

        print('function has run for', path)

'''
last one: function has run for raw_photos\20240613_124346.jpg
'''