# for creating ndvi images from the "Image and Visual Represtatino Lab" IVRL
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# for this to work on a personal computer, change the in_path variable to whatever it is on your machine

import numpy as np
import imageio
import os


def normalize_255(im1, im_color):
    # input: im1 f64 numpy array with some sort of vegetation index info
    # input: im_color numpy array holding original rgb values of the xVI image
    # purpose: take an xVI image and make it human readable and jpg exportable
    im_norm = (im1 / np.max(im1)) * 255  # gives greatest contrast w/out losing data
    im_norm[im_norm < 0] = 0  # removes negative values (water, soil)
    im_norm = np.uint8(im_norm)  # round off and make uint8 (imageio likes it)

    im_norm[:, :, 0] = im_color[:, :, 0]  # add visual red
    # im_norm[:, :, 2] = im_color[:, :, 2]  # add visual blue (uness but looks better)

    return im_norm


def check_shape(nir, rgb):
    if np.shape(rgb)[0] != np.shape(nir)[0] or np.shape(rgb)[1] != np.shape(nir)[1]:
        print("Dimension Mismatch, exiting")
        exit()

def calc_evi(nir, rgb):
    # L, C1, C2, G = 1, 6, 7.5, 2.5
    pass
    

def calc_ndvi(nir, rgb):
    check_shape(nir, rgb)
    
    red = np.zeros((np.shape(rgb)[0], np.shape(rgb)[1], 3))
    ndvi = np.zeros((np.shape(rgb)[0], np.shape(rgb)[1], 3))
    
    red[:,:,0] = rgb[:,:,1]
    ndvi[:, :,1] = (nir - red[:, :, 0]) / (red[:, :, 0] + nir)
    
    ndvi_norm = normalize_255(ndvi, rgb)
    
    return ndvi_norm
    

dir_path = "C:/Users/iaad5777/Documents/git/EarthLab/nirscene1/country/"
write_path = dir_path # provides options
files = os.listdir(dir_path)
ext_nir = "_nir.tiff"
ext_rgb = "_rgb.tiff"
ext_output = ".tiff" # tiff faster than jpg

verbose = True

for filename in os.listdir(dir_path): # for every file in dir_path
    try:
        if filename.endswith(ext_nir): # if it ends with a certain ext (only want one bc two images being evald)
            if verbose: print(filename + " being evaluated")
            
            # import images (split splits after _, [0] takes first element [the actual filename])
            rgb = imageio.imread(dir_path + filename.split("_")[0] + ext_rgb)
            nir = imageio.imread(dir_path + filename.split("_")[0] + ext_nir)
            
            # calculate indices
            ndvi_norm = calc_ndvi(nir, rgb)
            
            # export images
            imageio.imwrite(dir_path + filename.split("_")[0] + "_ndvi.tiff", ndvi_norm[:,:])
        else:
            if verbose: print(filename + " is being skipped")
            
    except FileNotFoundError:
        print(filename + " does not exist")
        
    except:
        print("something went wrong, exiting")
        exit()

print("done")