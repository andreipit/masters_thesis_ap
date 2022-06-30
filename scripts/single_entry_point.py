import time
import socket
import os
import time
import gym
#from utils.network.server_unity3d import Server
from utils.network.server_coppelia import Server
from environment.envs.env_01 import Env01

if __name__ == '__main__':
    print('hi')
    Server.connect()




if __name__ == '__main__2':
    Server.connect()

    #env = gym.make('environment:env-v1')
    #env = Env01()
    done = False

    #time.sleep(2)
    #state = env.reset(seed = None, return_info = False, options = None)

    while not done:
        time.sleep(0.1)
        #state = env.reset(seed = None, return_info = None, options = None)
        #action = env.action_space.sample()
        #state, reward, done, info = env.step(action)

        #print('frame', time.time())
        Server.check_connection(1)



    
    
