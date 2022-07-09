#!/usr/bin/env python
from collections import OrderedDict
import numpy as np
from scipy import ndimage
import torch
import torch.nn as nn
import torch.nn.functional as F
from torch.autograd import Variable
import torchvision
import matplotlib.pyplot as plt
import time

"""
summary:
create 2 conv nets: pushnet & graspnet
use pretrained torchvision.densenet121 as feature_extractor

"""


class push_grasp_net_min(nn.Module):

    def __init__(self, use_cuda = True): # , snapshot=None
        pass

    def forward(self, input_color_data, input_depth_data, is_volatile=False, specific_rotation=-1):
        pass