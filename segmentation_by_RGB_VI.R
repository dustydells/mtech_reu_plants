library(tidyverse)
library(rasterVis)
library(raster)
library(OpenImageR)
library(RImagePalette)
library(jpeg)
library(sp)
library(lattice)
library(latticeExtra)


file_path <- 'test_photos/test_image_22.jpg'

# Read in the image
img <- stack(file_path)

# Show the image
plotRGB(img, 1, 2, 3)
