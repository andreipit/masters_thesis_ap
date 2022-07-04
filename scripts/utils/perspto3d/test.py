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

    # persp
    converter1 = PerspToOrth()
    color_img, depth_img = converter1.get_camera_data(env.r.m.engine)
    cam_depth_scale: float = 1
    depth_img = depth_img * cam_depth_scale # env.r.m.cam_depth_scale # Apply depth scale from calibration
    print('persp color_img.shape=', color_img.shape) # (480, 640, 3)
    print('persp depth_img.shape=', depth_img.shape) # (480, 640)
    plt.imshow(color_img); plt.show(block=True)
    plt.imshow(depth_img); plt.show(block=True)

    # persp -> orth
    cam_pose = converter1.create_perspcamera_trans_matrix4x4(env.r.m.engine) #env.r.sim.create_perspcamera_trans_matrix4x4(env.r.m)
    color_heightmap, depth_heightmap = converter1.convert_persp_to_gravity_orth(color_img, depth_img, cam_pose, env.r.m.engine)
    print('color_heightmap.shape=', color_heightmap.shape) # (224, 224, 3)
    print('depth_heightmap.shape=', depth_heightmap.shape) # (224, 224)
    plt.imshow(color_heightmap); plt.show(block=True)
    plt.imshow(depth_heightmap); plt.show(block=True)
    
    # orth -> 3d
    converter2 = OrthTo3d()
    # test seed
    alp = 4 * 22.5
    top_l = (alp, 0, 0) # arm-eye-view (camera looks TO arm face)
    top_r = (alp, 223, 0) # arm-eye-view (camera looks TO arm face)
    bottom_r = (alp, 223, 223) # arm-eye-view (camera looks TO arm face)
    bottom_l = (alp, 0, 223) # arm-eye-view (camera looks TO arm face)
    heightmap_resolution: float = 0.002
    for coor in [top_l, top_r, bottom_r, bottom_l]:
        pos3d = converter2.pixel_to_3d(coor[2], coor[1], depth_heightmap, heightmap_resolution, env.r.m.workspace_limits)
        env.r.mover.move(pos3d, env.r.m.workspace_limits, env.r.m.engine)
        env.r.mover.rotate(alp, env.r.m.engine)











