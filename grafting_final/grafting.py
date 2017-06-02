from __future__ import division

from numpy import matrix
import numpy as np

from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

#from model import *
from model_new import *

'''
run grafting algorithm on data set from file fname
X: data matrix, n*d dimension
Y: labels vector, n*1 dimension
w: features weight vector, d*1 dimension
'''

def grafting(X, Y, threshold, epsilon):
    X_model = np.ones_like(X[:, 0])
    w = np.ones(1)
    #w, obj_value = update_wegiht(w, X_model, Y, threshold)

    X_index = np.array([], dtype=int)
    X_index_retained = np.array([], dtype=int)
    obj_values = np.array([], dtype=float)

    n, d = X.shape
    for j in range(d):
        x = normalize(X[:, j])
        #if C_grad_std(x, w, X_model, Y, threshold, epsilon):
        if C_grad(x, w, X_model, Y, threshold, epsilon):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            w = np.hstack((w, 1))
            w, obj_value = update_wegiht(w, X_model, Y, threshold)
            w, X_model, X_index_retained = refresh_selected(w, X_model, X_index_retained, 1e-5)
            print("j = %-6d obj_value = %f"%(j, obj_value))
            print("X_index_retained = %s"%str(X_index_retained))
            print("weight_vector = %s"%str(w))
            print "***"*30
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
    return X_index_retained, w, X_index, obj_values

def run(fname, threshold, epsilon, label_pos):
    print("deal with %s"%fname)
    from util import read_data
    X, Y = read_data(fname, label_pos)
    print("X shape: %s"%str(X.shape))
    results = grafting(np.matrix(X), np.matrix(Y).T, threshold, epsilon)
    X_index_retained, w, X_index, obj_values = results
    
    print(str("**"*30))
    print("dataset name: %s"%fname)
    print("selected features index retained: ")
    print("grafting l1-norm ")
    print("threshold = %s, epsilon = %s: "%(str(threshold), str(epsilon))),
    print("%s"%str(list(X_index_retained)))
    print("selected features weight: %s"%str(w))
    print("selected features index: %s"%str(X_index))
    print("objective function values: %s"%str(obj_values))
    print(str("**"*30))
    print("DONE")

    obj_values_df = DataFrame(obj_values, index=X_index, columns=["obj values"])
    weights_df = DataFrame(w, index=np.hstack((-1, X_index_retained)), columns=["weight"])
    df = pd.concat((obj_values_df, weights_df))
    df.plot(subplots=True)
    plt.show()

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog datafilename [options]')
    opt.add_option('-t', '--threshold', type='float', dest='threshold', help='coefficient of regularization term')
    opt.add_option('-e', '--epsilon', type='float', dest='epsilon', help='scope of sample point')
    opt.add_option('-p', '--label_pos', type='int', dest='label_pos', help='position of label in data set')
    opt.set_defaults(threshold=0.2, epsilon=0.1, label_pos=-1)
    return opt.parse_args(args)[0]

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    args = sys.argv[2:]
    options = get_options(args)
    run(fname, options.threshold, options.epsilon, options.label_pos)
