# for creating ndvi images from the "Image and Visual Represtatino Lab" IVRL
# https://ivrl.epfl.ch/research-2/research-downloads/supplementary_material-cvpr11-index-html/
# for this to work on a personal computer, change the in_path variable to whatever it is on your machine

import numpy as np
import imageio


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


for x in range(100):
    x = x + 1
    
    try:
        prefix = str(x).zfill(4) # pad with zeros (makes 4 digit)
        in_path = "C:/Users/iaad5777/Documents/git/EarthLab/nirscene1/mountain/"
        out_path = in_path # to provide more options

        rgb = imageio.imread(in_path + prefix + "_rgb.tiff")
        nir = imageio.imread(in_path + prefix + "_nir.tiff")

        x_length = np.shape(rgb)[0]
        y_length = np.shape(rgb)[1]
    
        if np.shape(rgb)[0] != np.shape(nir)[0] or np.shape(rgb)[1] != np.shape(nir)[1]:
            print("Dimension Mismatch, exiting")
            exit()
    
        red = np.zeros((x_length, y_length, 3))
        ndvi = np.zeros((x_length, y_length, 3))
        
        red[:, :, 0] = rgb[:, :, 0]  # extract just red channel
        
        ndvi[:, :, 0] = (nir - red[:, :, 0]) / (red[:, :, 0] + nir)
        
        ndvi_norm = normalize_255(ndvi, rgb)

        imageio.imwrite(out_path + prefix + "_ndvi.jpg", ndvi_norm[:,:])
    
    except FileNotFoundError:
        print("file not found" + str(x))

print("done")