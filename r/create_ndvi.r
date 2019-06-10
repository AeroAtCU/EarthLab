# import 2 images given filepaths/ names, convert to ndvi, save output image. will be a function eventaully

# install.packages("package_name")
# for magick, you might have to install imagemagick or it's extras first. Xubuntu wanted:
# sudo apt install libmagick++-dev
# https://cran.r-project.org/web/packages/magick/vignettes/intro.html
cat("\014") # send Ctrl+L to consle (clear)
library("here")
library("magick")
source(here::here("r","VIHelper.R")) # grab helper functions
cat(" ===== ===== =====\n","===== begin =====\n","===== ===== =====\n")

# program begins
rgb_path <- here::here("nirscene1","country","0000_rgb.tiff")
nir_path <- here::here("nirscene1","country","0000_nir.tiff")
out_path <- here::here("r_tmpout","a.png")

tmp_input <- magick::image_read(rgb_path)
magick::image_write(tmp_input, path=out_path, format = "png")

cat(rgb_path,"\n")
testPrint("some string")
