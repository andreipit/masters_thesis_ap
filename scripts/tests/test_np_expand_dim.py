import numpy as np

if __name__ == '__main__':
    x = np.array([[1,2,3,4], [5,6,7,8]])
    print(x)
    print(x.shape)
    x = np.array([x,x,x])
    print(x.shape)
    x = np.swapaxes(x,0,2)
    x = np.swapaxes(x,0,1)
    print(x.shape)
    print(x)
    print('squeeze:')
    x = x[:, :, 0]
    print(x.shape)
    print(x)




