from net.importer import *

def plot(log:list, title:str):
    plt.figure(figsize=[16, 9])
    plt.subplot(2, 2, 2)
    plt.title(title)
    #plt.plot(utils.smoothen(log, 100))
    plt.plot(log)
    plt.grid()
    plt.show()
