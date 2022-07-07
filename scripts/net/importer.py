# pip install --upgrade pip
# python -m pip install psutil
# python -m pip install pygame
# python -m pip install tqdm
# python -m pip install ipython
# python -m pip install pandas
import gym
import os
import time
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline
import torch
import torch.nn as nn
import torch.nn.functional as F
#device = torch.device('cuda' if torch.cuda.is_available() else 'cpu')
device = torch.device('cuda')

from net.model import create_network_4_to_2, create_network_224x224_to_224x224
from net.factory import create_env
from net.forward import get_action
from net.loss_ddqn import td_loss_double_dqn
from net import utils
from net.plot import plot

