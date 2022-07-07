from net.importer import *

def create_network() -> nn.Module:
    network = nn.Sequential()
    network.add_module('linear1', nn.Linear(4, 64))
    network.add_module('relu1', nn.ReLU())
    network.add_module('linear2', nn.Linear(64, 64))
    network.add_module('relu2', nn.ReLU())
    network.add_module('prediction', nn.Linear(64, 2))
    return network


#class Network():
#    network = None

#    def __init__(self):
#        self.network = nn.Sequential()
#        self.network.add_module('linear1', nn.Linear(4, 64))
#        self.network.add_module('relu1', nn.ReLU())
#        self.network.add_module('linear2', nn.Linear(64, 64))
#        self.network.add_module('relu2', nn.ReLU())
#        self.network.add_module('prediction', nn.Linear(64, 2))


