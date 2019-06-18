create_save_ndvi <- function(rgb_path="", nir_path="", out_path=""){
  # Input: Absolute paths to rgb, nir, and output image.
  # Output: True/False on success of function (import, calculation, img writing)
  # Notes: Tries to overwrite the output image if it already exists.
  #        Requires packages "raster", "rgeos", "rgdal", "RColorBrewer" (Probably?)
  #        Should output in any standard formats (png, jpg, etc). Only tested with ".png"
  
  options(stringsAsFactors = FALSE) # seemingly uneccessary
  
  # make sure files exist
  if (!file.exists(rgb_path) | !file.exists(nir_path)){
    return(FALSE)
  }

  # get rgb and IR images
  rgb <- raster::stack(rgb_path)
  nir <- raster::stack(nir_path)
  
  # calculate the ndvi.
  ndvi <- (nir[[1]] - rgb[[1]]) / (nir[[1]] + rgb[[1]])
  
  # normalize values (for png) so it looks better. Currently does not change much
  ndvi_norm <- raster::stretch(ndvi, minv = 0, maxv = 255, minq = -1, maxq = 1)
  
  # create output image. Try/Catch/Finally should come later, but have had no errors so far.
  png(filename=out_path) # open file
  
  plot(ndvi_norm,
       main = paste("NDVI of ", basename(rgb_path), sep=""),
       axes = FALSE, box = FALSE)
  
  dev.off() # close file. Stays open in RStudio though.
  
  return(TRUE)
}