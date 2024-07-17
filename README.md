# mtech_reu_plants
 Professor Graff's REU project on automating vegetation surveys

## About the Project
The purpose of this project is to automate the process of measuring the health of plants in photos of the ground. The photos used in creating this process are pictures of plucked willow leaves and stems on gray backgrounds, and primarily on images of the ground that contain quadrats (a 1x1 meter pvc pipe square, generally used to quantify a square meter of ground in ecological surveys).  
![image containing quadrat](raw_photos/20240530_164307.jpg)
![image containing willow leaves](test_photos_greenhouse/image_1.JPG)
These photos can be found in the folders "raw_photos" and "test_photos_greenhouse."

## Usage
The file called "master_script.py" will take the path to one image and run the entire process on that image. The process applies your vegetation index of choice to the image and calculates the percentage of green pixels, and outputs a histogram displaying the distribution of vegetation index values. 
![Example of output](results/master_script_output/example.jpg)
All functions used by the master script are contained in the file "functions.py". 

## Tips
- If you are using this process to get the vegetative index of many images at once, make sure you resize all the images to a consistent size. The function "resize_square_imgs" was designed to do this.
- Once the images are resized, if you are measuring rock size, it is necessary to calculate the conversion rate of pixels to centimeters every time you have a new batch of photos with a different size than the last. So when you use this process on a batch of photos, you will need to calculate your conversion rate immediately after you resize all images. The function "calc_pixels_to_cm" was designed to do this. 

## Acknowledgements