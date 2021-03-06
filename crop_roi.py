# -*- coding: utf-8 -*-
"""crop-roi.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1ONpUDYHMgBkA3pRA8cwIFCeQ1t0KiGHZ
"""

import numpy as np
import matplotlib.pyplot as plt
from glob import glob
from skimage.io import imread
from skimage.color import rgb2gray
from skimage.filters import threshold_otsu
from skimage.morphology import convex_hull_image
from skimage.measure import label, regionprops

def plot_image(img):
    
    plt.figure(figsize = (10, 10))
    plt.imshow(img, cmap=plt.cm.gray)

    
def binarize_image(image_array):
    return image_array > threshold_otsu(image_array)

"""# Prova de conceito"""

all_images = glob('images/*.png')

image = imread(all_images[5])

image_gray = rgb2gray(image)

image_bin = binarize_image(image_gray)

image_mask = np.invert(convex_hull_image(image_bin == 0))

plot_image(image)

plot_image(image_bin)

plot_image(image_mask)

label_img = label(image_mask == 0)

region, *_ = regionprops(label_img)

minr, minc, maxr, maxc = region.bbox
    
bx = (minc, maxc, maxc, minc, minc)
by = (minr, minr, maxr, maxr, minr)

plot_image(image_gray)
plt.plot(bx, by, '-r', linewidth=2.5)
plt.show()

"""# Aplicando"""

def crop_image_roi(image):
    
    # Padding dos limites de borda
    safe_zone_pixel = 5
    
    # Gerando Mask
    image_gray = rgb2gray(image)

    image_bin = binarize_image(image_gray)

    image_mask = np.invert(convex_hull_image(image_bin == 0))

    # Contornando limites
    label_img = label(image_mask == 0)

    region, *_ = regionprops(label_img)
    
    minr, minc, maxr, maxc = region.bbox

    # Cortando o ROI
    return image_gray[minr - safe_zone_pixel:
                      maxr + safe_zone_pixel,
                      minc - safe_zone_pixel: 
                      maxc + safe_zone_pixel]

def rotate_image(image):
    pass

image = imread(all_images[0])
result = crop_image_roi(image)

plot_image(result)

