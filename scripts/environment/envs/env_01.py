from environment.modules.importer import *
#self.initer, self.steper, self.reseter, self.renderer, self.model = EnvInit(), EnvStep(), EnvReset(), EnvRender(), EnvModel()


class Env01(Env):

    r : Robot = None

    def __init__(self):
        #Server.connect()

        # 2) robot simulation and generate cubes
        

        # maybe later:
        #r.m.cam_pose = r.sim.create_perspcamera_trans_matrix4x4(r.m)
        
        # state (s_t) - rgb-d image 224x224x4 (heightmap representation)
        self.observation_space = Box(low=-1., high=1., shape=(480, 640, 3), dtype="float32")
  
        
        # action (a_t) = (psi, q) | psi E {push,grasp}, q -> p E s_t, where p is pixel, q is 3d coords of p
        # example: (0, 5, 6, 8) => push at Vector3(5,6,8) to right 10sm
        self.action_space = Box(low=-1., high=1., shape=(4,), dtype="float32")

        # reward
        self.collected_reward = -1
        #self.rounds = 3
        print('Env is made')
    
    def step(self, action):
        done = False
        info = {}
        r = 0

        #self.rounds -= 1
        action = (action + 1) * 50 # denormalize action: [-1..1] => [0..100]: -1=>0, 0=>50, 1=>100, -0.5=>(-0.5+1)*50 = 25
        obs = self.state + action
        
        if obs < 50:
            self.collected_reward += -1
            r = -1
        elif obs > 50 and obs < 100:
            self.collected_reward += 0
            r = 0
        else:
            self.collected_reward += 1
            r = 1
            
        if self.rounds == 0:
            done = True
        
        self.renderer(action, r)
        obs = obs/50 - 1 # normalize obs: [0..100] => [-1..1] =>: 0=>-1, 50=>0, 100=>1, 25 = 25/50 - 1 = -0.5
        return obs, self.collected_reward, done, info
    
    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, Tuple[ObsType, dict]]:
        """ Restart scene, add blocks, move arm to top position """
        self.r = Robot()
        self.r.create_empty_helpers()
        self.r.connect_and_restart()
        self.r.add_objects(5)

        #self.state = np.zeros((480, 640, 3), dtype="float32") # random.randint(0, 10)
        #self.state = self.observation_space.sample()
        bg_color_img, bg_depth_img = self.r.get_photo()
        self.state = bg_color_img

        EnvReset.run()
        print('Env is resetted. State =', self.state.shape, ' [x200;y200] =', self.state[200][200]) # (480, 640, 3)  [x200;y200] = [45 45 45]
        return self.state
        #return np.ones((1,), dtype="float32")


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
        
        
