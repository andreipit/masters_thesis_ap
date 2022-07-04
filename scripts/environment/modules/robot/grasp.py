import time
import numpy as np

import utils.utils as utils
from utils.arg.model import ArgsModel
from .model import RobotModel
from .camera import RobotCamera
from .sim import RobotSim
from .gripper import RobotGripper
from .move import RobotMove
from .objects import RobotObjects
from .simulation.engine import Engine
from utils.custom_types import NDArray

class RobotGrasp():

    def __init__(self):
        pass
    
    def grasp(self, pos_new: NDArray["3,1", float], degrees_new: float, limits: list, engine: Engine,  gripper: RobotGripper, mover: RobotMove) -> bool:
        gripper.open_gripper(engine)
        mover.rotate(degrees_new, engine)
        mover.move(pos_new, limits, engine)
        #_, pos_old = engine.global_position_get(_ObjName = 'UR5_target') #print('pos_old', pos_old, ' \n pos_new', pos_new)
        pos_new[2] -= 0.15
        mover.move(pos_new, limits, engine)
        gripper_full_closed = gripper.close_gripper(engine)
        pos_new[2] += 0.15*2 #0.15
        mover.move(pos_new, limits, engine)
        grasp_success = not gripper_full_closed
        return grasp_success
