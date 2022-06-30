import time
import numpy as np
import os
import random

from utils.arg.model import ArgsModel
from .model import RobotModel

class RobotObjects():

    prev_obj_positions = []
    obj_positions = []

    def __init__(self):
        pass

    def add_objects(self, m: RobotModel, num_obj: int = 8):
        """ 
            Randomly select [num_obj] objects from 0.obj to 7.obj
            GameObject.name == filename.obj
            GameObject ID is called [Handle] and equal strange number
        """
        mesh_list = [0, 1, 2, 3, 4, 5, 6, 7]
        mesh_list = mesh_list[0 : num_obj]
        random.shuffle(mesh_list)
        print('Instantiating', num_obj, 'blocks...')

        for object_idx in mesh_list: # in 1.2: 0,1,2,3,4 (obj_number == 5)
            curr_mesh_file = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'objects', 'blocks', str(object_idx) + '.obj')

            # position 
            drop_x = (m.workspace_limits[0][1] - m.workspace_limits[0][0] - 0.2) * np.random.random_sample() + m.workspace_limits[0][0] + 0.1
            drop_y = (m.workspace_limits[1][1] - m.workspace_limits[1][0] - 0.2) * np.random.random_sample() + m.workspace_limits[1][0] + 0.1
            object_position = [drop_x, drop_y, 0.15] # [-0.5563970338899049, -0.05543686472451201, 0.15]
            # rotation
            object_orientation = [2*np.pi*np.random.random_sample(), 2*np.pi*np.random.random_sample(), 2*np.pi*np.random.random_sample()]
            # color
            obj_mesh_color = m.color_space[np.asarray(range(num_obj)) % 10, :]
            object_color = [obj_mesh_color[object_idx][0], obj_mesh_color[object_idx][1], obj_mesh_color[object_idx][2]]
            # name
            curr_shape_name = 'shape_%02d' % object_idx # => shape_00

            for i in range(5): # give him 5 attempts to call function in scene
                time.sleep(0.3)
                ret_resp, ret_ints, ret_floats, ret_strings, ret_buffer = m.engine.getcomponent_and_run(
                    _ObjName = 'remoteApiCommandServer', 
                    _FunName = 'importShape',
                    _Input = ([0, 0, 255, 0], #int
                              object_position + object_orientation + object_color, #float
                              [curr_mesh_file, curr_shape_name], #string
                              bytearray()) # buffer
                )
                if ret_resp != 8:
                    m.object_handles.append(ret_ints[0]) # save gameObject id
                    break
                elif i == 4: #  if nothing helped -> exit
                    print('Failed to add new objects to simulation. Please restart.')
                    exit()

        print('Instantiating is done. IDs of GameObjects:', m.object_handles)

    def get_obj_positions(self, m: RobotModel):
        obj_positions = []
        for object_handle in m.object_handles:
            sim_ret, object_position = m.engine.global_position_get(_ObjID = object_handle)
            obj_positions.append(object_position)
        return obj_positions

