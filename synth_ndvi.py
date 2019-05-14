# purpose: read an RGB image in, compute VARI 
# (Visible Atmospherically Resistant Index) values, create an output image.
# VARI equation used: VARI = (green - red) / (green + red - blue)

import numpy as np
import pandas as pd
import imageio

print("Beginning program")

im_read_path = "C:/Users/iaad5777/Documents/git/EarthLab/ex_rgb.png"
im_write_path = "C:/Users/iaad5777/Documents/git/EarthLab/test_vari.png"

im_orig = imageio.imread(im_read_path)
# im[x] is a row of pixels
# im[x][y] is a vector holding the color value, at position x,y
# im[x][y][z] is a pixel's color value

# im[:,:,0] = 0 # takes out all red
# im[1][1][0] == im[1,1,0]

im_new = (im_orig[:,:,1] - im_orig[:,:,0]) / (im_orig[:,:,1] + im_orig[:,:,0] - im_orig[:,:,2])

imageio.imwrite(im_write_path, im_new[:, :])