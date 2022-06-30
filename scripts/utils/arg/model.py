import os
import numpy as np
import argparse

from utils.custom_types import NDArray


class ArgsModel():

    stage: str = '' # grasp_only
    goal_obj_idx: int = 0 # 4
    _workspace_limits: NDArray["3,2", float] = NDArray(shape=(3,2), dtype=float)# [[-7.24e-01 -2.76e-01] [-2.24e-01  2.24e-01] [-1.00e-04  4.00e-01]] = np.zeros((3, 3), dtype=np.complex64)
    workspace_limits = property(_workspace_limits.getx, _workspace_limits.setx, _workspace_limits.delx, "_workspace_limits")


    def __init__(self):
        pass
