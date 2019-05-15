# purpose: read an rgb and nir image, combine and export into an ndvi image
# 

import numpy as np
# import pandas as pd # for dataframe
import imageio

def crop_smallest(im1, im2):
    # purpose: given two numpy arrays (imagio images), crop the larger to the 
    # dimenions of the smaller. Clips larger values (rightmost x and topmost y)
    im1_shape = np.shape(im1)
    im2_shape = np.shape(im2)

    if not(im1_shape[0] == im2_shape[0]):
        print("dimension mismatch on y axis, cropping")
        if (im1_shape[0] > im2_shape[0]):
            im1 = im1[0:im2_shape[0],:,:]
        else:
            im2 = im2[0:im1_shape[0],:,:]
    
    if not(im1_shape[1] == im2_shape[1]):
        print("dimension mismatch on x axis, cropping")
        if (im1_shape[1] > im2_shape[1]):
            im1 = im1[:,0:im2_shape[1],:]
            return im1, im2
        else:
            im2 = im2[:,0:im1_shape[1],:]
            return im1, im2
        
    if not(im1[0] == im2[0] and im1[1] == im2[1]):
        print("crop unsuccessful, exiting")
        exit()

    return im1, im2

# define image paths
prefix = "landscape"

path = "C:/Users/iaad5777/Documents/git/EarthLab/photos/"
rgb_name = prefix + "_rgb.jpg"
nir_name = prefix + "_nir.jpg"

# import images
rgb_im = imageio.imread(path + rgb_name)
nir_im = imageio.imread(path + nir_name) # all nir pixel values same

# crop images to smallest dimensions, get dimensions
rgb_im, nir_im = crop_smallest(rgb_im, nir_im)
rgb_shape = np.shape(rgb_im)
nir_shape = np.shape(nir_im)

# calculate pure ndvi values (only red and nir)
# unsure why red is still needed but does not currently work using rgb_im
red_im = np.zeros((rgb_shape[0], rgb_shape[1], 3))
red_im[:,:,0] = rgb_im[:,:,0]

ndvi_im = np.zeros((rgb_shape[0], rgb_shape[1], 3))
ndvi_im[:,:,0] = (nir_im[:,:,0] - red_im[:,:,0]) / (red_im[:,:,0] + nir_im[:,:,0])

# normalize values for better readability
ndvi_norm_im = ( (ndvi_im) / np.max(ndvi_im) ) * 255 # scale by largest value
ndvi_norm_im[ndvi_norm_im < 0] = 0 # remove neg ndvi values (water, land)
ndvi_norm_im = np.uint8(ndvi_norm_im) # convert to work with imageio jpg

ndvi_norm_im[:,:,1] = ndvi_norm_im[:,:,0] # add NDVI on green channel
ndvi_norm_im[:,:,0] = rgb_im[:,:,0] # add visual red 
ndvi_norm_im[:,:,2] = rgb_im[:,:,2] # add visual blue (for looks)

# write image
imageio.imwrite(path + prefix + "_ndvi.jpg", ndvi_norm_im[:,:])