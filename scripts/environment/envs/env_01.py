from numpy import float64
from environment.modules.importer import *
#self.initer, self.steper, self.reseter, self.renderer, self.model = EnvInit(), EnvStep(), EnvReset(), EnvRender(), EnvModel()
import torch


class Env01(Env):

    r : Robot = None
    observation_space: Box = None


    def __init__(self):
        """
        state (s_t) - rgb-d image 224x224x4 (heightmap representation)
        action (a_t) = (psi, q) | psi E {push,grasp}, q -> p E s_t, where p is pixel, q is 3d coords of p
        example: (0, 5, 6, 8) => push at Vector3(5,6,8) to right 10sm
        """
        #self.observation_space = Box(low=-1., high=1., shape=(480, 640, 3), dtype="float32") # color + depth => 4 layers
        #self.observation_space = Box(low=-1., high=1., shape=(224, 224), dtype="float64") # color + depth => 4 layers
        self.observation_space = Box(low=-1000., high=1000., shape=(2, 224, 224, 3), dtype="float64") # color + depth => 4 layers
        #self.observation_space = Box(low=-10., high=10., shape=(2, 1, 3, 640, 640), dtype="float32") # 2 mini batches: both 3x640x640 wrapped in extra dim
        #self.observation_space = Box(low=-10., high=10., shape=(2, 1, 3, 640, 640), dtype="float32") # 2 mini batches: both 3x640x640 wrapped in extra dim
        #self.observation_space = Box(low=-1., high=1., shape=(480, 640), dtype="float32") # 2 mini batches: both 3x640x640 wrapped in extra dim
        self.action_space = Box(low=-1., high=1., shape=(5,), dtype="float64") # [1.0, -0.5, 0, 0.25, 90] -> push at (-0.5,0,0.25) on angle 90
        self.total_r = -1
        self.round = -1
        print('Env is initted')
    
    def step(self, a: NDArray["5,1", float]) -> Tuple[ObsType, float, bool, dict]:
        r = 0
        done = False
        info = {}

        a_type: str = 'push' if (a[0] == 0.0) else 'grasp'
        a_coord: NDArray["3,1", float] = np.asarray([a[1], a[2], a[3]])
        a_angle: float = a[4] # degrees

        if a_type == 'grasp':
            success = self.r.grasp(pos = a_coord, degrees = a_angle)
            print('grasp_success',success)
            r = (r+1) if success else (r-1)
        elif a_type == 'push':
            success = self.r.push(pos = a_coord, rot = a_angle)
            r = (r+0.5) if success else (r-0.5)

        self.state = self._get_state() 
        done = (r > 10)
        self.round += 1
        return self.state, r, done, info
    
    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, Tuple[ObsType, dict]]:
        """ Restart scene, add blocks, move arm to top position """
        self.r = Robot()
        self.r.create_empty_helpers()
        self.r.connect_and_restart()
        self.r.add_objects(5)

        # 3 ways to get state:
        #self.state = np.zeros((480, 640, 3), dtype="float32") # random.randint(0, 10)
        #self.state = self.observation_space.sample()
        #bg_color_img, bg_depth_img = self.r.get_photo()
        #self.state = bg_color_img
        self.state = self._get_state() 

        self.round = 0
        EnvReset.run()
        print('Env is resetted. State =', self.state.shape) # (480, 640, 3)  [x200;y200] = [45 45 45]
        return self.state # old version: np.ones((1,), dtype="float32")

    def render(self):
        #plt.imshow(self.state); plt.show(block=True)
        print("=============================================================================")
        print('Round:', self.round, 'Total r:', self.total_r, 'State:', self.state.shape, ' pixel_223_223:', self.state[223][223])
        print("=============================================================================")


    def _get_state(self) -> ObsType:
        """ depth enough for px->3d conversion, color used for mask only
        """
        color_img_480_640_3, depth_img_480_640 = self.r.get_persp_camera_data() # -> Tuple[NDArray["480,640,3", float], NDArray["480,640", float]]:
        c, depth_heightmap_224x224 = PerspToOrth().convert_persp_to_gravity_orth(color_img_480_640_3, depth_img_480_640, self.r.m.engine) # -> Tuple[NDArray["224,224,3", float], NDArray["224,224", float]]:
        d = Reshaper().add_3_depth_channels(depth_heightmap_224x224) # 224, 224 => 224, 224, 3
        mix = np.array([c, d], dtype=float64)
        #print('mix==',mix.shape, mix.dtype)

        #print('d', d.shape, d.dtype, d)
        #return depth_heightmap_224x224
        return mix
        
        #depth_img_3_channels = np.expand_dims(depth_img, axis=0) # 480,640 ==> 480,640,3
        #print('depth_img_3_channels',depth_img_3_channels.shape)
        #rs = np.array([color_img, depth_img_3_channels])
        #print('ppppp',rs.shape)
        #return rs

        #c, d = Reshaper().scale_224x224_to_640x480(c, d)
        #c, d = Reshaper().add_padding_keep_shape(c, d)
        #c, d = Reshaper().scale_and_normalize(c, d) # -> Tuple[NDArray["640, 640, 3", float], NDArray["640, 640, 3", float]]:
        #c, d = Reshaper().reshape_to_minibatch_1_3_640_640(c, d) #  -> Tuple[NDArray["1, 3, 640, 640", float], NDArray["1, 3, 640, 640", float]]:
        #color_heightmap = c
        #depth_heightmap = d
        #two_batches = torch.stack([color_heightmap, depth_heightmap]) # ([2, 1, 3, 640, 640])
        #print('---two_batches',two_batches.shape)
        #return two_batches


if __name__ == '__main__':
    print('hiiii')
    env = Env01()
    done = False
    while not done:
        state = env.reseter(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.steper(action)
        
        
