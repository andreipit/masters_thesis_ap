from utils.imports.entry_point_import import *
from net.importer import *
EPOCHS = 30 #30 # 1000 # each month we lower exploration tradeoff (start more exploitation)
SESSIONS = 100 #100 # 100 # each day we count our money and maybe losses
STEPS = 1000 #1000 # 1000 # each order we backprop



def create_env():
    env = Env01() #gym.make("CartPole-v1") #env = gym.make('environment:env-v1')
    NN = create_network().to(device)
    NN_frozen = create_network().to(device) #DQNAgent(NN.state_shape, NN.n_actions, epsilon=0.5).to(device)
    NN_frozen.load_state_dict(NN.state_dict())
    opt = torch.optim.Adam(NN.parameters(), lr=1e-4)
    ex_ex = 0.5
    return env, NN, NN_frozen, opt, ex_ex


if __name__ == '__main__':

    env, NN, NN_frozen, opt, eps_ex_ex = create_env()
    r_session = 0   # accumulate r from all steps inside one session
    r_sessions = [] # save all sessions rewards inside one epoch
    r_epochs = []   # it is NOT sessions sum! It is mean! Epoch reward = mean of all his sessions
    i = 0

    s = env.reset()

    while True:
        i += 1
        a = get_action(s, NN, eps_ex_ex)
        s2, r, done, info = env.step(a)
        r_session += r
        opt.zero_grad()
        loss = td_loss_double_dqn([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
        loss.backward()
        opt.step()
        s = s2
        if done: # done means object is grasped => session end
            i = i + (STEPS - i % STEPS) # finish session # 150 + (1000 - 150%1000) = 1000; 2150 + (1000 - 2150%1000) = 3000
            r_sessions.append(r_session)
            r_session = 0
            s = env.reset()


