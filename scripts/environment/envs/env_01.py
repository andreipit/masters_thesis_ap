from environment.modules.importer import *
#self.initer, self.steper, self.reseter, self.renderer, self.model = EnvInit(), EnvStep(), EnvReset(), EnvRender(), EnvModel()


class Env01(Env):

    r : Robot = None

    def __init__(self):
        Server.connect()

        # 2) robot simulation and generate cubes
        r: Robot = Robot()
        r.create_empty_helpers()
        r.connect()
        r.add_objects()
        # maybe later:
        #r.m.cam_pose = r.sim.create_perspcamera_trans_matrix4x4(r.m)
        #r.m.bg_color_img, self.m.bg_depth_img = r.sim.get_2_perspcamera_photos_480x640(self.m)
        
        
        # state (s_t) - rgb-d image 224x224x4 (heightmap representation)
        self.observation_space = Box(low=-1., high=1., shape=(2, 2), dtype="float32")
        #self.state = np.zeros((2,2), dtype="float32") # random.randint(0, 10)
        self.state = self.observation_space.sample()
        
        # action (a_t) = (psi, q) | psi E {push,grasp}, q -> p E s_t, where p is pixel, q is 3d coords of p
        # example: (0, 5, 6, 8) => push at Vector3(5,6,8) to right 10sm
        self.action_space = Box(low=-1., high=1., shape=(4,), dtype="float32")

        # reward
        self.collected_reward = -1
        #self.rounds = 3
        print('Env is made. State =', self.state)
    
    def step(self, action):
        done = False
        info = {}
        rw = 0
        self.rounds -= 1
        action = (action + 1) * 50 # denormalize action: [-1..1] => [0..100]: -1=>0, 0=>50, 1=>100, -0.5=>(-0.5+1)*50 = 25
        obs = self.state + action
        
        if obs < 50:
            self.collected_reward += -1
            rw = -1
        elif obs > 50 and obs < 100:
            self.collected_reward += 0
            rw = 0
        else:
            self.collected_reward += 1
            rw = 1
            
        if self.rounds == 0:
            done = True
        
        self.renderer(action, rw)
        obs = obs/50 - 1 # normalize obs: [0..100] => [-1..1] =>: 0=>-1, 50=>0, 100=>1, 25 = 25/50 - 1 = -0.5
        return obs, self.collected_reward, done, info
    
    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, Tuple[ObsType, dict]]:
        self.reseter.run()
        self.state = 0
        return np.ones((1,), dtype="float32")

    def render(self, action, rw):
        print("=============================================================================")
        print(f"v1new: Round : {self.rounds}\nDistance Travelled : {action[0]}\nReward Received: {rw}")
        print(f"Total Reward : {self.collected_reward}")
        print("=============================================================================")

if __name__ == '__main__':
    print('hiiii')
    env = Env01()
    done = False
    while not done:
        state = env.reseter(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.steper(action)
        
        
