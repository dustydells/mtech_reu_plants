import glob
from master_script import run_script


# Enter path to folder that contains all photos that will be sent through the loop
folder = 'raw_photos\\*'

for file in glob.glob(folder):
    print('function has run for', file)
