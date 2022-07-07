from net.importer import *

# https://pytorch.org/tutorials/recipes/recipes/defining_a_neural_network.html

def set_weights_goodway(myconv, weights):
    with torch.no_grad():
        myconv.weight = nn.Parameter(weights)


def set_weights_bestway(myconv, weights):
    myconv.weight.data.copy_(weights)

    
if __name__ == '__main__':

    myconv = nn.Conv2d(
            in_channels = 1, 
            out_channels = 1, 
            kernel_size = (3, 3),
            stride=1, # if 1 -> we dont skip pixels
            padding=0, # if 1 -> width increases on 2 pixels => keep res if kernel=3x3
            dilation=1, 
            groups=1, 
            bias=True
        )

    weights = torch.Tensor([
        [1, 0, -1], 
        [1, 0, -1], 
        [1, 0, -1]]).unsqueeze(0).unsqueeze(0)
    print('weights', weights)
    weights.requires_grad = True

    set_weights_bestway(myconv, weights)


    network = nn.Sequential()
    network.add_module('conv', myconv)

    #https://discuss.pytorch.org/t/setting-custom-kernel-for-cnn-in-pytorch/27176?u=markroxor
    # https://stackoverflow.com/questions/52790775/setting-custom-kernel-for-cnn-in-pytorch
    # https://www.coursera.org/learn/convolutional-neural-networks/lecture/ctQZz/convolutions-over-volume
    img = torch.Tensor([
        [3, 0, 1, 2, 7, 4], 
        [1, 5, 8, 9, 3, 1],
        [2, 7, 2, 5, 1, 3],
        [0, 1, 3, 1, 7, 8],
        [4, 2, 1, 6, 2, 8],
        [2, 4, 5, 2, 3, 9]
        ])

    ground_truth = torch.Tensor([
        [-5, -4, 0, 8],
        [-10, -2, 2, 3],
        [0, -2, -4, -7],
        [-3, -2, -3, -16],
        ])
    print('ground_truth',ground_truth)
    #img = torch.rand((1, 6, 6))
    img = torch.unsqueeze(img, 0) # (6, 6) => (1, 6, 6)
    img = torch.unsqueeze(img, 0) # (1, 6, 6) => (1, 1, 6, 6)
    print('input:',img)
    output = myconv(img)
    print ('layer output=', output)
    #output= tensor([[[[ -4.9421,  -3.9421,   0.0579,   8.0579],
    #      [ -9.9421,  -1.9421,   2.0579,   3.0579],
    #      [  0.0579,  -1.9421,  -3.9421,  -6.9421],
    #      [ -2.9421,  -1.9421,  -2.9421, -15.9421]]]],
    #   grad_fn=<ThnnConv2DBackward>)

    #output.mean().backward()
    #print(myconv.weight.grad)

    output = network(img)
    print ('net output=', output)
    #output= tensor([[[[ -5.3061,  -4.3061,  -0.3061,   7.6939],
    #      [-10.3061,  -2.3061,   1.6939,   2.6939],
    #      [ -0.3061,  -2.3061,  -4.3061,  -7.3061],
    #      [ -3.3061,  -2.3061,  -3.3061, -16.3061]]]],
    #   grad_fn=<ThnnConv2DBackward>)






    
#class Net(nn.Module):
#    def __init__(self):
#      super(Net, self).__init__()

#      # First 2D convolutional layer, taking in 1 input channel (image),
#      # outputting 32 convolutional features, with a square kernel size of 3
#      self.conv1 = nn.Conv2d(1, 32, 3, 1)
#      # Second 2D convolutional layer, taking in the 32 input layers,
#      # outputting 64 convolutional features, with a square kernel size of 3
#      self.conv2 = nn.Conv2d(32, 64, 3, 1)

#      # Designed to ensure that adjacent pixels are either all 0s or all active
#      # with an input probability
#      self.dropout1 = nn.Dropout2d(0.25)
#      self.dropout2 = nn.Dropout2d(0.5)

#      # First fully connected layer
#      self.fc1 = nn.Linear(9216, 128)
#      # Second fully connected layer that outputs our 10 labels
#      self.fc2 = nn.Linear(128, 10)

#class Net2(nn.Module):
#    def __init__(self):
#        super(Net2, self).__init__()
#        self.conv1 = nn.Conv2d(1, 32, 3, 1)
#        self.conv2 = nn.Conv2d(32, 64, 3, 1)
#        self.dropout1 = nn.Dropout2d(0.25)
#        self.dropout2 = nn.Dropout2d(0.5)
#        self.fc1 = nn.Linear(9216, 128)
#        self.fc2 = nn.Linear(128, 10)

#    # x represents our data
#    def forward(self, x):
#        # Pass data through conv1
#        x = self.conv1(x)
#        # Use the rectified-linear activation function over x
#        x = F.relu(x)

#        x = self.conv2(x)
#        x = F.relu(x)

#        # Run max pooling over x
#        x = F.max_pool2d(x, 2)
#        # Pass data through dropout1
#        x = self.dropout1(x)
#        # Flatten x with start_dim=1
#        x = torch.flatten(x, 1)
#        # Pass data through fc1
#        x = self.fc1(x)
#        x = F.relu(x)
#        x = self.dropout2(x)
#        x = self.fc2(x)

#        # Apply softmax to x
#        output = F.log_softmax(x, dim=1)
#        return output




#if __name__ == '__main__3':
#    network = nn.Sequential()


#    network.add_module('conv', nn.Conv2d(1, 32, 3, 1))
#    network.add_module('conv', nn.Conv2d(32, 64, 3, 1))
#    network.add_module('pool', nn.Dropout2d(0.25))
#    network.add_module('conv2', nn.Dropout2d(0.5))
#    network.add_module('Linear', nn.Linear(9216, 128))
#    network.add_module('Linear', nn.Linear(128, 3))

#    random_data = torch.rand((1, 1, 28, 28))
#    result = network(random_data)
#    print ('result=',result)


#if __name__ == '__main__2':
#    my_nn = Net()
#    print(my_nn)

#    my_nn2 = Net2()
#    print(my_nn2)

#    random_data = torch.rand((1, 1, 28, 28))
#    print('random_data.shape=',random_data.shape)

#    result = my_nn2(random_data)
#    print ('result=',result)
