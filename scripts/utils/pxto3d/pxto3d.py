import time
import numpy as np

import utils.utils as utils
from environment.modules.robot.simulation.engine import Engine
from utils.custom_types import NDArray
from environment.envs.env_01 import Env01
from matplotlib import pyplot as plt


class Pxto3d():

    def __init__(self):
        pass
    
    def convert_px_to_3d(self, color_img, depth_img, cam_pose, engine: Engine):

        cam_intrinsics = np.asarray([[618.62, 0, 320], [0, 618.62, 240], [0, 0, 1]])
        workspace_limits: list = [[ -0.724, -0.276 ], [ -0.224, 0.224 ], [ -0.0001, 0.4 ]] # 3 axis: xmax-xmin; ymax-ymin, zmax-zmin
        heightmap_resolution: float = 0.002

        color_heightmap, depth_heightmap = utils.get_heightmap(
            color_img, 
            depth_img, 
            cam_intrinsics, 
            cam_pose, 
            workspace_limits,
            heightmap_resolution)

        plt.imshow(color_heightmap); plt.show(block=True)
        plt.imshow(depth_heightmap); plt.show(block=True)

        pass

    
    #def get_heightmap(self, m: MainloopModel, a: ArgsModel, r: Robot, l: Logger, t: Trainer, p: Proc):
    #    # Get heightmap from RGB-D image (by re-projecting 3D point cloud)
    #    p.m.color_heightmap, p.m.depth_heightmap = utils.get_heightmap(m.color_img, m.depth_img, r.m.cam_intrinsics, r.m.cam_pose, a.workspace_limits, a.heightmap_resolution)
    #    p.m.valid_depth_heightmap = p.m.depth_heightmap.copy()
    #    p.m.valid_depth_heightmap[np.isnan(p.m.valid_depth_heightmap)] = 0
    #    if a.goal_conditioned:
    #        if a.is_testing and not a.random_scene_testing:
    #            obj_contour = r.get_test_obj_mask(p.m.nonlocal_variables['goal_obj_idx'])
    #        else: # works in 1.2 start
    #            obj_contour = r.get_obj_mask(p.m.nonlocal_variables['goal_obj_idx'])
            
    #        p.m.goal_mask_heightmap = np.zeros(p.m.color_heightmap.shape[:2], np.uint8)
    #        p.m.goal_mask_heightmap = utils.get_goal_mask(obj_contour, p.m.goal_mask_heightmap, a.workspace_limits, a.heightmap_resolution)
    #        #kernel = np.ones((3,3))
    #        p.m.nonlocal_variables['border_occupy_ratio'] = utils.get_occupy_ratio(p.m.goal_mask_heightmap, p.m.depth_heightmap)
    #        p.m.writer.add_scalar('border_occupy_ratio', p.m.nonlocal_variables['border_occupy_ratio'], t.m.iteration)

    def get_camera_data(self, engine: Engine):

        # Get color image from simulation
        #sim_ret, resolution, raw_image = vrep.simxGetVisionSensorImage(self.sim_client, self.cam_handle, 0, vrep.simx_opmode_blocking)
        sim_ret, cam_handle = engine.gameobject_find('Vision_sensor_persp')
        sim_ret, resolution, raw_image = engine.camera_image_rgb_get(cam_handle)
        
        color_img = np.asarray(raw_image)
        color_img.shape = (resolution[1], resolution[0], 3)
        color_img = color_img.astype(float)/255
        color_img[color_img < 0] += 1
        color_img *= 255
        color_img = np.fliplr(color_img)
        color_img = color_img.astype(np.uint8)

        # Get depth image from simulation
        #sim_ret, resolution, depth_buffer = vrep.simxGetVisionSensorDepthBuffer(self.sim_client, self.cam_handle, vrep.simx_opmode_blocking)
        sim_ret, resolution, depth_buffer = engine.camera_image_depth_get(cam_handle)
        depth_img = np.asarray(depth_buffer)
        depth_img.shape = (resolution[1], resolution[0])
        depth_img = np.fliplr(depth_img)
        zNear = 0.01
        zFar = 10
        depth_img = depth_img * (zFar - zNear) + zNear

        return color_img, depth_img



if __name__ == '__main__':
    env = Env01() #env = gym.make('environment:env-v1') # Env01()
    state = env.reset()
    env.render()
    done = False

    converter = Pxto3d()

    # perst images
    color_img, depth_img = converter.get_camera_data(env.r.m.engine)
    depth_img = depth_img * env.r.m.cam_depth_scale # Apply depth scale from calibration
    plt.imshow(color_img); plt.show(block=True)
    plt.imshow(depth_img); plt.show(block=True)

    # converted to ortho
    cam_pose = env.r.sim.create_perspcamera_trans_matrix4x4(env.r.m)

    converter.convert_px_to_3d(color_img, depth_img, cam_pose, env.r.m.engine)


