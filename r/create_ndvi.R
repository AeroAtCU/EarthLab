# Input: Absolute paths to rgb, nir, and output image.
# Output: True/False on success of function (import, calculation, img writing)

# techincally don't need to source these if using package::fun for everything
#library("raster")
#library("rgeos")
#library("rgdal")
#library("RColorBrewer")
options(stringsAsFactors = FALSE) # want strings to be string s

# Define filepaths and strings (some will need to be looped)
# this_wd <- getwd() # inconsistent
this_wd <- "C:/Users/iaad5777/Documents/git/EarthLab/r" # harcoded for now
images_path <- file.path(dirname(this_wd),"nirscene1") # assuming folder is in parent
out_path <- file.path(dirname(this_wd),"r_tmpout") # assuming folder is in parent
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
png(filename=file.path(out_path,"b.png"))
plot(ndvi_norm,
     main = paste(img_num,"_nir.tiff",sep=""),
     axes = FALSE, box = FALSE)
dev.off()
