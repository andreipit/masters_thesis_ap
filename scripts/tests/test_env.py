
from gym import Env
from gym.spaces import Box, Discrete
import random
import numpy as np
from typing import Optional, Tuple, Union, TypeVar
ObsType = TypeVar("ObsType")


from utils.env.init import EnvInit
from utils.env.step import EnvStep
from utils.env.reset import EnvReset
from utils.env.render import EnvRender

class Env01(Env):

    #server: Server = None

    init: EnvInit = None

    def __init__(self):
        self.init = EnvInit()

        self.observation_space = Box(low=-1, high=1, shape=(1,), dtype="float32")
        self.action_space = Box(low=-1, high=1, shape=(1,), dtype="float32")
        self.state = random.randint(0, 10)
        self.rounds = 3
        self.collected_reward = -1
    
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
        
        self.render(action, rw)
        obs = obs/50 - 1 # normalize obs: [0..100] => [-1..1] =>: 0=>-1, 50=>0, 100=>1, 25 = 25/50 - 1 = -0.5
        return obs, self.collected_reward, done, info
    
    def reset(self, seed: Optional[int] = None, return_info: bool = False, options: Optional[dict] = None) -> Union[ObsType, Tuple[ObsType, dict]]:
        self.state = 0
        return np.ones((1,), dtype=np.float32)

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
        state = env.reset(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
        
        
