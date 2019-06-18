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
  #   Requires packages "raster", "rgeos", "rgdal", "RColorBrewer" (Probably?)
  #   Should output in any standard formats (png, jpg, etc). Only tested with ".png"
  
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