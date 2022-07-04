import time
import numpy as np

import utils.utils as utils
from utils.arg.model import ArgsModel
from .model import RobotModel
from .sim import RobotSim
from .simulation.engine import Engine
from utils.custom_types import NDArray

class RobotMove():

    def __init__(self):
        pass

    def rotate(self,  degrees_new: float, engine: Engine):
        """ angle_new is in degrees between -90 and 90 """
        radians_new = self._convert_rot(degrees_new) # trim and to radians
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id) # radians!!!
        delay = int(abs(rot_old[1] - radians_new) * 10) # or 20; more difference -> more time we need
        for i in range(1, delay + 1):
            angle_next = self._lerp_f(rot_old[1], radians_new, i / delay)
            engine.global_rotation_set(_ObjID = dummy_id, _NewRot3D = (np.pi / 2, angle_next, np.pi / 2))
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id) # radians!!!

    def move(self, pos_new: NDArray["3", float], limits: list, engine: Engine):
        #pos_new = self._convert_pos(pos_new, limits)
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, pos_old = engine.global_position_get(_ObjID = dummy_id) #print('pos_old', pos_old, ' \n pos_new', pos_new)
        delay = int(np.linalg.norm(np.asarray(pos_old) - np.asarray(pos_new)) * 50)
        for i in range(1, delay + 1):
            pos_next = self._lerp_vec(pos_old, pos_new, i / delay) #print('pos_next', pos_next)
            engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_next)

            
    def _lerp_f(self, start:float, stop:float, i:float) -> list:
        """ 20 30 0.3 => 20 + (30-20)*0.3 = 23 
            30 20 0.3 => 30 + (20-30)*0.3 = 30-3 
        """
        return start + (stop - start) * i

    def _lerp_vec(self, start:list, stop:list, i:float) -> list:
        x = start[0] + (stop[0] - start[0]) * i
        y = start[1] + (stop[1] - start[1]) * i
        z = start[2] + (stop[2] - start[2]) * i
        return [x, y, z]

    def _convert_pos(self, pos: NDArray["3,1", float], limits: list) -> NDArray["3,1", float]:
        res = np.asarray(pos).copy()
        res[2] = max(res[2] - 0.04, limits[2][0] + 0.02) # higher table or -= 0.04
        res = (res[0], res[1], res[2] +  0.15) # just += 0.15
        return res

    def _convert_rot(self, angle: float):
        if angle < -90: angle = -90
        if angle > 90: angle = 90
        angle = angle * np.pi / 180 # convert to radians
        return angle


    #def move_to(self, sim: RobotSim, m: RobotModel, tool_position, tool_orientation):

    #     #sim_ret, UR5_target_handle = vrep.simxGetObjectHandle(self.sim_client,'UR5_target',vrep.simx_opmode_blocking)
    #    #sim_ret, UR5_target_position = vrep.simxGetObjectPosition(self.sim_client, self.UR5_target_handle,-1,vrep.simx_opmode_blocking)
    #    sim_ret, UR5_target_handle = m.engine.gameobject_find(_Name = 'UR5_target')
    #    sim_ret, UR5_target_position = m.engine.global_position_get(_ObjID = UR5_target_handle)

    #    move_direction = np.asarray([tool_position[0] - UR5_target_position[0], tool_position[1] - UR5_target_position[1], tool_position[2] - UR5_target_position[2]])
    #    move_magnitude = np.linalg.norm(move_direction)
    #    move_step = 0.02*move_direction/move_magnitude
    #    num_move_steps = int(np.floor(move_magnitude/0.02))

    #    for step_iter in range(num_move_steps):
    #        m.engine.global_position_set(_ObjID = UR5_target_handle, _NewPos3D = (UR5_target_position[0] + move_step[0], UR5_target_position[1] + move_step[1], UR5_target_position[2] + move_step[2]))
    #        #vrep.simxSetObjectPosition(self.sim_client,self.UR5_target_handle,-1,(UR5_target_position[0] + move_step[0], UR5_target_position[1] + move_step[1], UR5_target_position[2] + move_step[2]),vrep.simx_opmode_blocking)
    #        #sim_ret, UR5_target_position = vrep.simxGetObjectPosition(self.sim_client,self.UR5_target_handle,-1,vrep.simx_opmode_blocking)
    #        sim_ret, UR5_target_position = m.engine.global_position_get(_ObjID = UR5_target_handle)
        
    #    #vrep.simxSetObjectPosition(self.sim_client,self.UR5_target_handle,-1,(tool_position[0],tool_position[1],tool_position[2]),vrep.simx_opmode_blocking)
    #    m.engine.global_position_set(_ObjID = UR5_target_handle, _NewPos3D = (tool_position[0],tool_position[1],tool_position[2]))

