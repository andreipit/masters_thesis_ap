import time
import numpy as np

import utils.utils as utils
from utils.arg.model import ArgsModel
from .model import RobotModel
from .sim import RobotSim
from .simulation.engine import Engine
from utils.custom_types import NDArray

class RobotGripper():

    def __init__(self):
        pass

    
    def close_gripper(self, engine:Engine, asynch=False):

        gripper_motor_velocity = -0.5
        gripper_motor_force = 100

        sim_ret, RG2_gripper_handle = engine.gameobject_find(_Name = 'RG2_openCloseJoint')
        sim_ret, gripper_joint_position = engine.global_position_get_joint(_ObjID = RG2_gripper_handle)

        engine.joint_force_set(_ObjID = RG2_gripper_handle, _Value = gripper_motor_force)
        engine.joint_target_velocity_set(_ObjID = RG2_gripper_handle, _Value = gripper_motor_velocity)
        
        gripper_fully_closed = False
        while gripper_joint_position > -0.045: # Block until gripper is fully closed
            sim_ret, new_gripper_joint_position = engine.global_position_get_joint(_ObjID = RG2_gripper_handle)
            #sim_ret, new_gripper_joint_position = vrep.simxGetJointPosition(self.sim_client, RG2_gripper_handle, vrep.simx_opmode_blocking)
            # print(gripper_joint_position)
            if new_gripper_joint_position >= gripper_joint_position:
                return gripper_fully_closed
            gripper_joint_position = new_gripper_joint_position
        gripper_fully_closed = True

        return gripper_fully_closed


    def open_gripper(self, engine:Engine, asynch=False):
        gripper_motor_velocity = 0.5
        gripper_motor_force = 20
        sim_ret, RG2_gripper_handle = engine.gameobject_find('RG2_openCloseJoint')
        sim_ret, gripper_joint_position = engine.global_position_get_joint(_ObjID = RG2_gripper_handle)
        engine.joint_force_set(_ObjID = RG2_gripper_handle, _Value = gripper_motor_force)
        engine.joint_target_velocity_set(_ObjID = RG2_gripper_handle, _Value = gripper_motor_velocity)
        while gripper_joint_position < 0.03: # Block until gripper is fully open
            sim_ret, gripper_joint_position = engine.global_position_get_joint(_ObjID = RG2_gripper_handle)    
