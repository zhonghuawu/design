import scipy.io as sio
import numpy as np

def read_data(fname, label_pos=-1):
    data = sio.loadmat(fname)
    X, Y = None, None
    if 'data' in data.keys():
        data = data['data']
        y = data[:, label_pos]
        X = np.delete(data, label_pos, axis=1)
        #Y = np.ones(y.shape)
        #Y[y==0]=-1
    else :
        X = data['X']
        y = data['Y'][:, 0]
        Y = np.ones(y.shape)
        Y[y==2]=-1
    return X, Y

def read_data_multi(fname, label_pos=-1):
    data = sio.loadmat(fname)
    X, Y = None, None
    if 'data' in data.keys():
        data = data['data']
        Y = data[:, label_pos]
        X = np.delete(data, label_pos, axis=1)
    else :
        X = data['X']
        Y = data['Y'][:, 0]
    return X, Y

def fprime(xk, f, epsilon, *args):
    f0 = f(*((xk,)+args))
    grad = np.zeros((xk.shape), float)
    ei = np.zeros((xk.shape), float)
    for i in range(xk.shape[0]):
        for j in range(xk.shape[1]):
            ei[i, j] = 1.0
            d = np.multiply(epsilon, ei)
            grad[i, j] = (f(*((xk+d,)+args))-f0)/d[i, j]
            ei[i, j] = 0.0
    return grad

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    X, Y = read_data(fname)
    print X, type(X)
    print Y, type(Y)
    print 'DONE'
