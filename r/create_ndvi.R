# https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf
# https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-data/vegetation-indices-NDVI-in-R/

# for magick, you might have to install imagemagick or it's extras first. Xubuntu wanted:
# sudo apt install libmagick++-dev
# ":s/^/# /" will crash rstudio
rm(list=ls()) # clear all variables. Apparently bad practice but seemingly necessary

library("magick")
library("raster")
library("rgeos")
library("rgdal")
library("RColorBrewer")
options(stringsAsFactors = FALSE) # want strings to be string s
#source("some_function.R")

# Define filepaths and strings (some will need to be looped)
# this_wd <- getwd()
this_wd <- "C:/Users/iaad5777/Documents/git/EarthLab/r"
images_path <- file.path(dirname(this_wd),"nirscene1") # assuming folder is in parent
img_num <- "0001" # eventually, how to convert int to 0 padded string?
subfolder <- "forest"

# get normal and IR images
rgb <- stack(file.path(images_path, subfolder, (paste(img_num,"_rgb.tiff",sep=""))))
out <- rgb
nir <- stack(file.path(images_path, subfolder, (paste(img_num,"_nir.tiff",sep=""))))

# calculate the ndvi. Why img[[x]]?
ndvi <- (nir[[1]] - rgb[[1]]) / (nir[[1]] + rgb[[1]])

# normalize values so it looks good
ndvi_norm <- raster::stretch(ndvi, minv = 0, maxv = 255, minq = -1, maxq = 1)

# create output image.
plot(ndvi_norm,
     main = paste(img_num,"_nir.tiff",sep=""),
     axes = FALSE, box = FALSE)