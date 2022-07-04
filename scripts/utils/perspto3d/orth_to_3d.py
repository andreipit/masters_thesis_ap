import time
import numpy as np
from matplotlib import pyplot as plt
import math

from environment.modules.robot.simulation.engine import Engine
from utils.custom_types import NDArray
from environment.envs.env_01 import Env01
from .persp_to_orth import PerspToOrth

class OrthTo3d():

    #def compute_pixel_3d_position(self, m: ProcModel, a: ArgsModel, r: Robot, l: Logger, t: Trainer):
    def compute_pixel_3d_position(self, px_id: NDArray["3,1", float], depth_heightmap ):
        """ 
        px_id[0] = angle (22.5 steps count)
        px_id[1] = y
        px_id[2] = x

        Ex: pixel_id = (5, 56, 72), 
            num_rotations 16
            best_rotation_angle 0.7853981633974483
        Action: grasp at (4, 56, 71) # - left far corner from hand view
        Action: grasp at (7, 23, 87) # - left middle point from hand view
        Action: grasp at (9, 103, 199) # - noLeft-noRight nearest point from hand view
        
        """
        num_rotations = 16 # just constant from nets body

        # 
        # 1st pixel value is angle in 22.5 steps (not deg or rad!)
        #rotation_step = 360 / 16 = 22.5 # on 22.5 degrees we rotate 16 times
        angle_deg = px_id[0] * 22.5
        angle_rad = np.deg2rad(angle_deg)
        best_rotation_angle = angle_rad

        best_pix_x = px_id[2]
        best_pix_y = px_id[1]

        heightmap_resolution: float = 0.002
        workspace_limits: list = [[ -0.724, -0.276 ], [ -0.224, 0.224 ], [ -0.0001, 0.4 ]] # 3 axis: xmax-xmin; ymax-ymin, zmax-zmin
        valid_depth_heightmap = depth_heightmap.copy()
        valid_depth_heightmap[np.isnan(valid_depth_heightmap)] = 0


        # actual pos
        x = best_pix_x * heightmap_resolution + workspace_limits[0][0]
        y = best_pix_y * heightmap_resolution + workspace_limits[1][0]
        z = valid_depth_heightmap[best_pix_y][best_pix_x] + workspace_limits[2][0]
        primitive_position = [x, y, z]

        return primitive_position
        pass
        ##Action: grasp at (4, 56, 71) # - left far corner from hand view
        ##Action: grasp at (7, 23, 87) # - left middle point from hand view
        ##Action: grasp at (9, 103, 199) # - noLeft-noRight nearest point from hand view
        
        ## Compute 3D position of pixel
        #print('Action: %s at (%d, %d, %d)' % (m.nonlocal_variables['primitive_action'], m.nonlocal_variables['best_pix_ind'][0], m.nonlocal_variables['best_pix_ind'][1], m.nonlocal_variables['best_pix_ind'][2]))
        #best_rotation_angle = np.deg2rad(m.nonlocal_variables['best_pix_ind'][0]*(360.0/t.m.model.num_rotations))
        #best_pix_x = m.nonlocal_variables['best_pix_ind'][2]
        #best_pix_y = m.nonlocal_variables['best_pix_ind'][1]
        ## 3D position
        #m.primitive_position = [best_pix_x * a.heightmap_resolution + a.workspace_limits[0][0], best_pix_y * a.heightmap_resolution + a.workspace_limits[1][0], m.valid_depth_heightmap[best_pix_y][best_pix_x] + a.workspace_limits[2][0]]
        ## If pushing, adjust start position, and make sure z value is safe and not too low
        #if m.nonlocal_variables['primitive_action'] == 'push': # or m.nonlocal_variables['primitive_action'] == 'place':
        #    # simulation parameter
        #    finger_width = 0.02
        #    safe_kernel_width = int(np.round((finger_width/2)/a.heightmap_resolution))
        #    local_region = m.valid_depth_heightmap[max(best_pix_y - safe_kernel_width, 0):min(best_pix_y + safe_kernel_width + 1, m.valid_depth_heightmap.shape[0]), max(best_pix_x - safe_kernel_width, 0):min(best_pix_x + safe_kernel_width + 1, m.valid_depth_heightmap.shape[1])]
        #    if local_region.size == 0:
        #        safe_z_position = a.workspace_limits[2][0] - 0.02
        #    else:
        #        safe_z_position = np.max_z_position = np.max(local_region) + a.workspace_limits[2][0] - 0.02
        #    m.primitive_position[2] = safe_z_position
        #    print('3D z position:', m.primitive_position[2])

        #    # Before pushing
        #    if a.stage == 'push_only':
        #        if m.best_grasp_conf <= a.grasp_reward_threshold and m.nonlocal_variables['push_step'] < a.max_push_episode_length:
        #            # Get grasp reward before pushing
        #            prev_img = m.color_heightmap
        #            obj_contours = r.get_obj_masks()
        #            obj_number = len(r.m.obj_mesh_ind)
        #            mask_all = np.zeros(prev_img.shape[:2], np.uint8)
        #            obj_grasp_predictions, mask_all = utils.get_obj_grasp_predictions(m.grasp_predictions, obj_contours, mask_all, prev_img, obj_number, a.workspace_limits, a.heightmap_resolution)

        #            m.prev_single_predictions = [np.max(obj_grasp_predictions[i]) for i in range(len(obj_grasp_predictions))]
        #            print('reward of grasping before pushing: ', m.prev_single_predictions) 

        #            # Get occupy ratio before pushing
        #            if a.goal_conditioned:
        #                m.prev_occupy_ratio = utils.get_occupy_ratio(m.goal_mask_heightmap, m.depth_heightmap)      








    #def compute_pixel_3d_position(self, m: ProcModel, a: ArgsModel, r: Robot, l: Logger, t: Trainer):
    #    # Compute 3D position of pixel
    #    print('Action: %s at (%d, %d, %d)' % (m.nonlocal_variables['primitive_action'], m.nonlocal_variables['best_pix_ind'][0], m.nonlocal_variables['best_pix_ind'][1], m.nonlocal_variables['best_pix_ind'][2]))
    #    m.best_rotation_angle = np.deg2rad(m.nonlocal_variables['best_pix_ind'][0]*(360.0/t.m.model.num_rotations))
    #    best_pix_x = m.nonlocal_variables['best_pix_ind'][2]
    #    best_pix_y = m.nonlocal_variables['best_pix_ind'][1]
    #    # 3D position
    #    m.primitive_position = [best_pix_x * a.heightmap_resolution + a.workspace_limits[0][0], best_pix_y * a.heightmap_resolution + a.workspace_limits[1][0], m.valid_depth_heightmap[best_pix_y][best_pix_x] + a.workspace_limits[2][0]]
    #    # If pushing, adjust start position, and make sure z value is safe and not too low
    #    if m.nonlocal_variables['primitive_action'] == 'push': # or m.nonlocal_variables['primitive_action'] == 'place':
    #        # simulation parameter
    #        finger_width = 0.02
    #        safe_kernel_width = int(np.round((finger_width/2)/a.heightmap_resolution))
    #        local_region = m.valid_depth_heightmap[max(best_pix_y - safe_kernel_width, 0):min(best_pix_y + safe_kernel_width + 1, m.valid_depth_heightmap.shape[0]), max(best_pix_x - safe_kernel_width, 0):min(best_pix_x + safe_kernel_width + 1, m.valid_depth_heightmap.shape[1])]
    #        if local_region.size == 0:
    #            safe_z_position = a.workspace_limits[2][0] - 0.02
    #        else:
    #            safe_z_position = np.max_z_position = np.max(local_region) + a.workspace_limits[2][0] - 0.02
    #        m.primitive_position[2] = safe_z_position
    #        print('3D z position:', m.primitive_position[2])

    #        # Before pushing
    #        if a.stage == 'push_only':
    #            if m.best_grasp_conf <= a.grasp_reward_threshold and m.nonlocal_variables['push_step'] < a.max_push_episode_length:
    #                # Get grasp reward before pushing
    #                prev_img = m.color_heightmap
    #                obj_contours = r.get_obj_masks()
    #                obj_number = len(r.m.obj_mesh_ind)
    #                mask_all = np.zeros(prev_img.shape[:2], np.uint8)
    #                obj_grasp_predictions, mask_all = utils.get_obj_grasp_predictions(m.grasp_predictions, obj_contours, mask_all, prev_img, obj_number, a.workspace_limits, a.heightmap_resolution)

    #                m.prev_single_predictions = [np.max(obj_grasp_predictions[i]) for i in range(len(obj_grasp_predictions))]
    #                print('reward of grasping before pushing: ', m.prev_single_predictions) 

    #                # Get occupy ratio before pushing
    #                if a.goal_conditioned:
    #                    m.prev_occupy_ratio = utils.get_occupy_ratio(m.goal_mask_heightmap, m.depth_heightmap)      

