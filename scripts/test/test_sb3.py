if __name__ == '__main__SAC_broken':
    from utils.imports.entry_point_import import *
    #from stable_baselines3 import PPO
    from stable_baselines3.sac.sac import SAC

    env2 = Env01()
    env = gym.make('environment:env-v1') # Env01()
    #env.render()
    
    #model = PPO("MlpPolicy", env, verbose=1)
    #model = SAC("CnnPolicy", env, verbose=1)
    model = SAC("CnnPolicy", env, verbose=1)
    #model.learn(total_timesteps=10_000)
    #model.learn(total_timesteps=10)
    
    obs = env.reset() # # s is ortho image 224x224
    for i in range(100):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
            obs = env.reset()



if __name__ == '__main__':
    from utils.imports.entry_point_import import *
    from stable_baselines3 import PPO

    env = Env01()
    env2 = gym.make('environment:env-v1') # Env01()
    #env.render()
    
    model = PPO("MlpPolicy", env, verbose=1)
    #model.learn(total_timesteps=10_000)
    #model.learn(total_timesteps=5)
    
    obs = env.reset() # # s is ortho image 224x224
    for i in range(100):
        action, _states = model.predict(obs, deterministic=True)
        print('before step')
        obs, reward, done, info = env.step(action)
        print('after step')
        env.render()
        if done:
            obs = env.reset()



if __name__ == '__main__github_example':
    # https://github.com/DLR-RM/stable-baselines3#example
    # pip install stable-baselines3
    # pip install gym[all]
    # ignor errors about mujoco, run and see cartPole
    import gym

    from stable_baselines3 import PPO

    env = gym.make("CartPole-v1")

    model = PPO("MlpPolicy", env, verbose=1)
    model.learn(total_timesteps=10_000)

    obs = env.reset()
    for i in range(1000):
        action, _states = model.predict(obs, deterministic=True)
        obs, reward, done, info = env.step(action)
        env.render()
        if done:
          obs = env.reset()

    env.close()