# https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf
# https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-data/vegetation-indices-NDVI-in-R/

# for magick, you might have to install imagemagick or it's extras first. Xubuntu wanted:
# sudo apt install libmagick++-dev
rm(list=ls())

library("magick")
library("raster")
library("rgeos")
library("rgdal")
library("RColorBrewer")
options(stringsAsFactors = FALSE) # want strings to be string s

this_wd <- getwd()
images_path <- file.path(dirname(this_wd),"nirscene1") # assuming folder is in parent

img_num <- "0000" # eventually, how to convert int to 0 padded string?
subfolder <- "country"

rgb <- stack(file.path(images_path, subfolder, (paste(img_num,"_rgb.tiff",sep=""))))
nir <- stack(file.path(images_path, subfolder, (paste(img_num,"_nir.tiff",sep=""))))

ndvi <- (nir[[1]] - rgb[[3]]) / (nir[[1]] + rgb[[3]])

plot(ndvi,
     main = paste(img_num,"_nir.tiff",sep=""),
     axes = FALSE, box = FALSE)