# Functions to help with general Vegitation Index procedures
calcNDVI <- function(rgb_im, nir_im, verbose = FALSE) {
  # Calculate the normalized difference vegitation index
  #
  # Args:
  #   rgb_im: x*y*3 dataframe (?) holding original color vals
  #   nir_im: x*y*any dataframe (?) holding near infrared vals
  #   verbosity: if TRUE, print small updates. else nothing.
  #
  # Returns:
  #   an x*y*3 dataframe (?) of zeros with straight NDVI vals on G channel
  cat("calcNDVI called")
}

testPrint <- function(input="") {
  # test if function calls work
  cat("asdf",input,"\n")
}
