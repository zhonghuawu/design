import scipy.io as sio
import numpy as np

def read_data(fname, label_pos=-1):
    data = sio.loadmat(fname)['data']
    X = data[:, :label_pos]
    Y = data[:, label_pos]
    Y[Y==0]=-1
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
