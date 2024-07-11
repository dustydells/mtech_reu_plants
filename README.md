# mtech_reu_plants
 Professor Graff's REU project on automating vegetation surveys

## About the Project
The initial purpose of this project is to automate the process of segmenting ground photos into 4 different categories:
1. Live vegetation
2. Dead vegetation
3. Rocks > 2 in (5.08 cm)
4. other
These categories are designed to suit the requirements of the BRES ecological survey.

## Usage
The file called "master_script.py" contains an example of the sequence in which to use the functions. all functions are contained in 
the file "functions.py". 

## Tips
- If you are using this process to get the vegetative index of many images at once, make sure you resize all the images to a consistent size. The function "resize_square_imgs" was designed to do this.

## Acknowledgements