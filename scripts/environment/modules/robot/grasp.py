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

    def _move_to():
        pass

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

    def grasp(self, pos_new, rot_new, limits, engine: Engine):

        for x in range(36):
            self.rotate(x*10, engine)
        #self.rotate(rot_new, engine)
        self.move(pos_new, limits, engine)

    def rotate(self,  angle_new, engine: Engine):
        """ angle_new is in degrees """

        if angle_new > 360:
            angle_new = 360 % angle_new
            
        if angle_new < -360:
            angle_new = -360 % angle_new

        if angle_new > 180:
            angle_new -= 180
        elif angle_new < 0:
            angle_new = 180 - angle_new

        print('angle_new',angle_new)
            # trim all to 0..90
        angle_new = angle_new * np.pi / 180 # convert to radians
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id) # radians!!!
        print('rot_old',rot_old)
        print('angle_new rad',angle_new)
        for i in range(1, 10 + 1):
            angle_next = self.lerp_f(rot_old[1], angle_new, i / 10)
            print('angle_next',angle_next)
            engine.global_rotation_set(_ObjID = dummy_id, _NewRot3D = (np.pi / 2, angle_next, np.pi / 2))

    def move(self, pos_new, limits, engine: Engine):
        pos_new = self._convert_pos(pos_new, limits)
        _, dummy_id = engine.gameobject_find('UR5_target')
        _, pos_old = engine.global_position_get(_ObjID = dummy_id) #print('pos_old', pos_old, ' \n pos_new', pos_new)
        for i in range(1, 20 + 1):
            pos_next = self.lerp_vec(pos_old, pos_new, i / 20) #print('pos_next', pos_next)
            engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_next)



    def grasp44(self, pos_new, rot_new, limits, engine: Engine):
        """
        Grasp is just moving dummy "UR5_target"
        """
        #_, dummy_id = engine.gameobject_find('UR5_target')
        #engine.global_position_set(_ObjID = dummy_id, _NewPos3D = pos_new)
        #return 

        _, dummy_id = engine.gameobject_find('UR5_target')
        _, pos_old = engine.global_position_get(_ObjID = dummy_id)
        _, rot_old = engine.global_rotation_get(_ObjID = dummy_id)

        print('pos_old', pos_old)

        pos_new = self._convert_pos(pos_new, limits)
        rot_new = self._convert_rot(rot_new)
        print('pos_new', pos_new)

        # where and how many times
        pos_step_vec, pos_steps_count = self._get_pos_step(pos_old, pos_new)
        rot_step_vec, rot_steps_count = self._get_rot_step(rot_old, rot_new)
        print('pos_step_vec', pos_step_vec)
        print('pos_steps_count', pos_steps_count)

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



    def grasp3(self, sim: RobotSim, m: RobotModel, cam: RobotCamera, gripper: RobotGripper, mover: RobotMove, obj: RobotObjects,
              position, #  -0.5, 0, 0.2 # center of desk on height 0.2
              heightmap_rotation_angle, # 22.5 
              workspace_limits): # [[ -0.724, -0.276 ], [ -0.224, 0.224 ], [ -0.0001, 0.4 ]]

        #print('rot=', heightmap_rotation_angle, ' pos=', position)

        #22.5 ==> -1.05:  16 images, step=22.5 degrees, 10%4=2, 22.5%3.14=0.52; 0.52 - 3.14/2 =-1.05
        # convert to radians and set start to pi/2 degrees
        # Compute tool orientation from heightmap rotation angle
        tool_rotation_angle = (heightmap_rotation_angle % np.pi) - np.pi/2 #  -1.0619449019234484

        # z -= 0.04  ==> z = 0.16
        # Avoid collision with floor
        # z: 0.5 ==> 0.46:  max(0.5-0.04, -0.0001 + 0.02) => 0.5-0.04 is higher! So use it!
        # [-0.5   0.    0.16]
        position = np.asarray(position).copy()
        position[2] = max(position[2] - 0.04, workspace_limits[2][0] + 0.02) #  workspace_limits[2] [-0.0001, 0.4]

        # z += 0.15 ==> z = 0.31
        # Move gripper to location above grasp target
        grasp_location_margin = 0.15
        # sim_ret, UR5_target_handle = vrep.simxGetObjectHandle(self.sim_client,'UR5_target',vrep.simx_opmode_blocking)
        location_above_grasp_target = (position[0], position[1], position[2] + grasp_location_margin) #  (-0.5, 0.0, 0.31)


        #---- Compute gripper position and linear movement increments-----
        #UR5_target_position == [-0.5, 0.0, 0.30000001192092896] # higher then target on 0.1
        tool_position = location_above_grasp_target # copy pos
        # gripper moves to UR5_target at game start (center of L gripper)
        sim_ret, UR5_target_handle = m.engine.gameobject_find('UR5_target')
        # UR5_target global pos
        sim_ret, UR5_target_position = m.engine.global_position_get(_ObjID = UR5_target_handle)


        # vector from UR5_target to final pos
        # target(-0.5, 0.0, 0.31) -  current[-0.5, 0.0, 0.30000001192092896] =  [0.,0.,0.00999999]
        # approx: 0.31 - 0.3 = 0.01
        move_direction = np.asarray([tool_position[0] - UR5_target_position[0], tool_position[1] - UR5_target_position[1], tool_position[2] - UR5_target_position[2]])
        # move_magnitude = 0.009999988079071043 ~= 0.01
        move_magnitude = np.linalg.norm(move_direction) # len of that vector
        
        # move_step [0.   0.   0.05]
        move_step = 0.05*move_direction/move_magnitude # Vector3 step = 5% of vector len in each axis
        #print('move_step',move_step)

        # step=5%, so steps count in x axis = 20
        if move_direction[0] == None or move_step[0] == None or move_direction[0]/move_step[0] == None or np.floor(move_direction[0]/move_step[0]) == None:
            num_move_steps = 0
        else:
            num_move_steps = int(np.floor(move_direction[0]/move_step[0]))
            print('num_move_steps222',num_move_steps)

        # rot step = 0.3 degrees, num steps = (targetAngle - startAngle) / 0.3
        # Compute gripper orientation and rotation increments
        sim_ret, gripper_orientation = m.engine.global_rotation_get(_ObjID = UR5_target_handle)
        #sim_ret, gripper_orientation = vrep.simxGetObjectOrientation(self.sim_client, self.UR5_target_handle, -1, vrep.simx_opmode_blocking)
        rotation_step = 0.3 if (tool_rotation_angle - gripper_orientation[1] > 0) else -0.3
        num_rotation_steps = int(np.floor((tool_rotation_angle - gripper_orientation[1])/rotation_step))


        # Simultaneously move and rotate gripper
        for step_iter in range(max(num_move_steps, num_rotation_steps)):
            m.engine.global_position_set(
                _ObjID = UR5_target_handle, 
                _NewPos3D = (
                    UR5_target_position[0] + move_step[0]*min(step_iter,num_move_steps), 
                    UR5_target_position[1] + move_step[1]*min(step_iter,num_move_steps), 
                    UR5_target_position[2] + move_step[2]*min(step_iter,num_move_steps)
                )
            )
            #m.engine.global_rotation_set(
            #    _ObjID = UR5_target_handle, 
            #    _NewRot3D = (
            #        np.pi/2, 
            #        gripper_orientation[1] + rotation_step*min(step_iter,num_rotation_steps), 
            #        np.pi/2
            #    )
            #)

     # Primitives ----------------------------------------------------------
    def grasp_backup(self, a: ArgsModel, sim: RobotSim, m: RobotModel, cam: RobotCamera, gripper: RobotGripper, mover: RobotMove, obj: RobotObjects,
              position, 
              heightmap_rotation_angle, 
              workspace_limits):
        print('Executing: grasp at (%f, %f, %f)' % (position[0], position[1], position[2]))
        # Compute tool orientation from heightmap rotation angle
        tool_rotation_angle = (heightmap_rotation_angle % np.pi) - np.pi/2

        # Avoid collision with floor
        position = np.asarray(position).copy()
        position[2] = max(position[2] - 0.04, workspace_limits[2][0] + 0.02)

        # Move gripper to location above grasp target
        grasp_location_margin = 0.15
        # sim_ret, UR5_target_handle = vrep.simxGetObjectHandle(self.sim_client,'UR5_target',vrep.simx_opmode_blocking)
        location_above_grasp_target = (position[0], position[1], position[2] + grasp_location_margin)

        # Compute gripper position and linear movement increments
        tool_position = location_above_grasp_target

        sim_ret, UR5_target_handle = m.engine.gameobject_find('UR5_target')
        sim_ret, UR5_target_position = m.engine.global_position_get(_ObjID = UR5_target_handle)
        #sim_ret, UR5_target_position = vrep.simxGetObjectPosition(self.sim_client, self.UR5_target_handle,-1,vrep.simx_opmode_blocking)
        move_direction = np.asarray([tool_position[0] - UR5_target_position[0], tool_position[1] - UR5_target_position[1], tool_position[2] - UR5_target_position[2]])
        move_magnitude = np.linalg.norm(move_direction)
        move_step = 0.05*move_direction/move_magnitude

        #if move_direction == None or  move_direction[0] == None or move_step == None or move_step[0] == None or move_direction[0]/move_step[0] == None or np.floor(move_direction[0]/move_step[0]) == None:
        if move_direction[0] == None or move_step[0] == None or move_direction[0]/move_step[0] == None or np.floor(move_direction[0]/move_step[0]) == None:
            num_move_steps = 0
        else:
            num_move_steps = int(np.floor(move_direction[0]/move_step[0]))

        # Compute gripper orientation and rotation increments
        sim_ret, gripper_orientation = m.engine.global_rotation_get(_ObjID = UR5_target_handle)
        #sim_ret, gripper_orientation = vrep.simxGetObjectOrientation(self.sim_client, self.UR5_target_handle, -1, vrep.simx_opmode_blocking)
        rotation_step = 0.3 if (tool_rotation_angle - gripper_orientation[1] > 0) else -0.3
        num_rotation_steps = int(np.floor((tool_rotation_angle - gripper_orientation[1])/rotation_step))

        # Simultaneously move and rotate gripper
        for step_iter in range(max(num_move_steps, num_rotation_steps)):
            m.engine.global_position_set(
                _ObjID = UR5_target_handle, 
                _NewPos3D = (
                    UR5_target_position[0] + move_step[0]*min(step_iter,num_move_steps), 
                    UR5_target_position[1] + move_step[1]*min(step_iter,num_move_steps), 
                    UR5_target_position[2] + move_step[2]*min(step_iter,num_move_steps)
                )
            )
            m.engine.global_rotation_set(
                _ObjID = UR5_target_handle, 
                _NewRot3D = (
                    np.pi/2, 
                    gripper_orientation[1] + rotation_step*min(step_iter,num_rotation_steps), 
                    np.pi/2
                )
            )
        m.engine.global_position_set(
            _ObjID = UR5_target_handle, 
            _NewPos3D = (tool_position[0], tool_position[1], tool_position[2])
        )
        m.engine.global_rotation_set(
            _ObjID = UR5_target_handle, 
            _NewRot3D = (np.pi/2, tool_rotation_angle, np.pi/2)
        )
        # # Simultaneously move and rotate gripper
        #for step_iter in range(max(num_move_steps, num_rotation_steps)):
        #    vrep.simxSetObjectPosition(self.sim_client,self.UR5_target_handle,-1,(UR5_target_position[0] + move_step[0]*min(step_iter,num_move_steps), UR5_target_position[1] + move_step[1]*min(step_iter,num_move_steps), UR5_target_position[2] + move_step[2]*min(step_iter,num_move_steps)),vrep.simx_opmode_blocking)
        #    vrep.simxSetObjectOrientation(self.sim_client, self.UR5_target_handle, -1, (np.pi/2, gripper_orientation[1] + rotation_step*min(step_iter,num_rotation_steps), np.pi/2), vrep.simx_opmode_blocking)
        #vrep.simxSetObjectPosition(self.sim_client,self.UR5_target_handle,-1,(tool_position[0],tool_position[1],tool_position[2]),vrep.simx_opmode_blocking)
        #vrep.simxSetObjectOrientation(self.sim_client, self.UR5_target_handle, -1, (np.pi/2, tool_rotation_angle, np.pi/2), vrep.simx_opmode_blocking)

        # Ensure gripper is open
        gripper.open_gripper(sim, m)

        # Approach grasp target
        mover.move_to(sim, m, position, None)

        # Get images before grasping
        color_img, depth_img = cam.get_camera_data(sim, m)
        depth_img = depth_img * m.cam_depth_scale # Apply depth scale from calibration

        # Get heightmaps beforew grasping
        cam_pose = sim.create_perspcamera_trans_matrix4x4(m)

        color_heightmap, depth_heightmap = utils.get_heightmap(color_img, depth_img, m.cam_intrinsics,
                                                                cam_pose, workspace_limits,
                                                                0.002)  # heightmap resolution from args
        valid_depth_heightmap = depth_heightmap.copy()
        valid_depth_heightmap[np.isnan(valid_depth_heightmap)] = 0

        # Close gripper to grasp target
        gripper_full_closed = gripper.close_gripper(sim, m)

        # Move gripper to location above grasp target
        mover.move_to(sim, m, location_above_grasp_target, None)

        # Check if grasp is successful
        gripper_full_closed = gripper.close_gripper(sim, m)
        grasp_success = not gripper_full_closed

        # Move the grasped object elsewhere
        if grasp_success:
            object_positions = np.asarray(obj.get_obj_positions(m))
            object_positions = object_positions[:,2]
            grasped_object_ind = np.argmax(object_positions)
            print('grasp obj z position', max(object_positions))
            grasped_object_handle = m.object_handles[grasped_object_ind]
            m.engine.global_position_set(_ObjID = grasped_object_handle, _NewPos3D = (-0.5, 0.5 + 0.05*float(grasped_object_ind), 0.1))
            #vrep.simxSetObjectPosition(self.sim_client,grasped_object_handle,-1,(-0.5, 0.5 + 0.05*float(grasped_object_ind), 0.1),vrep.simx_opmode_blocking)
            return grasp_success, color_img, depth_img, color_heightmap, valid_depth_heightmap, grasped_object_ind
        else:
            return grasp_success, None, None, None, None, None

