# for creating ndvi images from the "Image and Visual Represtatino Lab" IVRL
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# for this to work on a personal computer, change the in_path variable to whatever it is on your machine

import numpy as np
import imageio
import os
import sys


def normalize_255(im1, im_color):
    # input: im1 f64 numpy array with some sort of vegetation index info
    # input: im_color numpy array holding original rgb values of the xVI image
    # purpose: take an xVI image and make it human readable and jpg exportable
    im_norm = im1
    im_norm[im_norm > 10] = 0  # remove large outliers (works b/c functions should always normalize)
    im_norm[im_norm > 1] = 1 # remove outliers (AFAIK, veg idx should only go -1:1)
    im_norm[im_norm < 0] = 0  # removes negative values (water, soil)
    im_norm = (im_norm / np.max(im1)) * 255  # gives greatest contrast w/out losing data
    im_norm = np.uint8(im_norm)  # round off and make uint8 (imageio likes it)

    im_norm[:, :, 0] = im_color[:, :, 0]  # add visual red
    # im_norm[:, :, 2] = im_color[:, :, 2]  # add visual blue (uness but looks better)

    return im_norm


def check_shape(nir, rgb):
    if np.shape(rgb)[0] != np.shape(nir)[0] or np.shape(rgb)[1] != np.shape(nir)[1]:
        print("Dimension Mismatch, exiting")
        sys.exit(1)

def calc_evi(nir, rgb):
    check_shape(nir, rgb) # make sure sizes are equal
    xleng = np.shape(rgb)[0]
    yleng = np.shape(rgb)[1]
    
    L, C1, C2, G = 1, 6, 7.5, 2.5 # define constants for evi equation
    
    # create base zero arrays
    red = np.zeros((xleng, yleng, 3))
    blue = np.zeros((xleng, yleng, 3))
    evi = np.zeros((xleng, np.shape(rgb)[1], 3))
    numer = np.zeros((xleng, np.shape(rgb)[1], 3))
    denom = np.zeros((xleng, np.shape(rgb)[1], 3))
    
    # doesn't like it when using rgb, so extract one color per channel
    red[:,:,0] = rgb[:,:,0]
    blue[:,:,2] = rgb[:,:,2]
    
    # run calculation. np.divide(options) prevents divion by zero (sets any/0 to 0)
    numer = nir - red[:,:,0]
    denom = (nir + C1*red[:,:,0] - C2*blue[:,:,2] + L)
    evi[:,:,1] = G * (np.divide(numer, denom, out=np.zeros_like(numer), where=denom!=0))
    
    evi_norm = normalize_255(evi, rgb)
    
    return evi_norm, evi

def calc_ndvi(nir, rgb):
    check_shape(nir, rgb) # make sure sizes are equal
    
    # create base zero arrays
    red = np.zeros((np.shape(rgb)[0], np.shape(rgb)[1], 3))
    ndvi = np.zeros((np.shape(rgb)[0], np.shape(rgb)[1], 3))
    
    red[:,:,0] = rgb[:,:,1] # extract red
    # nir is a x by y grid of NIR reflected values. rgb[:,:,0] is a x by y grid of red reflected values.
    ndvi[:, :,1] = (nir - red[:, :, 0]) / (red[:, :, 0] + nir) # run calculation and set to green channel
    
    ndvi_norm = normalize_255(ndvi, rgb) # norm values to make changes easier to see
    
    return ndvi_norm, ndvi
    

# dir_path = "C:/Users/iaad5777/Documents/git/EarthLab/nirscene1/country/" # uncomment this and change it to exact path if os.path.<etc> doesn't work
dir_path = os.path.dirname(os.path.abspath(__file__)) + "/nirscene1/forest/"
ext_nir = "_nir.tiff"
ext_rgb = "_rgb.tiff"

write_path = dir_path # provides options
out_ext = ".tiff" # tiff faster than jpg

verbose = False # Display every image vs only errors

print("beginning loop inside " + dir_path) if verbose else print("start")
for filename in os.listdir(dir_path): # for every file in dir_path (NOT IN ORDER)
    try:
        if filename.endswith(ext_nir): # if it ends with a certain ext (only want one bc two images being evald)
            # ternary operator stype. also, print("x", end="") prints without newline
            #print(filename + " being evaluated") if verbose else print(".", end='')
            print(filename + " being evaluated") if verbose else print(".", end = "")
            
            # import images (split splits after _, [0] takes first element [the actual filename])
            rgb = imageio.imread(dir_path + filename.split("_")[0] + ext_rgb)
            nir = imageio.imread(dir_path + filename.split("_")[0] + ext_nir)
                        
            # calculate indices
            ndvi_norm, ndvi = calc_ndvi(nir, rgb)
            evi_norm, evi = calc_evi(nir, rgb)
            
            # export images
            imageio.imwrite(write_path + filename.split("_")[0] + "_ndvi" + out_ext, ndvi_norm[:,:])
            imageio.imwrite(write_path + filename.split("_")[0] + "_evi" + out_ext, evi_norm[:,:])
        elif filename.endswith(ext_rgb): 
            pass # nec bc only want below when filename != _rgb.tiff || _nir.tiff
        else:
            print(filename + " is not a file I can use") if verbose else print("", end='') # to provide options
            
    except FileNotFoundError:
        print(filename + " does not exist")
        
    except:
        print("something went wrong, exiting")
        sys.exit(1)

print("done")
