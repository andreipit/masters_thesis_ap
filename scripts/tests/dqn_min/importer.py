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

from tests.dqn_min.utils import utils
from tests.dqn_min.network import create_net
from tests.dqn_min.forward import get_action
from tests.dqn_min.loss import td_loss
from tests.dqn_min.loss_double_dqn import td_loss_double_dqn
from tests.dqn_min.plot import plot_loss
from tests.dqn_min.log import Logger
from tests.dqn_min.factory import create_objects, create_objects_legacy

