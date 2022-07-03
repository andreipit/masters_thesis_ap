
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
        """
        Grasp is just moving and rotating dummy "UR5_target"
        Gives strange result. Sometimes rotates, sometimes not.
        """
        #_, dummy_id = engine.gameobject_find('UR5_target')
        #engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_new)
        #return 

        _, dummy_id = engine.gameobject_find('UR5_target')
        _, pos_old = engine.global_position_get(_ObjID = dummy_id)
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id)

        print('rot_old', rot_old)
        rot_new = rot_new * np.pi / 180 # convert to radians

        pos_new = self._convert_pos(pos_new, limits)
        rot_new = self._convert_rot(rot_new)
        print('rot_new', rot_new)

        # where and how many times
        pos_step_vec, pos_steps_count = self._get_pos_step(pos_old, pos_new)
        rot_step_vec, rot_steps_count = self._get_rot_step(rot_old, rot_new)
        print('rot_step_vec', rot_step_vec)
        print('rot_steps_count', rot_steps_count)

        for i in range(max(pos_steps_count, rot_steps_count)):
            pos_next = self._get_next_pos(pos_old, pos_step_vec, i, pos_steps_count)
            rot_next = self._get_next_rot(rot_old, rot_step_vec, i, rot_steps_count)
            
            engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_next)
            engine.global_rotation_set(_ObjID = dummy_id, _NewRot3D = rot_next)

    def _convert_pos(self, pos, limits):
        res = np.asarray(pos).copy()
        res[2] = max(res[2] - 0.04, limits[2][0] + 0.02) # higher table or -= 0.04
        res = (res[0], res[1], res[2] +  0.15) # just += 0.15
        return res

    def _convert_rot(self, rot):
        #22.5 ==> -1.05:  16 images, step=22.5 degrees, 10%4=2, 22.5%3.14=0.52; 0.52 - 3.14/2 =-1.05
        # convert to radians and set start to pi/2 degrees
        # Compute tool orientation from heightmap rotation angle
        res = (rot % np.pi) - np.pi / 2 #  -1.0619449019234484
        return res

    def _get_pos_step(self, pos_old, pos_new):
        if pos_old == pos_new:
            return np.asarray([.0, .0, .0]), 0
        move_direction = np.asarray([pos_new[0] - pos_old[0], pos_new[1] - pos_old[1], pos_new[2] - pos_old[2]])
        move_magnitude = np.linalg.norm(move_direction)
        move_step = 0.05 * move_direction / move_magnitude # Vector3 step = 5% of vector len in each axis
        num_move_steps = int(np.floor(move_direction[0] / move_step[0]))
        return move_step, num_move_steps

    def _get_rot_step(self, rot_old, rot_new, speed = 0.3):
        step = speed if (rot_new - rot_old[1] > 0) else -speed
        if step == 0:
            return 0, 0
        num_steps = int(np.floor((rot_new - rot_old[1]) / step))
        return step, num_steps
  
    def _get_next_pos(self, pos_old, pos_step_vec, i, pos_steps_count):
        """ If i is bigger then steps_count, we don't move.
            This can happen if we have more rot steps then move steps.
        """
        x = pos_old[0] + pos_step_vec[0] * min(i, pos_steps_count)
        y = pos_old[1] + pos_step_vec[1] * min(i, pos_steps_count) 
        z = pos_old[2] + pos_step_vec[2] * min(i, pos_steps_count)
        return (x, y, z)

    def _get_next_rot(self, rot_old, rot_step_vec, i, rot_steps_count):
        x = np.pi / 2
        y = rot_old[1] + rot_step_vec * min(i, rot_steps_count)
        z = np.pi / 2
        return (x, y, z)


