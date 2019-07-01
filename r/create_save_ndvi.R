create_save_ndvi <- function(rgb_path="", nir_path="", out_path=""){
  # Calculates and save an NDVI image from an existing rgb and nir image.
  #
  # Args:
  #   rgb_path: absolute path to the 3 channel rgb image
  #   nir_path: absolute path to the 1 channel nir image
  #   out_path: asbolute path to the output image. (".../folder/name.png")
  #
  # Returns:
  #   (Intended to) TRUE if no errors occured, FALSE otherwise.
  # 
  # Notes:
  #   Tries to overwrite the output image if it already exists.
  #   Requires packages "raster","rgeos", "rgdal", "RColorBrewer"
  #   rStudio on Linux Mint doesn't has issues with installing rgdal, others
  #   Untesed but should output in any standard formats (png, jpg, etc).
  #
  # For problems on linux:
  #   Took a long time but the following worked eventually on Xubuntu 18.x. In a terminal:
  #   sudo apt update
  #   sudo apt install gdal-bin libgdal-dev libproj-dev
  #   (in rstudio, install the above package with install.packages("x")
  #   this is after many iterations of fruitless installs, and I cannot documentall of them. This was the most recent thing that worked. Remember to source them once you're done with library("x")
  #   Also, don't use Conda as apparently it's got bad pkg version management and is "rigid"

  library("raster")
  library("rgdal")
  library("rgeos")
  library("RColorBrewer")
  
  options(stringsAsFactors = FALSE) # likely uneccessary, but earthdatascience.org likes it.
  
  # make sure files exist
  if (!file.exists(rgb_path) | !file.exists(nir_path)){
    return(FALSE)
  }

  # get rgb and IR images
  rgb <- raster::stack(rgb_path)
  nir <- raster::stack(nir_path)
  
  # calculate the ndvi.
  ndvi <- (nir[[1]] - rgb[[1]]) / (nir[[1]] + rgb[[1]])
  
  # normalize values for png. Currently does really change anything.
  ndvi_norm <- raster::stretch(ndvi, minv = 0, maxv = 255, minq = -1, maxq = 1)
  
  # create output image. Try/Catch/Finally should come later, but have had no errors so far.
  png(filename=out_path) # open file
  
  # create plot
  plot(ndvi_norm,
       main = paste("NDVI of ", basename(rgb_path), sep=""),
       axes = FALSE, box = FALSE)
  
  dev.off() # close file. Stays open in RStudio though.
  
  return(TRUE)
}
