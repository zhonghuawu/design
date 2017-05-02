import scipy.io as sio

def read_data(fname):
    data = sio.loadmat(fname)['data']
    X = data[:, :-1]
    Y = data[:, -1]
    Y[Y==0]=-1
    return X, Y

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    X, Y = read_data(fname)
    print X, type(X)
    print Y, type(Y)
    print 'DONE'
