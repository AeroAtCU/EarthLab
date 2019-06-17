# Import rgb, nir image and create ndvi plot. Eventually loop through entire set and export Vi images.

# Useful links:
# https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf
# https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-data/vegetation-indices-NDVI-in-R/
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/

# ":s/^/# /" (comment selected block) will crash rstudio in vim input mode
rm(list=ls()) # clear all variables. Apparently bad practice but seemingly necessary
cat("\014") # send C-L to console to clear

# techincally don't need to source these if using package::fun for everything
#source("some_function.R")
library("raster")
library("rgeos")
library("rgdal")
library("RColorBrewer")
options(stringsAsFactors = FALSE) # want strings to be string s

# Define filepaths and strings (some will need to be looped)
# this_wd <- getwd() # inconsistent
this_wd <- "C:/Users/iaad5777/Documents/git/EarthLab/r" # harcoded for now
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