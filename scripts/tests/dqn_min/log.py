from tests.dqn_min.importer import *

class Logger():
    EPOCHS = 30 #30 # 1000 # each month we lower exploration tradeoff (start more exploitation)
    SESSIONS = 100 #100 # 100 # each day we count our money and maybe losses
    STEPS = 1000 #1000 # 1000 # each order we backprop

    losses:list = [] # each day we clear it
    rewards:float = 0 # each day we clear it
    rewards_grouped_by_day = []
    losses_grouped_by_day = []

    def __init__(self):
        pass

    def update(self, i:int, r:float, loss:float, ex_ex:float) -> float:
        self.losses.append(loss)
        self.rewards += r
        
        # each evening sum all rewards and average losses
        if i % self.STEPS == 0:
            #self.rewards_grouped_by_day.append(np.sum(self.rewards))
            self.rewards_grouped_by_day.append(self.rewards)
            print('day i:', i, ' r:', self.rewards)
            self.rewards = 0
            self.losses_grouped_by_day.append(np.mean(self.losses))
            self.losses = []

        # each month start more exploiting
        if i % (self.SESSIONS * self.STEPS) == 0:
            if ex_ex > 0.01: ex_ex *= (1 - 1e-2) # Lower epsilon => less often we choose random # 
        
        
        # at the end plot all
        #if i % (self.MONTHS * self.DAYS * self.ORDERS) == 0:
        #    self._plot(self.rewards_grouped_by_day, 'rewards per day')
        #    self._plot(self.losses_grouped_by_day, 'losses per day')

        return ex_ex

    def plot_all(self):
        self._plot(self.rewards_grouped_by_day, 'rewards per day')
        self._plot(self.losses_grouped_by_day, 'losses per day')

    def _plot(self, log:list, title:str):
        plt.figure(figsize=[16, 9])
        plt.subplot(2, 2, 2)
        plt.title(title)
        #plt.plot(utils.smoothen(log, 100))
        plt.plot(log)
        plt.grid()
        plt.show()

