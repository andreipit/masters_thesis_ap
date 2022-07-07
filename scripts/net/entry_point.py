from net.importer import *

class Network():
    def __init__(self):
        pass

EPOCHS = 30 #30 # 1000 # each month we lower exploration tradeoff (start more exploitation)
SESSIONS = 100 #100 # 100 # each day we count our money and maybe losses
STEPS = 1000 #1000 # 1000 # each order we backprop


def start():
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
        #loss = td_loss([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
        loss = td_loss_double_dqn([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
        loss.backward()
        opt.step()
        s = s2
        if done: # dones means 'pole has fallen' => session end, ie done is bad
            i = i + (STEPS - i % STEPS) # finish session # 150 + (1000 - 150%1000) = 1000; 2150 + (1000 - 2150%1000) = 3000
            r_sessions.append(r_session)
            r_session = 0
            s = env.reset()

        if i % 100 == 0: # after 100 steps - NN snapshot
            NN_frozen.load_state_dict(NN.state_dict())
        if i % (SESSIONS * STEPS) == 0: # after ONE epoch
            eps_ex_ex = eps_ex_ex * (1 - 1e-2) if eps_ex_ex > 0.01 else eps_ex_ex
            print('i:', i, 'epoch r:', np.mean(r_sessions), 'eps_ex_ex:', eps_ex_ex)
            torch.save(NN.state_dict(), os.path.join('net', 'logs', 'saved_model_' + str(i) + '_r_' + str(int(np.mean(r_sessions))) +'.pt'))
            r_epochs.append(np.mean(r_sessions))
            r_sessions = []
        if i >= EPOCHS * SESSIONS * STEPS: # after ALL epochs
            break

    #plot(r_epochs, 'reward epochs')

if __name__ == '__main__':
    start()