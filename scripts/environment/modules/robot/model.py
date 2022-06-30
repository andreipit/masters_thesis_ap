import os
import numpy as np
from utils.custom_types import NDArray
from utils.arg.model import ArgsModel
from .simulation.simulator import Simulator
from typing import TextIO

class RobotModel():

    cam_intrinsics = np.asarray([[618.62, 0, 320], [0, 618.62, 240], [0, 0, 1]])
    cam_depth_scale = 1

    # created later at robot_objects.py:
    test_obj_mesh_files: list = []
    test_obj_mesh_colors: list = []
    test_obj_positions: list = []
    test_obj_orientations: list = []
    object_handles: list = []

    def __init__(self):
        pass
