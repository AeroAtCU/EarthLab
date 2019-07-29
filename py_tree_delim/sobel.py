# given input image path, create a new image (and return the image)
# with the edges

import numpy as np
import imageio
import os
import PIL as pil
import sys

def make_gray(input_im):
    # make int8 so averaging does not overflow
    input_im = np.float64(input_im)
    
    # get dimensions
    xleng = np.shape(input_im)[0]
    yleng = np.shape(input_im)[1]
    
    # creat output 1d array, populated w 0
    out_im = np.zeros((xleng, yleng, 1))
    
    # make black and white using averages
    out_im[:,:,0] = (input_im[:,:,0] + input_im[:,:,1] + input_im[:,:,2]) / 3
    
    # make uint8
    out_im = np.uint8(out_im)
    
    return out_im

input_im_name = "ex.png"
input_im_path = os.path.join("home","ian","Pictures",input_im_name)
this_path = sys.path[0]

input_im = imageio.imread(input_im_name)

# check if image is a 3d RGB, if not exit
if (np.shape(input_im)[2] != 3):
    print("input image is not 3 dimensional (RGB), exiting")
    exit(0)

gray = make_gray(input_im)
print(gray)

imageio.imwrite('out.png', gray)

print("done")

# does not work with 4 layer pngs
#try:
#    input_im = imageio.imread(input_im_path)
#except FileNotFoundError:
#    print("file not found error:" + input_im_path)
#    print("defaulting to ex.png in script's folder")
#    input_im = imageio.imread('ex.png')
#except:
#    print("something went wrong")
#    exit(0)
