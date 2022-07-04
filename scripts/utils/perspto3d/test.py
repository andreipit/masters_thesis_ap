import time
import numpy as np
from matplotlib import pyplot as plt
import math

from environment.modules.robot.simulation.engine import Engine
from utils.custom_types import NDArray
from environment.envs.env_01 import Env01
from utils.perspto3d.persp_to_orth import PerspToOrth
from utils.perspto3d.orth_to_3d import OrthTo3d


if __name__ == '__main__':
    # start simulation
    env = Env01() #env = gym.make('environment:env-v1') # Env01()
    state = env.reset()
    env.render()
    done = False

    # create converters
    engine = Engine()

    # persp
    converter1 = PerspToOrth()
    color_img, depth_img = converter1.get_camera_data(engine)
    cam_depth_scale: float = 1
    depth_img = depth_img * cam_depth_scale # env.r.m.cam_depth_scale # Apply depth scale from calibration
    print('persp color_img.shape=', color_img.shape) # (480, 640, 3)
    print('persp depth_img.shape=', depth_img.shape) # (480, 640)
    #plt.imshow(color_img); plt.show(block=True)
    #plt.imshow(depth_img); plt.show(block=True)

    # persp -> orth
    cam_pose = converter1.create_perspcamera_trans_matrix4x4(engine) #env.r.sim.create_perspcamera_trans_matrix4x4(env.r.m)
    color_heightmap, depth_heightmap = converter1.convert_persp_to_gravity_orth(color_img, depth_img, cam_pose, engine)
    print('color_heightmap.shape=', color_heightmap.shape) # (224, 224, 3)
    print('depth_heightmap.shape=', depth_heightmap.shape) # (224, 224)
    #plt.imshow(color_heightmap); plt.show(block=True)
    #plt.imshow(depth_heightmap); plt.show(block=True)
    
    # orth -> 3d
    converter2 = OrthTo3d()

    pos3d = converter2.compute_pixel_3d_position((4, 56, 71), depth_heightmap)
    env.r.grasp(np.asarray(pos3d), 0)

