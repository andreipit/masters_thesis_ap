import time
import numpy as np
from matplotlib import pyplot as plt
import math
#from typing import Optional, Tuple, Union, TypeVar
from typing import Tuple

from environment.modules.robot.simulation.engine import Engine
from utils.custom_types import NDArray


class PerspToOrth():

    def __init__(self):
        pass

    def convert_persp_to_gravity_orth(self, color_img, depth_img, engine: Engine) -> Tuple[NDArray["224,224,3", float], NDArray["224,224", float]]:
        cam_pose = self.create_perspcamera_trans_matrix4x4(engine) #env.r.sim.create_perspcamera_trans_matrix4x4(env.r.m)
        cam_intrinsics = np.asarray([[618.62, 0, 320], [0, 618.62, 240], [0, 0, 1]])
        workspace_limits: list = [[ -0.724, -0.276 ], [ -0.224, 0.224 ], [ -0.0001, 0.4 ]] # 3 axis: xmax-xmin; ymax-ymin, zmax-zmin
        heightmap_resolution: float = 0.002

        color_heightmap, depth_heightmap = self._get_heightmap(
            color_img, 
            depth_img, 
            cam_intrinsics, 
            cam_pose, 
            workspace_limits,
            heightmap_resolution)

        # make same rotation as in persp image: rot90 + flip:
        color_heightmap = np.rot90(color_heightmap, k=1, axes=(0,1))
        color_heightmap = np.flip(color_heightmap, axis=1)
        depth_heightmap = np.rot90(depth_heightmap, k=1, axes=(0,1))
        depth_heightmap = np.flip(depth_heightmap, axis=1)

        # set missing heights == 0
        valid_depth_heightmap = depth_heightmap.copy()
        valid_depth_heightmap[np.isnan(valid_depth_heightmap)] = 0


        return color_heightmap, valid_depth_heightmap
        pass

    def create_perspcamera_trans_matrix4x4(self, engine: Engine) -> NDArray["4,4", float]:
        # 0) find persp camera in scene
        sim_ret, cam_handle = engine.gameobject_find('Vision_sensor_persp')

        # 1) get pos/rot
        sim_ret, cam_position = engine.global_position_get(_ObjID = cam_handle)
        sim_ret, cam_orientation = engine.global_rotation_get(_ObjID = cam_handle)
        # => cam_position [-1.0, 0.0, 0.5] 
        # => cam_orientation [3.141592025756836, 0.7853984832763672, 1.5707961320877075]

        # 2) Create matrices and fill them
        cam_trans = np.eye(4,4) # 4x4, all zeros, only diagonal items == 1
        """
        [[1. 0. 0. 0.]
         [0. 1. 0. 0.]
         [0. 0. 1. 0.]
         [0. 0. 0. 1.]]
        """
        cam_trans[0:3,3] = np.asarray(cam_position) # put [-1.0, 0.0, 0.5] to last column
        """
        [[ 1.   0.   0.  -1. ]
         [ 0.   1.   0.   0. ]
         [ 0.   0.   1.   0.5]
         [ 0.   0.   0.   1. ]]
        """
        cam_orientation = [-cam_orientation[0], -cam_orientation[1], -cam_orientation[2]] 
        # => [-3.141592025756836, -0.7853984832763672, -1.5707961320877075] # just 3 minuses
        cam_rotm = np.eye(4,4) # 4x4, all zeros, only diagonal items == 1
        cam_rotm[0:3,0:3] = np.linalg.inv(self._euler2rotm(cam_orientation))
        """
        looks like rot matrix. If we mult each sensor vertex on it -> will get euler angles.
        [[ 1.37678730e-07 -7.07106555e-01  7.07107007e-01  0.00000000e+00]
         [-1.00000000e+00 -6.38652273e-07 -4.43944800e-07  0.00000000e+00]
         [ 7.65511775e-07 -7.07107007e-01 -7.07106555e-01  0.00000000e+00]
         [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]
        """

        # 3) Save result to variable
        # combine pos and rot matrices into one. Matrix x Matrix x Vec = Matrix x Vec
        # cam_pose x Dummy = Dummy with same pos and rot, as Vision_sensor_persp
        #m.cam_pose = np.dot(cam_trans, cam_rotm) # Compute rigid transformation representating camera pose
        cam_pose = np.dot(cam_trans, cam_rotm) # Compute rigid transformation representating camera pose
        return cam_pose

    def _get_pointcloud(self, color_img, depth_img, camera_intrinsics):

        # Get depth image size
        im_h = depth_img.shape[0]
        im_w = depth_img.shape[1]

        # Project depth into 3D point cloud in camera coordinates
        pix_x,pix_y = np.meshgrid(np.linspace(0,im_w-1,im_w), np.linspace(0,im_h-1,im_h))
        cam_pts_x = np.multiply(pix_x-camera_intrinsics[0][2],depth_img/camera_intrinsics[0][0])
        cam_pts_y = np.multiply(pix_y-camera_intrinsics[1][2],depth_img/camera_intrinsics[1][1])
        cam_pts_z = depth_img.copy()
        cam_pts_x.shape = (im_h*im_w,1)
        cam_pts_y.shape = (im_h*im_w,1)
        cam_pts_z.shape = (im_h*im_w,1)

        # Reshape image into colors for 3D point cloud
        rgb_pts_r = color_img[:,:,0]
        rgb_pts_g = color_img[:,:,1]
        rgb_pts_b = color_img[:,:,2]
        rgb_pts_r.shape = (im_h*im_w,1)
        rgb_pts_g.shape = (im_h*im_w,1)
        rgb_pts_b.shape = (im_h*im_w,1)

        cam_pts = np.concatenate((cam_pts_x, cam_pts_y, cam_pts_z), axis=1)
        rgb_pts = np.concatenate((rgb_pts_r, rgb_pts_g, rgb_pts_b), axis=1)

        return cam_pts, rgb_pts

    def _get_heightmap(self, color_img, depth_img, cam_intrinsics, cam_pose, workspace_limits, heightmap_resolution):

        # Compute heightmap size
        #print('---utils, workspace_limits=',workspace_limits, ' heightmap_resolution=', heightmap_resolution)
        heightmap_size = np.round(((workspace_limits[1][1] - workspace_limits[1][0])/heightmap_resolution, (workspace_limits[0][1] - workspace_limits[0][0])/heightmap_resolution)).astype(int)
        #print('---utils, heightmap_size=',heightmap_size)

        # Get 3D point cloud from RGB-D images
        surface_pts, color_pts = self._get_pointcloud(color_img, depth_img, cam_intrinsics)

        # Transform 3D point cloud from camera coordinates to robot coordinates
        surface_pts = np.transpose(np.dot(cam_pose[0:3,0:3],np.transpose(surface_pts)) + np.tile(cam_pose[0:3,3:],(1,surface_pts.shape[0])))

        # Sort surface points by z value
        sort_z_ind = np.argsort(surface_pts[:,2])
        surface_pts = surface_pts[sort_z_ind]
        color_pts = color_pts[sort_z_ind]

        # Filter out surface points outside heightmap boundaries
        heightmap_valid_ind = np.logical_and(np.logical_and(np.logical_and(np.logical_and(surface_pts[:,0] >= workspace_limits[0][0], surface_pts[:,0] < workspace_limits[0][1]), surface_pts[:,1] >= workspace_limits[1][0]), surface_pts[:,1] < workspace_limits[1][1]), surface_pts[:,2] < workspace_limits[2][1])
        surface_pts = surface_pts[heightmap_valid_ind]
        color_pts = color_pts[heightmap_valid_ind]

        # Create orthographic top-down-view RGB-D heightmaps
        color_heightmap_r = np.zeros((heightmap_size[0], heightmap_size[1], 1), dtype=np.uint8)
        color_heightmap_g = np.zeros((heightmap_size[0], heightmap_size[1], 1), dtype=np.uint8)
        color_heightmap_b = np.zeros((heightmap_size[0], heightmap_size[1], 1), dtype=np.uint8)
        depth_heightmap = np.zeros(heightmap_size)
        heightmap_pix_x = np.floor((surface_pts[:,0] - workspace_limits[0][0])/heightmap_resolution).astype(int)
        heightmap_pix_y = np.floor((surface_pts[:,1] - workspace_limits[1][0])/heightmap_resolution).astype(int)
        color_heightmap_r[heightmap_pix_y,heightmap_pix_x] = color_pts[:,[0]]
        color_heightmap_g[heightmap_pix_y,heightmap_pix_x] = color_pts[:,[1]]
        color_heightmap_b[heightmap_pix_y,heightmap_pix_x] = color_pts[:,[2]]
        color_heightmap = np.concatenate((color_heightmap_r, color_heightmap_g, color_heightmap_b), axis=2)
        depth_heightmap[heightmap_pix_y,heightmap_pix_x] = surface_pts[:,2]
        z_bottom = workspace_limits[2][0]
        depth_heightmap = depth_heightmap - z_bottom
        depth_heightmap[depth_heightmap < 0] = 0
        depth_heightmap[depth_heightmap == -z_bottom] = np.nan

        return color_heightmap, depth_heightmap
    
    def _euler2rotm(self, theta):
        # Get rotation matrix from euler angles
        R_x = np.array([[1,         0,                  0                   ],
                        [0,         math.cos(theta[0]), -math.sin(theta[0]) ],
                        [0,         math.sin(theta[0]), math.cos(theta[0])  ]
                        ])
        R_y = np.array([[math.cos(theta[1]),    0,      math.sin(theta[1])  ],
                        [0,                     1,      0                   ],
                        [-math.sin(theta[1]),   0,      math.cos(theta[1])  ]
                        ])         
        R_z = np.array([[math.cos(theta[2]),    -math.sin(theta[2]),    0],
                        [math.sin(theta[2]),    math.cos(theta[2]),     0],
                        [0,                     0,                      1]
                        ])            
        R = np.dot(R_z, np.dot( R_y, R_x ))
        # R = np.dot(R_x, np.dot( R_y, R_z ))
        return R

