import time
import socket
import os
import time

import gym

from utils.server import Server


if __name__ == '__main__':
    s: Server = Server()


    s.connect()

    env = gym.make('environment:env-v1')
    done = False
    while not done:
        state = env.reset(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)

        print('frame', time.time())
        s.validate_connection_loop(1)
        time.sleep(1)



    
