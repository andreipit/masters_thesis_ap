from net.importer import *


def create_network_224x224_to_224x224() -> nn.Module:
    from collections import OrderedDict
  
    network = nn.Sequential()
    network.add_module('conv', nn.Conv2d(in_channels=1, out_channels=1, kernel_size=3, padding=1))
    #image_h = 224
    #image_w = 224


    #network = nn.Sequential()
    #network.add_module('conv', nn.Conv2d(1, 6, 5))
    #network.add_module('pool', nn.MaxPool2d(2, 2))
    #network.add_module('conv2', nn.Conv2d(6, 16, 5))
    #network.add_module('Linear', nn.Linear(16 * image_h * image_w, 120))
    #network.add_module('Linear', nn.Linear(120, 84))
    #network.add_module('Linear', nn.Linear(84, 10))

    #network = nn.Sequential(OrderedDict([
    #    ('grasp-norm0', nn.BatchNorm2d(3072)),
    #    ('grasp-relu0', nn.ReLU(inplace=True)),
    #    ('grasp-conv0', nn.Conv2d(3072, 64, kernel_size=1, stride=1, bias=False)),
    #    ('grasp-norm1', nn.BatchNorm2d(64)),
    #    ('grasp-relu1', nn.ReLU(inplace=True)),
    #    ('grasp-conv1', nn.Conv2d(64, 1, kernel_size=1, stride=1, bias=False))
    #]))

    #network = nn.Sequential()
    #network.add_module('conv2d', nn.Conv2d(in_channels=1, out_channels=224, kernel_size=1))


    #network = nn.Sequential()
    #network.add_module('conv3d', nn.Conv2d(in_channels=1, out_channels=1, kernel_size=1))
    #network.add_module('linear1', nn.Linear(in_features=(224, 224), out_features=64))
    ##network.add_module('linear1', nn.Linear(4, 64))
    #network.add_module('relu1', nn.ReLU())
    ##network.add_module('linear2', nn.Linear(64, 64))
    #network.add_module('linear2', nn.Linear(64, 64, 64))
    #network.add_module('relu2', nn.ReLU())
    ##network.add_module('prediction', nn.Linear(64, 2))
    #network.add_module('prediction', nn.Linear( 64, (224, 224) ))
    
    return network


def create_network_4_to_2() -> nn.Module:
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


