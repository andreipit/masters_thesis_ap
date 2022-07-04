import os
import numpy as np
from utils.custom_types import NDArray
from utils.arg.model import ArgsModel
from .simulation.engine import Engine
from typing import TextIO

class RobotModel():
    engine:Engine = None

    # constants
    #cam_intrinsics = np.asarray([[618.62, 0, 320], [0, 618.62, 240], [0, 0, 1]])

    cam_depth_scale: float = 1
    workspace_limits: list = [[ -0.724, -0.276 ], [ -0.224, 0.224 ], [ -0.0001, 0.4 ]] # 3 axis: xmax-xmin; ymax-ymin, zmax-zmin
    color_space = np.asarray([[78.0, 121.0, 167.0], # blue
                                        [89.0, 161.0, 79.0], # green
                                        [156, 117, 95], # brown
                                        [242, 142, 43], # orange
                                        [237.0, 201.0, 72.0], # yellow
                                        [186, 176, 172], # gray
                                        [255.0, 87.0, 89.0], # red
                                        [176, 122, 161], # purpl                                           
                                        [118, 183, 178], # cyan
                                        [255, 157, 167]])/255.0 #pink

    # created later at robot_objects.py:
    #test_obj_mesh_files: list = []
    #test_obj_mesh_colors: list = []
    #test_obj_positions: list = []
    #test_obj_orientations: list = []
    object_handles: list = [] # id's of all instantiated blocks in scene: [178, 179, 180, 181, 182, 183, 184, 185]

    def __init__(self):
        pass
