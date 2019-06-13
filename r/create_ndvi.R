# import 2 images given filepaths/ names, convert to ndvi, save output image. will be a function eventaully
# https://www.agisoft.com/pdf/PS_1.3%20-Tutorial%20(BL)%20-%20Orthophoto,%20DEM%20(GCPs).pdf
# save.as

# install.packages("package_name")
# for magick, you might have to install imagemagick or it's extras first. Xubuntu wanted:
# sudo apt install libmagick++-dev
# https://cran.r-project.org/web/packages/magick/vignettes/intro.html

library("magick")

# get working directories. dirname gives parent.
this_wd = getwd()
this_parent = dirname(this_wd)
nirscene1_path = file.path(this_parent,"nirscene1") # hardcoded but should always be the same if using correct dataset.
out_path <- "C:\\Users\\iaad5777\\Documents\\git\\EarthLab\\r_tmpout" # bad

rgb_path = file.path(nirscene1_path,"country","0000_rgb.tiff")
nir_path = file.path(nirscene1_path,"country","0000_nir.tiff")

rgb <- magick::image_read(rgb_path)
nir <- magick::image_read(nir_path)
red <- magick::image_channel(tmp, "red")

red_nir <- c(nir, red)
red_nir_sub <- magick::image_flatten(red_nir,"Minus")

magick::image_browse(red_nir_sub)
magick::image_write(tmp_input, path=out_path, format = "png") #cannot write the image on student computer, not admin
#