from tests.dqn_min.importer import *

def create_objects():
    env = gym.make("CartPole-v1")
    NN = create_net().to(device)
    NN_frozen = create_net().to(device) #DQNAgent(NN.state_shape, NN.n_actions, epsilon=0.5).to(device)
    NN_frozen.load_state_dict(NN.state_dict())
    opt = torch.optim.Adam(NN.parameters(), lr=1e-4)
    ex_ex = 0.5
    return env, NN, NN_frozen, opt, ex_ex


def create_objects_legacy():
    env = gym.make("CartPole-v1")
    NN = create_net().to(device)
    NN_frozen = create_net().to(device) #DQNAgent(NN.state_shape, NN.n_actions, epsilon=0.5).to(device)
    NN_frozen.load_state_dict(NN.state_dict())
    opt = torch.optim.Adam(NN.parameters(), lr=1e-4)
    ex_ex = 0.5
    log = Logger()
    return env, NN, NN_frozen, opt, ex_ex, log


