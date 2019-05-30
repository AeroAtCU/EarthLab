# get 2 images, convert to ndvi, save output image. will be a function
# for ndvi_ivrl.R  eventually

# run these once
# install.packages("package") [tidyverse, magick]
cat("\014") # send Ctrl+L to consle (clear)
library("here")
library("imager") # probably delete imager and use magick
library("magick")
source(here::here("r","VIHelper.R")) # grab helper functions

# program begins
# rgb_path <- here::here("nirscene1","country","0000_rgb.tiff")
# nir_path <- here::here("nirscene1","country","0000_nir.tiff")

testPrint()