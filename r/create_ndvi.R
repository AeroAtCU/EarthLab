# import 2 images given filepaths/ names, convert to ndvi, save output image. will be a function eventaully

# install.packages("package_name")
# for magick, you might have to install imagemagick or it's extras first. Xubuntu wanted:
# sudo apt install libmagick++-dev
# https://cran.r-project.org/web/packages/magick/vignettes/intro.html

get_scriptpath <- function() {
  # location of script can depend on how it was invoked:
  # source() and knit() put it in sys.calls()
  path <- NULL
  
  if(!is.null(sys.calls())) {
    # get name of script - hope this is consisitent!
    path <- as.character(sys.call(1))[2] 
    # make sure we got a file that ends in .R, .Rmd or .Rnw
    if (grepl("..+\\.[R|Rmd|Rnw]", path, perl=TRUE, ignore.case = TRUE) )  {
      return(path)
    } else { 
      message("Obtained value for path does not end with .R, .Rmd or .Rnw: ", path)
    }
  } else{
    # Rscript and R -f put it in commandArgs
    args <- commandArgs(trailingOnly = FALSE)
  }
  return(path)
}

library("here")
library("magick")

here_path = here::here()
script_path = get_scriptpath()

#source(here::here("r","VIHelper.R")) # grab helper functions

cat("===== running =====\n")

#tmp_input <- magick::image_read(rgb_path)
#magick::image_write(tmp_input, path=out_path, format = "png")

cat("script_path:",script_path,"\n")
cat("here_path:",here_path,"\n")
