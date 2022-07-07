from tests.dqn_min.importer import *

def loss_to_f(loss:torch.Tensor) -> float:
    return loss.data.cpu().item()

def start():
    env, NN, NN_frozen, opt, ex_ex, log = create_objects_legacy()
    
    s = env.reset()
    i = 0
    #for j in range(1, log.MONTHS * log.DAYS * log.ORDERS):
    while True:
        i += 1
        a = get_action(s, NN, ex_ex)
        s2, r, done, info = env.step(a)
        #env.render()
        #print('a=', a, 'r=',r)
        opt.zero_grad()
        loss = td_loss([s], [a], [r], [s2], [done], NN, NN_frozen) # => tensor(1.0086, grad_fn=<MeanBackward0>)
        loss.backward()
        opt.step()
        if i % 100 == 0: NN_frozen.load_state_dict(NN.state_dict())
        s = s2
        
        if done: 
            orders_left = i % log.STEPS
            i = i + (log.STEPS - orders_left) # finish day
            #print('reset', 'r=',r, 'i=',i)
            s = env.reset()

        ex_ex = log.update(i, r, loss_to_f(loss), ex_ex) # plot loss and r, averaged by months
        if i >= log.EPOCHS * log.SESSIONS * log.STEPS:
            break

    log.plot_all()

    for i in range(1, log.EPOCHS * log.SESSIONS * log.STEPS):
        a = get_action(s, NN, ex_ex)
        s2, r, done, info = env.step(a)
        env.render()
        s = s2
        if done: 
            s = env.reset()

if __name__ == '__main__':
    start()