import os
import numpy as np
import matplotlib.pyplot as plt

def hips2img(file, order=[0,1,2], stretch=True, image_show=True, 
             image_save=False):
    
    # grab header info
    header_length = open(file).read().find('\n.')
    header = open(file).read()[:header_length].split()
    bands = int(header[1])
    res_x = int(header[2])
    res_y = int(header[3])
    fmt = int(header[4])
    
    # extract image from hips
    hips = np.fromfile(file, np.float32)
    hips_length = len(hips)
    img = hips[hips_length - (bands * res_x * res_y):].reshape(bands, res_x, res_y)
    img = np.rot90(img.T, 3)
    
    #stretch
    for b in range(bands):
        arr_b = img[:, :, b]
        if stretch:
            arr_b = ((arr_b - np.percentile(arr_b, 2.5)) / np.percentile(arr_b, 97.5))
            arr_b[arr_b < 0] = 0
            arr_b[arr_b > 1] = 1
        img[:, :, b] = arr_b
            
    # plot image to screen
    if image_show:
        if len(order) == 1 or bands == 1:
            order = order[0]
            cmap = 'gray'
        else:
            cmap = 'spectral'
        plt.figure(figsize=(10, 10))
        plt.axis('off')
        cmap = plt.imshow(img[:, :, order], cmap=cmap, interpolation='none')
        plt.show()
    
    # save image
    if image_save:
        plt.imsave(os.path.splitext(file)[0] + '.png', img)