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

class RobotPush():

    def __init__(self):
        pass
    
    def push(self, pos: NDArray["3,1", float], degrees: float, limits: list, engine: Engine,  gripper: RobotGripper, mover: RobotMove) -> bool:
        gripper_full_closed = gripper.close_gripper(engine)
        mover.rotate(degrees, engine)
        mover.move(pos, limits, engine)

        pos[2] -= 0.15
        mover.move(pos, limits, engine)
        
        print('before',pos)
        pos = self._get_push_end(pos, degrees)
        print('after',pos)
        mover.move(pos, limits, engine)

        pos[2] += 0.15
        mover.move(pos, limits, engine)

        success = True
        return success
        #gripper.open_gripper(engine)
        #_, pos_old = engine.global_position_get(_ObjName = 'UR5_target') #print('pos_old', pos_old, ' \n pos_new', pos_new)
        #grasp_success = not gripper_full_closed
        #return grasp_success

    def _get_push_end(self, start: NDArray["3,1", float], degrees_start: float) -> NDArray["3,1", float]:

        #pos[1] += 0.3
        #return pos

        push_length = 0.13

        x = start[0] + push_length * np.cos(degrees_start)
        y = start[1] + push_length * np.sin(degrees_start)
        z = start[2] # same height
        return np.asarray([x, y, z])

        #push_orientation = [1.0,0.0]
        #x = push_orientation[0]*np.cos(heightmap_rotation_angle)


        #push_direction = np.asarray([push_orientation[0]*np.cos(heightmap_rotation_angle) - push_orientation[1]*np.sin(heightmap_rotation_angle), push_orientation[0]*np.sin(heightmap_rotation_angle) + push_orientation[1]*np.cos(heightmap_rotation_angle)])



        ## Move gripper to location above pushing point
        #pushing_point_margin = 0.1
        #location_above_pushing_point = (position[0], position[1], position[2] + pushing_point_margin)

        ## Compute target location (push to the right)
        #push_length = 0.13
        #target_x = min(max(position[0] + push_direction[0]*push_length, workspace_limits[0][0]), workspace_limits[0][1])
        #target_y = min(max(position[1] + push_direction[1]*push_length, workspace_limits[1][0]), workspace_limits[1][1])
        #push_length = np.sqrt(np.power(target_x-position[0],2)+np.power(target_y-position[1],2))

        ## Move in pushing direction towards target location
        #mover.move_to(sim, m, [target_x, target_y, position[2]], None)

        #pass