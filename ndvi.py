# purpose: read an rgb and nir image, combine and export into an ndvi
# (and possibly other xVI) images

import numpy as np
# import pandas as pd # for dataframe
import imageio


def crop_smallest(im1, im2):
    # input: im1, im2 3 dimensional numpy arrays
    # purpose: crop the larger to the dimenions of the smaller. 
    # Clips larger values (rightmost x and topmost y)
    im1_shape = np.shape(im1)
    im2_shape = np.shape(im2)

    if not (im1_shape[0] == im2_shape[0]):
        print("dimension mismatch on y axis, cropping")
        if im1_shape[0] > im2_shape[0]:
            im1 = im1[0:im2_shape[0], :, :]
        else:
            im2 = im2[0:im1_shape[0], :, :]

    if not (im1_shape[1] == im2_shape[1]):
        print("dimension mismatch on x axis, cropping")
        if im1_shape[1] > im2_shape[1]:
            im1 = im1[:, 0:im2_shape[1], :]
            return im1, im2
        else:
            im2 = im2[:, 0:im1_shape[1], :]
            return im1, im2

    if not (im1[0] == im2[0] and im1[1] == im2[1]):
        print("crop unsuccessful, exiting")
        exit()

    return im1, im2


def normalize_255(im1, im_color):
    # input: im1 f64 numpy array with some sort of vegetation index info
    # input: im_color numpy array holding original rgb values of the xVI image
    # purpose: take an xVI image and make it human readable and jpg exportable
    im_norm = (im1 / np.max(im1)) * 255  # gives greatest contrast w/out losing data
    im_norm[im_norm < 0] = 0  # removes negative values (water, soil)
    im_norm = np.uint8(im_norm)  # round off and make uint8 (imageio likes it)

    im_norm[:, :, 1] = im_norm[:, :, 0]  # add plant data on green channel
    im_norm[:, :, 0] = im_color[:, :, 0]  # add visual red
    im_norm[:, :, 2] = im_color[:, :, 2]  # add visual blue (uness but looks better)

    return im_norm


def IVRL_get_image(full_in_path):
    #categories = ["country", "field", "forest", "indoor", "mountain", "oldbuilding", "street", "urban", "water"]
    # Image and Visual Representation Lab
    base = imageio.imread(full_in_path)
    im1 = base[0:1,2:3,:]
    im2 = base[0:1,2:3,:]
    
    return im1, im2

# define image paths
prefix = "landscape"
path = "C:/Users/iaad5777/Documents/git/EarthLab/photos/"
rgb_name = prefix + "_rgb.jpg"
nir_name = prefix + "_nir.jpg"

# import images
rgb = imageio.imread(path + rgb_name)
nir = imageio.imread(path + nir_name)  # all nir pixel values same

# crop images to smallest dimensions, get dimensions
rgb, nir = crop_smallest(rgb, nir)
x_length = np.shape(rgb)[0]
y_length = np.shape(rgb)[1]

# define data for later use
red = np.zeros((x_length, y_length, 3))
ndvi = np.zeros((x_length, y_length, 3))
savi = np.zeros((x_length, y_length, 3))
L = 0.5  # constant for SAVI

# calculate vegitation indexes
# NDVI: Normalized Difference Veg Idx
# SAVI: Soil Adjusted Veg Idx
red[:, :, 0] = rgb[:, :, 0]  # extract just red channel

ndvi[:, :, 0] = (nir[:, :, 0] - red[:, :, 0]) / (red[:, :, 0] + nir[:, :, 0])
savi[:, :, 0] = ((1 + L) * (nir[:, :, 0] - red[:, :, 0])) / (nir[:, :, 0] + red[:, :, 0] + L)

# normalize values for better readability
ndvi_norm = normalize_255(ndvi, rgb)
savi_norm = normalize_255(savi, rgb)

if np.array_equal(ndvi_norm, savi_norm):
    print("ndvi and savi are somehow the same")

# write image
imageio.imwrite(path + prefix + "_ndvi.jpg", ndvi_norm[:, :])
# imageio.imwrite(path + prefix + "_savi.jpg", savi_norm[:, :])
# savi ends up having the same values for some reason