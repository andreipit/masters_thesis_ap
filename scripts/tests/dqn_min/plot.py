from tests.dqn_min.importer import *

def plot_loss(td_loss_history):
    
    plt.figure(figsize=[16, 9])
    plt.subplot(2, 2, 2)
    plt.title("TD loss history (smoothened)")
    #plt.plot(utils.smoothen(td_loss_history, 1000))
    plt.plot(td_loss_history)
    plt.grid()
    plt.show()

