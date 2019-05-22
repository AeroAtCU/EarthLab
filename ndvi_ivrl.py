# for creating ndvi images from the "Image and Visual Represtatino Lab" IVRL dataset. Download:
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# Ian Adler
# 2019

import numpy as np
import imageio
import os
import sys


def normalize_vegidx(vegidx_im, rgb):
    # input: vegidx_im f64 numpy array containing vegetation index info
    # input: rgb numpy array holding original color values of the image
    # purpose: take vegitation index calculated data and make it human readable and exportable

    # remove outliers (vegidx should always go between -1:1)
    vegidx_im[vegidx_im > 5] = 0
    vegidx_im[vegidx_im > 1] = 1
    vegidx_im[vegidx_im < 0] = 0

    # normalize the values to work best with images
    vegidx_im *= 255 / np.max(vegidx_im) # equivalent to vegidx_im = 255 * (vegidx_im / np.max(vegidx_im)), but probably faster
    vegidx_im = np.uint8(vegidx_im)  # make uint8 (round and change datatype. imageio prefers uint8)

    # add visual bands
    vegidx_im[:, :, 0] = rgb[:, :, 0] # rgb[x,y,z] {z=(0,1,2) -> (r,g,b)}

    return vegidx_im


def check_shape(nir, rgb):
    # input: nir x*y numpy array
    # input: rgb x*y*3 numpy array
    # purpose: check if x and y dims are the same, exit if not (should always be the same)
    if np.shape(rgb)[0] != np.shape(nir)[0] or np.shape(rgb)[1] != np.shape(nir)[1]:
        print("Dimension mismatch, exiting.")
        sys.exit(1)


def calc_evi(nir, rgb):
    # input: nir x*y numpy array representing a picture
    # input: rgb x*y*3 numpy array representing a picture
    # purpose: calculate the enhanced vegitation index

    check_shape(nir, rgb) # make sure sizes are equal
    xleng = np.shape(rgb)[0]
    yleng = np.shape(rgb)[1]
    
    L, C1, C2, G = 1, 6, 7.5, 2.5 # define constants for evi equation
    
    # create base zero arrays
    red = np.zeros((xleng, yleng, 3))
    blue = np.zeros((xleng, yleng, 3))
    evi = np.zeros((xleng, yleng, 3))
    numer = np.zeros((xleng, yleng, 3))
    denom = np.zeros((xleng, yleng, 3))
    
    # doesn't like it when using rgb, so extract one color per channel needed
    red[:,:,0] = rgb[:,:,0]
    blue[:,:,2] = rgb[:,:,2]
    
    # run calculation. np.divide() prevents divion by zero (sets any/0 to 0). set result to green channel.
    numer = nir - red[:,:,0]
    denom = (nir + C1*red[:,:,0] - C2*blue[:,:,2] + L)
    evi[:,:,1] = G * (np.divide(numer, denom, out=np.zeros_like(numer), where=denom!=0))
    
    # normalize values for picture
    evi_norm = normalize_vegidx(evi, rgb)
    
    return evi_norm, evi


def calc_ndvi(nir, rgb):
    # input: nir x*y numpy array representing a picture
    # input: rgb x*y*3 numpy array representing a picture
    # purpose: calculate the normalized difference vegitation index
    # notes: nir is a grid of NIR reflected values. rgb[:,:,0] is a grid of red reflected values.
    
    check_shape(nir, rgb) # make sure sizes are equal
    xleng = np.shape(rgb)[0]
    yleng = np.shape(rgb)[1]
    
    # create base zero arrays
    red = np.zeros((xleng, yleng, 3))
    ndvi = np.zeros((xleng, yleng, 3))
    
    # doesn't like it when using rgb, so extract one color per channel needed
    red[:,:,0] = rgb[:,:,1]
    ndvi[:, :,1] = (nir - red[:, :, 0]) / (red[:, :, 0] + nir) # set result to green channel
    
    # normalize values for picture
    ndvi_norm = normalize_vegidx(ndvi, rgb)
    
    return ndvi_norm, ndvi
    

# define inputs path and type (currently only tested on .tiffs from above dataset)
script_path = os.path.dirname(os.path.abspath(__file__)) # get current (script) directory
ivrl_folder = os.path.join("nirscene1", "country") # join with the dataset
read_path = os.path.join(script_path, ivrl_folder, "")
ext_nir = "_nir.tiff"
ext_rgb = "_rgb.tiff"
write_path = read_path # provides options
out_ext = ".tiff" # exporting to tiff is faster than jpg

verbose = True # describe each file or just symbols

print("beginning loop inside " + read_path) if verbose else print("start")

for filename in os.listdir(read_path): # for every file in read_path (NOT IN ORDER)
    try:
        if filename.endswith(ext_nir): # if it ends with a certain ext (only want one bc two images being evald)
            # "ternary operator" style. end = "" specifies the end char to nothing (default~ \n)
            print(filename + " being evaluated") if verbose else print(".", end="")
            
            # import images (split splits after _, [0] takes first element [the actual filename])
            rgb = imageio.imread(read_path + filename.split("_")[0] + ext_rgb)
            nir = imageio.imread(read_path + filename.split("_")[0] + ext_nir)
                        
            # calculate indices
            ndvi_norm, nop = calc_ndvi(nir, rgb)
            evi_norm, nop = calc_evi(nir, rgb)
            
            # export images
            imageio.imwrite(write_path + filename.split("_")[0] + "_ndvi" + out_ext, ndvi_norm[:,:])
            imageio.imwrite(write_path + filename.split("_")[0] + "_evi" + out_ext, evi_norm[:,:])
        elif filename.endswith(ext_rgb) or filename.endswith("vi.tiff"): # not the best way to do this
            pass # necessary bc of the file and loop structure
        else:
            print(filename + " is not a file I can use") if verbose else print("x", end="")
            
    except FileNotFoundError:
        print(filename + " does not exist") if verbose else print("?", end="")
        
    except:
        print("something went wrong, exiting")
        sys.exit(1)

print('\n' + "done")