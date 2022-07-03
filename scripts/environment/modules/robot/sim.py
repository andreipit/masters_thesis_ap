import time
import numpy as np

import utils.utils as utils
#from utils.arg.model import ArgsModel
from .model import RobotModel
from .simulation.engine import Engine
from utils.custom_types import NDArray

class RobotSim():

    def __init__(self):
        pass

    def connect(self, m:RobotModel) -> bool:
        m.engine = Engine()
        res =  m.engine.connect()
        return res != -1 #  if res!=-1 it is ok (true); if res==-1 it is bad (false)
        #if m.engine.connect() != -1:
        #    self.restart_sim(m)
        ## fix: now we can run even if simulation is running
        #m.engine.stop(); time.sleep(0.1); m.engine.start(); time.sleep(0.1)
        ### Setup virtual camera in simulation
        ##self.setup_sim_camera(m)

    def stop_start_game_fix(self, m:RobotModel):
        m.engine.stop(); 
        time.sleep(0.1); 
        m.engine.start(); 
        time.sleep(0.1)

    def restart_sim(self, m:RobotModel):
        sim_ret, m.UR5_target_handle = m.engine.gameobject_find('UR5_target')
        m.engine.global_position_set(_NewPos3D = (-0.5,0,0.3), _ObjID = m.UR5_target_handle)
        m.engine.stop()
        m.engine.start()
        m.engine.sleep(1)
        m.RG2_tip_handle = m.engine.restart_hard('UR5_tip')

    #def create_perspcamera_trans_matrix4x4(self, m:RobotModel) -> NDArray["4,4", float]:
    #    # 0) find persp camera in scene
    #    sim_ret, m.cam_handle = m.engine.gameobject_find('Vision_sensor_persp')

    #    # 1) get pos/rot
    #    sim_ret, cam_position = m.engine.global_position_get(_ObjID = m.cam_handle)
    #    sim_ret, cam_orientation = m.engine.global_rotation_get(_ObjID = m.cam_handle)
    #    # => cam_position [-1.0, 0.0, 0.5] 
    #    # => cam_orientation [3.141592025756836, 0.7853984832763672, 1.5707961320877075]

    #    # 2) Create matrices and fill them
    #    cam_trans = np.eye(4,4) # 4x4, all zeros, only diagonal items == 1
    #    """
    #    [[1. 0. 0. 0.]
    #     [0. 1. 0. 0.]
    #     [0. 0. 1. 0.]
    #     [0. 0. 0. 1.]]
    #    """
    #    cam_trans[0:3,3] = np.asarray(cam_position) # put [-1.0, 0.0, 0.5] to last column
    #    """
    #    [[ 1.   0.   0.  -1. ]
    #     [ 0.   1.   0.   0. ]
    #     [ 0.   0.   1.   0.5]
    #     [ 0.   0.   0.   1. ]]
    #    """
    #    cam_orientation = [-cam_orientation[0], -cam_orientation[1], -cam_orientation[2]] 
    #    # => [-3.141592025756836, -0.7853984832763672, -1.5707961320877075] # just 3 minuses
    #    cam_rotm = np.eye(4,4) # 4x4, all zeros, only diagonal items == 1
    #    cam_rotm[0:3,0:3] = np.linalg.inv(utils.euler2rotm(cam_orientation))
    #    """
    #    looks like rot matrix. If we mult each sensor vertex on it -> will get euler angles.
    #    [[ 1.37678730e-07 -7.07106555e-01  7.07107007e-01  0.00000000e+00]
    #     [-1.00000000e+00 -6.38652273e-07 -4.43944800e-07  0.00000000e+00]
    #     [ 7.65511775e-07 -7.07107007e-01 -7.07106555e-01  0.00000000e+00]
    #     [ 0.00000000e+00  0.00000000e+00  0.00000000e+00  1.00000000e+00]]
    #    """

    #    # 3) Save result to variable
    #    # combine pos and rot matrices into one. Matrix x Matrix x Vec = Matrix x Vec
    #    # cam_pose x Dummy = Dummy with same pos and rot, as Vision_sensor_persp
    #    #m.cam_pose = np.dot(cam_trans, cam_rotm) # Compute rigid transformation representating camera pose
    #    cam_pose = np.dot(cam_trans, cam_rotm) # Compute rigid transformation representating camera pose
    #    return cam_pose

    def get_2_perspcamera_photos_480x640(self, engine: Engine, cam_depth_scale: float) -> (NDArray["480,640,3", np.uint8], NDArray["480,640", float]):
        """
        Gets 2 images from "Vision_sensor_persp":
        RGB=480x640x3 int 0..255, Depth=480x640 float 0..2550
        """
        # 1) Get rgb
        sim_ret, cam_handle = engine.gameobject_find('Vision_sensor_persp')
        sim_ret, resolution, raw_image = engine.camera_image_rgb_get(_ObjID = cam_handle) # Vision_sensor_persp
        
        # 2) Normalize it
        # We have RGB image - 640x480x3. 
        # a)Reshape, b)to(0,1),remove negative,to(0,255), c)mirror, d) to int
        # a)Reshape
        color_img = np.asarray(raw_image) # convert to 1d array: (921600,)
        color_img.shape = (resolution[1], resolution[0], 3) # 921600=> 480x640x3
        # b)to(0,1),remove negative,to(0,255),
        color_img = color_img.astype(float)/255 # convert pixels 0..255 => 0..1
        # len(color_img[color_img < 0]) => 422234
        color_img[color_img < 0] += 1 # maybe fixes bug, when color is in (-1,0)
        color_img *= 255 # convert pixel back: 0..1 => 0..255
        # c)mirror
        color_img = np.fliplr(color_img) # like mirror columns order. Shape still (480, 640, 3)
        # d) to int
        color_img = color_img.astype(np.uint8)

        # 3) Get depth
        # Get depth image from simulation (just now we use different method name)
        sim_ret, resolution, depth_buffer = engine.camera_image_depth_get(_ObjID = cam_handle) # Vision_sensor_persp
        # We have alpha image (1 layer only) - 640x480.
        
        # 4) Normalize it
        # a) reshape
        depth_img = np.asarray(depth_buffer)
        depth_img.shape = (resolution[1], resolution[0])
        # b) mirror
        depth_img = np.fliplr(depth_img)
        zNear = 0.01
        zFar = 10
        # c) scale every pixel ~x10: 0..255 => 0..2550
        depth_img = depth_img * (zFar - zNear) + zNear
        # 125 * (10 - 0.01) + 0.01 = 1248.76

        #color_img[200][200][0] => 46, ie int
        #depth_img[200][200] => 10.0, ie float
        return color_img, depth_img * cam_depth_scale # RGB=480x640x3 int 0..255, Depth=480x640 float 0..255
