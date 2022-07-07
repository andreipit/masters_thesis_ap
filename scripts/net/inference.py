from net.importer import *

def plot(log:list, title:str):
    plt.figure(figsize=[16, 9])
    plt.subplot(2, 2, 2)
    plt.title(title)
    #plt.plot(utils.smoothen(log, 100))
    plt.plot(log)
    plt.grid()
    plt.show()

def start():
    env, NN, NN_frozen, opt, eps_ex_ex = create_env()
    model_path = os.path.join('net', 'logs', 'backup_1500000_r_77.pt')
    
    #torch.save(NN.state_dict(), model_path)
    #print('saved')
    #return

    NN.load_state_dict(torch.load(model_path))
    NN.eval()

    s = env.reset()
    while True:
        a = get_action(s, NN, 0)
        s2, r, done, info = env.step(a)
        env.render()
        s = s2
        if done: 
            time.sleep(1)
            s = env.reset()

if __name__ == '__main__':
    start()