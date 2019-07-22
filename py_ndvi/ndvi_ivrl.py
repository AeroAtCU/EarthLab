# for creating ndvi images from the "Image and Visual Represtatino Lab" IVRL dataset. Download:
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# Ian Adler
# 2019

import numpy as np
import imageio
import os
import sys


def normalize_vegidx(vegidx_im, rgb):
    # purpose: take vegitation index calculated data and make it human readable and exportable
    # input: vegidx_im x*y f64 numpy array containing vegetation index info
    # input: rgb x*y*3 numpy array holding original color values of the image

    # remove outliers (vegidx should always go between -1:1)
    output_im = vegidx_im
    output_im[output_im > 5] = 0
    output_im[output_im > 1] = 1
    output_im[output_im < 0] = 0

    # normalize the values to work best with images
    output_im *= 255 / np.max(output_im) # equivalent to output_im = 255 * (output_im / np.max(output_im)), but probably faster
    output_im = np.uint8(output_im)  # make uint8 (round and change datatype. imageio prefers uint8)

    # add visual bands
    output_im[:, :, 0] = rgb[:, :, 0] # rgb[x,y,z] {z=(0,1,2) -> (r,g,b)}

    return output_im


def check_shape(nir, rgb):
    # purpose: check if x and y dims are the same, exit if not (should return bool, but should also always be the same)
    # input: nir x*y numpy array
    # input: rgb x*y*3 numpy array
    
    if np.shape(rgb)[0] != np.shape(nir)[0] or np.shape(rgb)[1] != np.shape(nir)[1]:
        print("Dimension mismatch, exiting.")
        sys.exit(1)
    

def calc_evi(nir, rgb):
    # purpose: calculate the enhanced vegitation index
    # input: nir x*y numpy array representing a picture
    # input: rgb x*y*3 numpy array representing a picture

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
    # purpose: calculate the normalized difference vegitation index from an rgb and nir image
    # input: nir x*y numpy array representing a picture
    # input: rgb x*y*3 numpy array representing a picture
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
ivrl_folder = os.path.join("nirscene1", "country") # dataset folder (nirscene1) and subfolder (country, forest, etc) with actual images
script_path = os.path.dirname(os.path.abspath(__file__)) # get current (script's) directory
# full path to folder. last "" adds correct slash or backslash. works anyway with / and \, but safer
read_path = os.path.join(os.path.dirname(script_path), ivrl_folder, "") # needed second os.path.dirname to go to second parent.

ext_nir = "_nir.tiff"
ext_rgb = "_rgb.tiff"
write_path = read_path # provides options
out_ext = ".tiff" # exporting to tiff is faster than jpg

verbose = False # describe each file or just symbols

print("beginning loop inside " + read_path) if verbose else print("start")

for filename in os.listdir(read_path): # for every file in read_path (NOT IN ORDER)
    try:
        if filename.endswith(ext_nir): # only want one bc two images being evald
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
