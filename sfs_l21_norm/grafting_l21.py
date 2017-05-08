import numpy as np

from model import *
from util import read_data

def sfs_l21_norm(X, Y, threshold):
    X, Y = np.matrix(X), np.matrix(Y)
    X_model = np.ones_like(X[:, 0])
    W = np.ones_like(Y[0,:])
    InitCount = 0
    epsilon = 1e-3
    X_model = np.hstack((X_model, X[:, :InitCount]))
    W = np.vstack((W, np.ones((InitCount, Y.shape[1]))))
    X_index = np.arange(InitCount)
    W = update_weight(W, X_model, Y, threshold)
    W, X_model, X_index = refresh_selected(W, X_model, X_index, epsilon)

    n, d = X.shape
    n, c = Y.shape
    for j in range(InitCount, d):
        x = normalizate(X[:, j])
        if gradient_validation(x, W, X_model, Y, threshold):
            print "***"*30
            print "j = %s"%str(j)
            X_index = np.hstack((X_index, j))
            X_model = np.hstack((X_model, x))
            W = np.vstack((W, np.ones(c)))
            W = update_weight(W, X_model, Y, threshold)
            print "after update selected features weight"
            print "W = %s"%str(W)
            print "X_index = %s"%str(X_index)
            W, X_model, X_index = refresh_selected(W, X_model, X_index, epsilon)
            print "after refresh selected features:"
            print "W = %s"%str(W)
            print "X_index_retained = %s"%str(X_index)
            print "***"*30
            print 
    return X_index, W

def run(fname):
    X, Y = read_data(fname)
    print X.shape, Y.shape
    threshold = 0.1
    X_index, W = sfs_l21_norm(X, Y, threshold)
    
    print "**"*30
    print "selected features index: %s\n"%str(X_index)
    print "selected features weight: %s\n"%str(W)
    print "**"*30

if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    run(fname)
