from environment.modules.importer import *
#self.initer, self.steper, self.reseter, self.renderer, self.model = EnvInit(), EnvStep(), EnvReset(), EnvRender(), EnvModel()


class Env01(Env):

    r : Robot = None
    observation_space: Box = None


    def __init__(self):
        """
        state (s_t) - rgb-d image 224x224x4 (heightmap representation)
        action (a_t) = (psi, q) | psi E {push,grasp}, q -> p E s_t, where p is pixel, q is 3d coords of p
        example: (0, 5, 6, 8) => push at Vector3(5,6,8) to right 10sm
        """
        self.observation_space = Box(low=-1., high=1., shape=(480, 640, 3), dtype="float32")
        self.action_space = Box(low=-1., high=1., shape=(4,), dtype="float32")
        self.total_r = -1
        self.round = -1
        print('Env is initted')
    
    def step(self, a):
        r = 0
        done = False
        info = {}

        a_type: str = 'push' if (a[0] == 0.0) else 'grasp'
        a_coord: list = [a[1], a[2], a[3]]

        if a_type == 'grasp':
            self.r.grasp(pos = a_coord, rot = 22.5)
        elif a_type == 'push':
            self.r.push(pos = a_coord, rot = 0)

        bg_color_img, bg_depth_img = self.r.get_photo()
        self.state = bg_color_img
        r += 1
        done = (r > 2)

        self.round += 1
        return self.state, r, done, info

    
    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, Tuple[ObsType, dict]]:
        """ Restart scene, add blocks, move arm to top position """
        self.r = Robot()
        self.r.create_empty_helpers()
        self.r.connect_and_restart()
        #self.r.add_objects(5)

        # 3 ways to get state:
        #self.state = np.zeros((480, 640, 3), dtype="float32") # random.randint(0, 10)
        #self.state = self.observation_space.sample()
        bg_color_img, bg_depth_img = self.r.get_photo()
        self.state = bg_color_img

        self.round = 0
        EnvReset.run()
        print('Env is resetted. State =', self.state.shape, ' [x200;y200] =', self.state[200][200]) # (480, 640, 3)  [x200;y200] = [45 45 45]
        return self.state # old version: np.ones((1,), dtype="float32")


    def render(self):
        print("=============================================================================")
        print('Round:', self.round, 'Total r:', self.total_r, 'State:', self.state.shape, ' pixel_200_200:', self.state[200][200])
        print("=============================================================================")

if __name__ == '__main__':
    print('hiiii')
    env = Env01()
    done = False
    while not done:
        state = env.reseter(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.steper(action)
        
        
