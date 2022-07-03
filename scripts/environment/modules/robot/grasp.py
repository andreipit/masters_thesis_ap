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
    
    def grasp(self, pos_new, rot_new, limits, engine: Engine):
        self.rotate(rot_new, engine)
        self.move(pos_new, limits, engine)

    def rotate(self,  angle_new: float, engine: Engine):
        """ angle_new is in degrees between -90 and 90 """
        angle_new = self._convert_rot(angle_new)
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id) # radians!!!
        delay = int(abs(rot_old[1] - angle_new) * 10) # or 20; more difference -> more time we need
        for i in range(1, delay + 1):
            angle_next = self.lerp_f(rot_old[1], angle_new, i / delay)
            engine.global_rotation_set(_ObjID = dummy_id, _NewRot3D = (np.pi / 2, angle_next, np.pi / 2))
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id) # radians!!!

    def move(self, pos_new, limits, engine: Engine):
        pos_new = self._convert_pos(pos_new, limits)
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, pos_old = engine.global_position_get(_ObjID = dummy_id) #print('pos_old', pos_old, ' \n pos_new', pos_new)
        delay = int(np.linalg.norm(np.asarray(pos_old) - np.asarray(pos_new)) * 50)
        for i in range(1, delay + 1):
            pos_next = self.lerp_vec(pos_old, pos_new, i / delay) #print('pos_next', pos_next)
            engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_next)

    def _convert_pos(self, pos, limits):
        res = np.asarray(pos).copy()
        res[2] = max(res[2] - 0.04, limits[2][0] + 0.02) # higher table or -= 0.04
        res = (res[0], res[1], res[2] +  0.15) # just += 0.15
        return res

    def _convert_rot(self, angle: float):
        if angle < -90: angle = -90
        if angle > 90: angle = 90
        angle = angle * np.pi / 180 # convert to radians
        return angle

    def lerp_f(self, start:float, stop:float, i:float) -> list:
        """ 20 30 0.3 => 20 + (30-20)*0.3 = 23 
            30 20 0.3 => 30 + (20-30)*0.3 = 30-3 
        """
        return start + (stop - start) * i

    def lerp_vec(self, start:list, stop:list, i:float) -> list:
        x = start[0] + (stop[0] - start[0]) * i
        y = start[1] + (stop[1] - start[1]) * i
        z = start[2] + (stop[2] - start[2]) * i
        return [x, y, z]
