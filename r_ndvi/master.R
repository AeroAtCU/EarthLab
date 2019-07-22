# Loop through the EVRL dataset and create ndvi images.
# Useful links:
# https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf
# https://www.earthdatascience.org/courses/earth-analytics/multispectral-remote-sensing-data/vegetation-indices-NDVI-in-R/
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# https://www.int-arch-photogramm-remote-sens-spatial-inf-sci.net/XLI-B8/563/2016/isprs-archives-XLI-B8-563-2016.pdf

# ":s/^/# /" (comment selected block) will crash rstudio (vim input mode)

# this_wd <- getwd() # should be better, but inconsistent. Half the time defaults to ../Documents instead of .../git/...
rm(list=ls()) # clear all variables. Bad practice but seemingly necessary to ensure certain settings change
cat("\014") # send C-L to console to clear
# setwd("C:/Users/iaad5777/Documents/git/EarthLab/r") # harcoded for now
# setwd("C:/Users/iaad5777/Documents/git/EarthLab/r") # harcoded for now. necessary to source the create
# On linux, getwd() on starup returns /home/<username>. on windows, half the time
# does that, half the time print /.../EarthLab/r
library(raster)
library(tiff)

this_wd <- "/home/ian/Documents/git/EarthLab/r" # for linux #======#
setwd(this_wd)
source(file.path(this_wd,"create_save_ndvi.R"))

# needs work
# this_wd <- "C:/Users/iaad5777/Documents/git/EarthLab/r" # harcoded for now
images_path <- file.path(dirname(this_wd),"nirscene1") # assuming folder is in parent
out_path <- file.path(dirname(this_wd),"r_tmpout") # assuming folder is in parent
img_num <- "0033" # eventually, how to convert int to 0 padded string?
subfolder <- "forest"
subfolder_list <- c("country", "field", "forest", "mountain", "water") # list of usable ivrl folders

rgb_path <- (file.path(images_path, subfolder, (paste(img_num,"_rgb.tiff",sep=""))))
nir_path <- (file.path(images_path, subfolder, (paste(img_num,"_nir.tiff",sep=""))))
out_path <- file.path(dirname(this_wd),"r_tmpout","asdf.png") # assuming folder is in parent

rgb <- readTIFF(rgb_path)
ndvi <- rgb # should duplicate
nir <- readTIFF(nir_path)
# red is rgb[,,1]

# should make red
#rgb[,,2]=0
#rgb[,,3]=0

ndvi[,,1] = (nir[,1] - rgb[,,1]) / (nir[,1] - rgb[,,1])
ndvi[,,2] = 0
ndvi[,,3] = 0

writeTIFF(ndvi, out_path)

# create_save_ndvi(rgb_path, nir_path, out_path)
