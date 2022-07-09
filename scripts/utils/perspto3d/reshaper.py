import time
import numpy as np
from matplotlib import pyplot as plt
import math
#from typing import Optional, Tuple, Union, TypeVar
from typing import Tuple

from utils.custom_types import NDArray
from scipy import ndimage
import torch

class Reshaper():
    def __init__(self):
        pass

    def add_3_depth_channels(self, d: NDArray["224, 224", float])-> NDArray["224, 224, 3", float]:
        d = np.array([d,d,d])
        d = np.swapaxes(d,0,2)
        d = np.swapaxes(d,0,1)
        assert(d.shape == (224, 224, 3))
        return d

    def remove_3_depth_channels(self, d: NDArray["224, 224, 3", float])-> NDArray["224, 224", float]:
        d = d[:, :, 0]
        assert(d.shape == (224, 224))
        return d

    def cwh_to_whc(self, some_tensor: NDArray["3, 640, 640", float])-> NDArray["640, 640, 3", float]:
        #a = torch.rand(3,56,67)
        #print(a.transpose(0,2).transpose(0,1).size())
        #=====>torch.Size([56, 67, 3])
        return some_tensor.transpose(0,2).transpose(0,1)


    def scale_224x224_to_640x480(
        self, 
        color_heightmap: NDArray["224, 224,3", float], 
        depth_heightmap: NDArray["224, 224", float]) -> Tuple[NDArray["448, 448,3", float], NDArray["448, 448", float]]:
        # Apply 2x scale to input heightmaps
        # The third dimension is rgb
        #print('----fwd0:224, 224,3  color_heightmap.shape', color_heightmap.shape) # (224, 224, 3)
        #print('----fwd0:224, 224  depth_heightmap.shape', depth_heightmap.shape) # (224, 224)
        color_heightmap_2x = ndimage.zoom(color_heightmap, zoom=[2,2,1], order=0)
        depth_heightmap_2x = ndimage.zoom(depth_heightmap, zoom=[2,2], order=0)
        assert(color_heightmap_2x.shape[0:2] == depth_heightmap_2x.shape[0:2])
        #print('----fwd1:448, 448,3 color_heightmap_2x.shape', color_heightmap_2x.shape) # (448, 448, 3)
        #print('----fwd1: 448, 448 depth_heightmap_2x.shape', depth_heightmap_2x.shape) # (448, 448)
        assert(color_heightmap_2x.shape == (448, 448,3))
        assert(depth_heightmap_2x.shape == (448, 448))
        return color_heightmap_2x, depth_heightmap_2x

    def add_padding_keep_shape(
        self, 
        color_heightmap_2x: NDArray["448, 448,3", float], 
        depth_heightmap_2x: NDArray["448, 448", float]) -> Tuple[NDArray["640, 640, 3", float], NDArray["640, 640", float]]:
        # Add extra padding (to handle rotations inside network)
        diag_length = float(color_heightmap_2x.shape[0]) * np.sqrt(2)
        diag_length = np.ceil(diag_length/32)*32
        padding_width = int((diag_length - color_heightmap_2x.shape[0])/2)
        color_heightmap_2x_r =  np.pad(color_heightmap_2x[:,:,0], padding_width, 'constant', constant_values=0)
        color_heightmap_2x_r.shape = (color_heightmap_2x_r.shape[0], color_heightmap_2x_r.shape[1], 1)
        color_heightmap_2x_g =  np.pad(color_heightmap_2x[:,:,1], padding_width, 'constant', constant_values=0)
        color_heightmap_2x_g.shape = (color_heightmap_2x_g.shape[0], color_heightmap_2x_g.shape[1], 1)
        color_heightmap_2x_b =  np.pad(color_heightmap_2x[:,:,2], padding_width, 'constant', constant_values=0)
        color_heightmap_2x_b.shape = (color_heightmap_2x_b.shape[0], color_heightmap_2x_b.shape[1], 1)
        color_heightmap_2x = np.concatenate((color_heightmap_2x_r, color_heightmap_2x_g, color_heightmap_2x_b), axis=2)
        depth_heightmap_2x =  np.pad(depth_heightmap_2x, padding_width, 'constant', constant_values=0)
        #print('----fwd 2:640, 640, 3 color_heightmap_2x.shape', color_heightmap_2x.shape) # (640, 640, 3)
        #print('----fwd 2:640, 640  depth_heightmap_2x.shape', depth_heightmap_2x.shape) # (640, 640)
        assert(color_heightmap_2x.shape == (640, 640, 3))
        assert(depth_heightmap_2x.shape == (640, 640))
        return color_heightmap_2x, depth_heightmap_2x

    def scale_and_normalize(
        self, 
        color_heightmap_2x: NDArray["640, 640,3", float], 
        depth_heightmap_2x: NDArray["640, 640", float]) -> Tuple[NDArray["640, 640, 3", float], NDArray["640, 640, 3", float]]:
        # Pre-process color image (scale and normalize)
        image_mean = [0.485, 0.456, 0.406]
        image_std = [0.229, 0.224, 0.225]
        input_color_image = color_heightmap_2x.astype(float)/255
        for c in range(3):
            input_color_image[:,:,c] = (input_color_image[:,:,c] - image_mean[c])/image_std[c]

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
        assert(input_color_image.shape == (640, 640, 3))
        assert(input_depth_image.shape == (640, 640, 3))

        return input_color_image, input_depth_image
        

    def reshape_to_minibatch_1_3_640_640(
        self, 
        input_color_image: NDArray["640, 640,3", float], 
        input_depth_image: NDArray["640, 640,3", float]) -> Tuple[NDArray["1, 3, 640, 640", float], NDArray["1, 3, 640, 640", float]]:
        # Construct minibatch of size 1 (b,c,h,w)
        input_color_image.shape = (input_color_image.shape[0], input_color_image.shape[1], input_color_image.shape[2], 1)
        input_depth_image.shape = (input_depth_image.shape[0], input_depth_image.shape[1], input_depth_image.shape[2], 1)
        input_color_data = torch.from_numpy(input_color_image.astype(np.float32)).permute(3,2,0,1)
        input_depth_data = torch.from_numpy(input_depth_image.astype(np.float32)).permute(3,2,0,1)
        #print('----fwd 5: 1, 3, 640, 640 input_color_data.shape', input_color_data.shape, '[0][0]==]', input_color_data[0][0]) #  [1, 3, 640, 640]
        #print('----fwd 5: 1, 3, 640, 640 input_color_data[0][0][0]', input_color_data[0][0][0]) # [2, ...,-2]
        #print('----fwd 5: 1, 3, 640, 640 input_depth_image.shape', input_depth_image.shape, '[0][0]==]', input_depth_image[0][0]) #  [1, 3, 640, 640]
        #print('----fwd 5: 1, 3, 640, 640 input_depth_image[0][0][0]', input_depth_image[0][0][0]) # [0.31 ... 0.31]
        assert(input_color_data.shape == ( 1, 3, 640, 640))
        assert(input_color_data.shape == ( 1, 3, 640, 640))
        return input_color_data, input_depth_data