from utils.arg.model import ArgsModel
from .model import RobotModel
from .sim import RobotSim
from .objects import RobotObjects
from .simulation.engine import Engine

from .mask import RobotMask
from .push import RobotPush
from .move import RobotMove
from .gripper import RobotGripper
from .camera import RobotCamera
from .grasp import RobotGrasp
#from .px_to_3d import RobotPxTo3d

from utils.custom_types import NDArray


class Robot():
    debug: bool = False
    a: ArgsModel = None
    m: RobotModel = None
    sim: RobotSim = None
    obj: RobotObjects = None
    #pxto3d: RobotPxTo3d = None

    def __init__(self):
        pass

    def create_empty_helpers(self):
        self.m: RobotModel = RobotModel() # just fill some variables, using message from cmd
        self.sim: RobotSim  = RobotSim() # connect to sim, restart, set cam pos/rot, pick 2 screenshots from cam: rgb and depth
        self.obj: RobotObjects = RobotObjects() # instantiate some random cubes in scene
        self.mask = RobotMask()
        self.pusher = RobotPush()
        self.gripper = RobotGripper()
        self.mover = RobotMove()
        self.cam = RobotCamera()
        self.grasper = RobotGrasp()
        self.m.engine = Engine()
        #self.pxto3d = RobotPxTo3d()


    def connect_and_restart(self):
        if not self.sim.connect(self.m):
            self.sim.restart_sim(self.m)
        self.sim.stop_start_game_fix(self.m)

    def add_objects(self, num_obj = 8):
        self.obj.add_objects(self.m, num_obj = num_obj)

    def get_photo(self):
        return self.sim.get_2_perspcamera_photos_480x640(self.m.engine, self.m.cam_depth_scale)

    #def convert_px_to_3d(self, color_img, depth_img):
    #    self.pxto3d.convert_px_to_3d(color_img, depth_img, self.m)

    # test mask    
    def get_test_obj_mask(self, obj_ind):
        return self.mask.get_test_obj_mask(obj_ind, self.sim, self.m);
    def get_test_obj_masks(self, obj_ind):
        return self.mask.get_test_obj_masks(self.sim, self.m);
        
    # just mask    
    def get_obj_mask(self, obj_ind):
        return self.mask.get_obj_mask(obj_ind, self.sim, self.m);
    def get_obj_masks(self, obj_ind):
        return self.mask.get_obj_masks(self.sim, self.m);

    def grasp(self, pos: NDArray["3,1", float], rot: float):
        #self.grasper.move(pos, self.m.workspace_limits, self.m.engine)
        #self.grasper.rotate(rot, self.m.engine)
        return self.grasper.grasp( pos, rot, self.m.workspace_limits, self.m.engine, self.gripper, self.mover)

    def push(self, pos, rot):
        return self.pusher.push( pos, rot, self.m.workspace_limits, self.m.engine, self.gripper, self.mover)
        #self.grasper.move(pos, self.m.workspace_limits, self.m.engine)
        #return self.pusher.push(self.sim, self.m, self.gripper, self.mover, pos, rot, self.m.workspace_limits)

    # render
    def get_camera_data(self):
        return self.cam.get_camera_data(self.sim, self.m)

    # sim extra
    #def check_sim(self, a: ArgsModel, obj: RobotObjects, sim: RobotSim, m: RobotModel):
    def check_sim(self):
        #return self.sim.check_sim(a, obj, sim, m)
        # Check if simulation is stable by checking if gripper is within workspace
        sim_ret, gripper_position = self.m.engine.global_position_get(self.m.RG2_tip_handle)
        
        check_0a =  gripper_position[0] > self.a.workspace_limits[0][0] - 0.1
        check_0b = gripper_position[0] < self.a.workspace_limits[0][1] + 0.1
        check_1a =  gripper_position[1] > self.a.workspace_limits[1][0] - 0.1
        check_1b = gripper_position[1] < self.a.workspace_limits[1][1] + 0.1
        check_2a = gripper_position[2] > self.a.workspace_limits[2][0]
        check_2b =  gripper_position[2] < self.a.workspace_limits[2][1]

        sim_ok = check_0a and check_0b and check_1a and check_1b and check_2a and check_2b
        
        if not sim_ok:
            print('Simulation unstable. Restarting environment.')
            #print(check_0a , check_0b , check_1a , check_1b , check_2a , check_2b)
            #print('pos0,pos1,pos2:',gripper_position[0], gripper_position[1], gripper_position[2])
            self.sim.restart_sim(self.m)
            self.add_objects()
        else:
            print('Simulation is stable')


