import numpy as np
import matplotlib.pyplot as plt

from model import *

'''
streaming features selection regularized by l21-norm
X: data matrix, n*d dimension
Y: label matrix, n*c dimension
W: selection matrix, d*c
threshold: scalar, 0.1-0.5 empirical value
here,
n is number of samples
d is number of features
c is categories of labels
'''
def sfs_l21_norm(X, Y, threshold, epsilon):
    print "threshold = %s"%str(threshold)
    X, Y = np.matrix(X), np.matrix(Y)
    X_model = np.ones_like(X[:, 0])
    W = np.ones_like(Y[0,:])
    W, obj_value = update_weight(W, X_model, Y, threshold)

    X_index = np.array((), dtype=int)
    X_index_retained = np.array((), dtype=int)
    obj_values = np.array((), dtype=float)

    n, d = X.shape
    n, c = Y.shape
    for j in range(d):
        x = normalizate(X[:, j])
        if gradient_validation(x, W, X_model, Y, threshold, epsilon):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            W= np.vstack((W, np.ones(c)))
            W, obj_value = update_weight(W, X_model, Y, threshold)
            W, X_model, X_index_retained = refresh_selected(W, X_model, X_index_retained)
            print "***"*30
            print "j = %s obj_value = %s"%(str(j), str(obj_value))
            print "X_index_retained = %s"%str(X_index_retained)
            print "weight matrix: \n%s"%str(W)
            print "***"*30
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
    return X_index_retained, W, X_index, obj_values

def run(fname, epsilon, threshold, label_pos):
    from util import read_data
    X, Y = read_data(fname, label_pos)
    print X.shape, Y.shape
    print "X shape: %s"%str(X.shape)
    X_index_retained, W, X_index, obj_values = sfs_l21_norm(X, Y, threshold, epsilon)
    
    print "**"*30
    print "epsilon = %s, threshold = %s"%(str(epsilon), str(threshold))
    print "selected features index: \n%s\n"%str(list(X_index_retained))
    print "selected features weight: \n%s\n"%str(W)
    print "features index that through the gradient validation: \n%s\n"%str(X_index)
    print "**"*30
    print "DONE"

    obj_values_df = pd.DataFrame(obj_values, index=X_index, columns=["obj_values"])
    columns = ["weight_%d"%i for i in range(Y.shape[1])]
    weights_df = pd.DataFrame(W, index=np.hstack((-1, X_index_retained)), columns=columns)
    df = pd.concat((obj_values_df, weights_df))
    df.plot(subplots=True)
    plt.show()

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog data_file(.mat) [options]')
    opt.add_option('-t', '--threshold', action='store', type='float', dest='threshold', help='coefficient of regularization term')
    opt.add_option('-e', '--epsilon', action='store', type='float', dest='epsilon', help='value of sample point')
    opt.add_option('-p', '--label_pos', action='store', type='int', dest='label_pos', help='label pos in data set')
    opt.set_defaults(threshold=0.01, epsilon=0.05, label_pos=-1)
    return opt.parse_args(args)

if __name__ == "__main__":
    import sys
    args = sys.argv[1:]
    fname = args[0]
    options, args= get_options(args[1:])
    run(fname, options.epsilon, options.threshold, options.label_pos)
