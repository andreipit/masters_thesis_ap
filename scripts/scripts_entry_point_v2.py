from utils.imports.entry_point_import import *
from net.importer import *
EPOCHS = 30 #30 # 1000 # each month we lower exploration tradeoff (start more exploitation)
SESSIONS = 100 #100 # 100 # each day we count our money and maybe losses
STEPS = 1000 #1000 # 1000 # each order we backprop


def link_to_env():
    env222 = Env01() #gym.make("CartPole-v1") #env = gym.make('environment:env-v1')


def create_push_grasp_env():
    #env = gym.make("CartPole-v1") #env = gym.make('environment:env-v1')
    env = gym.make('environment:env-v1')
    NN = create_network_224x224_to_224x224().to(device)
    NN_frozen = create_network_224x224_to_224x224().to(device) #DQNAgent(NN.state_shape, NN.n_actions, epsilon=0.5).to(device)
    NN_frozen.load_state_dict(NN.state_dict())
    opt = torch.optim.Adam(NN.parameters(), lr=1e-4)
    ex_ex = 0.5
    return env, NN, NN_frozen, opt, ex_ex


def convert_state_to_nn_input(c, d):

    d = Reshaper().remove_3_depth_channels(d)
    c, d = Reshaper().scale_224x224_to_640x480(c, d)
    c, d = Reshaper().add_padding_keep_shape(c, d)
    c, d = Reshaper().scale_and_normalize(c, d) # -> Tuple[NDArray["640, 640, 3", float], NDArray["640, 640, 3", float]]:
    c, d = Reshaper().reshape_to_minibatch_1_3_640_640(c, d) #  -> Tuple[NDArray["1, 3, 640, 640", float], NDArray["1, 3, 640, 640", float]]:
    color_heightmap = c
    depth_heightmap = d
    return c, d


def test():
    env, NN, NN_frozen, opt, eps_ex_ex = create_push_grasp_env()
    r_session = 0   # accumulate r from all steps inside one session
    r_sessions = [] # save all sessions rewards inside one epoch
    r_epochs = []   # it is NOT sessions sum! It is mean! Epoch reward = mean of all his sessions
    s = env.reset()  # => s = np.array (224, 224) float64
    
    c_batch, d_batch = convert_state_to_nn_input(s[0], s[1])
    
    
    print('c_batch.shape ', c_batch.shape) # [1, 3, 640, 640]
    print('d_batch.shape ', d_batch.shape) # [1, 3, 640, 640]
    
    
    c_batch_640_640_3 = Reshaper().cwh_to_whc( c_batch[0] )
    print('c_batch_640_640_3',c_batch_640_640_3.shape)
    d_batch_640_640_3 = Reshaper().cwh_to_whc( d_batch[0] )
    print('d_batch_640_640_3',d_batch_640_640_3.shape)

    plt.imshow(c_batch_640_640_3); plt.show(block=True)
    plt.imshow(d_batch_640_640_3); plt.show(block=True)
    #plt.imshow(d_batch[0]); plt.show(block=True)


    #output_prob, state_feat = m.model.forward(input_color_data, input_depth_data, is_volatile, specific_rotation)


    #flatten = nn.Flatten()
    #s = flatten(s)

    #a = get_action(s, NN, eps_ex_ex)
    #print('a', a)
    #plt.imshow(a); plt.show(block=True)



if __name__ == '__main__':
    test()



#def start():
    
#    env, NN, NN_frozen, opt, eps_ex_ex = create_env()
#    r_session = 0   # accumulate r from all steps inside one session
#    r_sessions = [] # save all sessions rewards inside one epoch
#    r_epochs = []   # it is NOT sessions sum! It is mean! Epoch reward = mean of all his sessions
#    i = 0


#    s = env.reset()
#    while True:
#        i += 1
#        a = get_action(s, NN, eps_ex_ex)
#        s2, r, done, info = env.step(a)
#        r_session += r
#        opt.zero_grad()
#        loss = td_loss_double_dqn([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
#        loss.backward()
#        opt.step()
#        s = s2
#        if done: # done means object is grasped => session end
#            i = i + (STEPS - i % STEPS) # finish session # 150 + (1000 - 150%1000) = 1000; 2150 + (1000 - 2150%1000) = 3000
#            r_sessions.append(r_session)
#            r_session = 0
#            s = env.reset()



#def convert_state_to_nn_input(d):
#    d = ReshaperDepth.scale_224x224_to_640x480(d)
#    d = ReshaperDepth().add_padding_keep_shape(d)
#    d = ReshaperDepth().scale_and_normalize(d) # -> NDArray["640, 640, 3", float]:
#    d = ReshaperDepth().reshape_to_minibatch_1_3_640_640(d) #  -> Tuple[NDArray["1, 3, 640, 640", float], NDArray["1, 3, 640, 640", float]]:
#    return d
