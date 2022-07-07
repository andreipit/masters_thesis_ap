from net.importer import *

if __name__ == '__main__FLATTENTEST':
    input = torch.randn(32, 1, 5, 5)
    # With default parameters
    m = nn.Flatten()
    output = m(input)
    print(output.size()) # torch.Size([32, 25])
    # With non-default parameters
    m = nn.Flatten(0, 2)
    output = m(input)
    print(output.size()) # 160, 5

if __name__ == '__main__':

    network = nn.Sequential()
    network.add_module('conv', nn.Conv2d(1, 1, kernel_size=(3,3), padding=1)) # 1,1,6,6
    network.add_module('Flatten', nn.Flatten()) # torch.Size([1, 36]) # keeps batch size
    network.add_module('Linear', nn.Linear(in_features = 36, out_features = 4)) #  torch.Size([1, 4])
    # https://discuss.pytorch.org/t/transition-from-conv2d-to-linear-layer-equations/93850
    # https://stackoverflow.com/questions/69778174/runtime-error-mat1-and-mat2-shapes-cannot-be-multiplied-in-pytorch
    
    img = torch.Tensor([
        [3, 0, 1, 2, 7, 4], 
        [1, 5, 8, 9, 3, 1],
        [2, 7, 2, 5, 1, 3],
        [0, 1, 3, 1, 7, 8],
        [4, 2, 1, 6, 2, 8],
        [2, 4, 5, 2, 3, 9]
        ])
    img = torch.unsqueeze(img, 0) # (6, 6) => (1, 6, 6)
    img = torch.unsqueeze(img, 0) # (1, 6, 6) => (1, 1, 6, 6)
    

    output = network(img)
    print('output',output.shape)
    print('output',output)


#network = nn.Sequential()
#network.add_module('conv', nn.Conv2d(1, 1, kernel_size=(3,3), padding=1)) # 1,1,6,6
##network.add_module('conv', nn.Conv2d(1, 1,  kernel_size=(3,3), padding=1)) # 1,1,6,6
##network.add_module('pool', nn.Dropout2d(0.25)) # 1,1,6,6
##network.add_module('conv2', nn.Dropout2d(0.5)) # 1,1,6,6
#network.add_module('Flatten', nn.Flatten()) # torch.Size([1, 36])
#network.add_module('Linear', nn.Linear(in_features = 36, out_features = 4)) #  torch.Size([1, 4])
##network.add_module('Linear', nn.Linear(6, 3))
## https://discuss.pytorch.org/t/transition-from-conv2d-to-linear-layer-equations/93850
## https://stackoverflow.com/questions/69778174/runtime-error-mat1-and-mat2-shapes-cannot-be-multiplied-in-pytorch
    