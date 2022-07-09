import time
import numpy as np
from matplotlib import pyplot as plt
import math
#from typing import Optional, Tuple, Union, TypeVar
from typing import Tuple

from utils.custom_types import NDArray
from scipy import ndimage
import torch

class ReshaperDepth():
    def __init__(self):
        pass

    def scale_224x224_to_640x480(
        self, 
        depth_heightmap: NDArray["224, 224", float]) -> NDArray["448, 448", float]:
        # Apply 2x scale to input heightmaps
        # The third dimension is rgb
        #print('----fwd0:224, 224,3  color_heightmap.shape', color_heightmap.shape) # (224, 224, 3)
        #print('----fwd0:224, 224  depth_heightmap.shape', depth_heightmap.shape) # (224, 224)
        depth_heightmap_2x = ndimage.zoom(depth_heightmap, zoom=[2,2], order=0)
        #print('----fwd1:448, 448,3 color_heightmap_2x.shape', color_heightmap_2x.shape) # (448, 448, 3)
        #print('----fwd1: 448, 448 depth_heightmap_2x.shape', depth_heightmap_2x.shape) # (448, 448)
        assert(depth_heightmap_2x.shape == (448, 448))
        return depth_heightmap_2x

    def add_padding_keep_shape(
        self, 
        depth_heightmap_2x: NDArray["448, 448", float]) -> NDArray["640, 640", float]:
        # Add extra padding (to handle rotations inside network)
        diag_length = float(depth_heightmap_2x.shape[0]) * np.sqrt(2)
        diag_length = np.ceil(diag_length/32)*32
        padding_width = int((diag_length - depth_heightmap_2x.shape[0])/2)
        depth_heightmap_2x =  np.pad(depth_heightmap_2x, padding_width, 'constant', constant_values=0)
        #print('----fwd 2:640, 640, 3 color_heightmap_2x.shape', color_heightmap_2x.shape) # (640, 640, 3)
        #print('----fwd 2:640, 640  depth_heightmap_2x.shape', depth_heightmap_2x.shape) # (640, 640)
        assert(depth_heightmap_2x.shape == (640, 640))
        return depth_heightmap_2x

    def scale_and_normalize(
        self, 
        depth_heightmap_2x: NDArray["640, 640", float]) -> NDArray["640, 640, 3", float]:
        
        # Pre-process depth image (normalize)
        # change me
        image_mean = [0.01, 0.01, 0.01]
        image_std = [0.03, 0.03, 0.03]
        depth_heightmap_2x.shape = (depth_heightmap_2x.shape[0], depth_heightmap_2x.shape[1], 1)
        input_depth_image = np.concatenate((depth_heightmap_2x, depth_heightmap_2x, depth_heightmap_2x), axis=2)
        for c in range(3):
            input_depth_image[:,:,c] = (input_depth_image[:,:,c] - image_mean[c])/image_std[c]
        #print('----fwd 4: 640, 640,3 input_color_image.shape', input_color_image.shape, '[0]==', input_color_image[0]) # (640, 640, 3) [0]== [[-2.11790393 -2.03571429 -1.80444444]
        #print('----fwd 4: 640, 640,3 input_depth_image.shape', input_depth_image.shape, '[0==]', input_depth_image[0]) #  (640, 640, 3) [0==] [[-0.33333333 -0.33333333 -0.33333333]
        assert(input_depth_image.shape == (640, 640, 3))

        return input_depth_image
        

    def reshape_to_minibatch_1_3_640_640(
        self, 
        input_depth_image: NDArray["640, 640,3", float]) -> NDArray["1, 3, 640, 640", float]:
        # Construct minibatch of size 1 (b,c,h,w)
        input_depth_image.shape = (input_depth_image.shape[0], input_depth_image.shape[1], input_depth_image.shape[2], 1)
        input_depth_data = torch.from_numpy(input_depth_image.astype(np.float32)).permute(3,2,0,1)
        #print('----fwd 5: 1, 3, 640, 640 input_color_data.shape', input_color_data.shape, '[0][0]==]', input_color_data[0][0]) #  [1, 3, 640, 640]
        #print('----fwd 5: 1, 3, 640, 640 input_color_data[0][0][0]', input_color_data[0][0][0]) # [2, ...,-2]
        #print('----fwd 5: 1, 3, 640, 640 input_depth_image.shape', input_depth_image.shape, '[0][0]==]', input_depth_image[0][0]) #  [1, 3, 640, 640]
        #print('----fwd 5: 1, 3, 640, 640 input_depth_image[0][0][0]', input_depth_image[0][0][0]) # [0.31 ... 0.31]
        assert(input_depth_data.shape == ( 1, 3, 640, 640))
        return input_depth_data