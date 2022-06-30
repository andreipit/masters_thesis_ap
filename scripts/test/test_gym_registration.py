import gym # cd E:\notes\masters_thesis_ap\scripts, pip install -e .

if __name__ == '__main__':
    print('hiiii')
    env = gym.make('environment:env-v1')
    #env = DogTrain()
    done = False
    while not done:
        #state = env.reset()
        state = env.reset(seed = None, return_info = None, options = None)
        action = env.action_space.sample()
        state, reward, done, info = env.step(action)
