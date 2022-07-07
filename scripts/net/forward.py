from net.importer import *


def get_action(state, network, epsilon=0):
    """
    Lower epsilon => less often we choose random
    sample actions with epsilon-greedy policy
    recap: with p = epsilon pick random action, else pick action with highest Q(s,a)
    """
    state = torch.tensor(state[None], device=device, dtype=torch.float32)
    
    print('fwd input shape:',state.shape)
    #q_values = network(state).detach() # 2 qvalues for L and R: #==> q_values [[-0.16288276  0.15193802]] 
    q_values = network(state[None,...]).detach() # 2 qvalues for L and R: #==> q_values [[-0.16288276  0.15193802]] 
    
    # .numpy()
    n_actions = len(q_values[0])

    if np.random.random() < epsilon:
        chosen_action = np.random.choice(n_actions)
    else:
        chosen_action = np.argmax(q_values[0].cpu().numpy()) # q_values[0] [-0.16288276  0.15193802]

    return int(chosen_action)

