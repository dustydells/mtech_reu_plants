# mtech_reu_plants
 Professor Graff's REU project on automating vegetation surveys

## About the Project
The purpose of this project is to automate the process of measuring the health of plants in photos of the ground. The photos used in creating this process are primarily images of the ground that contain quadrats (a 1x1 meter pvc pipe square, generally used to quantify a square meter of ground in ecological surveys). There are also some pictures of plucked willow leaves and stems on gray backgrounds.  
![image containing quadrat](raw_photos/20240530_164307.jpg)
![image containing willow leaves](test_photos_greenhouse/image_1.JPG)
These photos can be found in the folders "raw_photos" and "test_photos_greenhouse."

## Usage
The file called "master_script.py" will take the path to one image and return a grid of figures like the images below.  
![Example of output (quadrat)](results/master_script_output/example.jpg)
![Example of output (willow leaves)](results/master_script_output/example_greenhouse.jpg)
It outputs several images representing steps in the editing process in addition to a histogram that displays the distribution of vegetation index values for every pixel.
All functions used by the master script are contained in the file "functions.py". 

## Tips
- The quadrat images were taken on the side of some trails and in some other grassy areas in Butte, Montana on sunny days. The data was collected haphazardly and not exhaustively. Therefore, when using your own photos, it is important to test for your own threshold values.
- If you are using this process to get the vegetation index of many images at once, make sure you resize all the images to a consistent size. The function "resize_square_imgs" was designed to do this.
- Once the images are resized, if you are measuring rock size, it is necessary to calculate the conversion rate of pixels to centimeters every time you have a new batch of photos with a different size than the last. So when you use this process on a batch of photos, you will need to calculate your conversion rate immediately after you resize all images. The function "calc_pixels_to_cm" was designed to do this. 

## Acknowledgements