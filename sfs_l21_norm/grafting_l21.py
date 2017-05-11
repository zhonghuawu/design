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
def sfs_l21_norm(X, Y, threshold):
    print "threshold = %s"%str(threshold)
    X, Y = np.matrix(X), np.matrix(Y)
    X_model = np.ones_like(X[:, 0])
    W = np.ones_like(Y[0,:])
    W, obj_value = update_weight(W, X_model, Y, threshold)

    X_index = np.array(())
    X_index_retained = np.array(())
    obj_values = np.array(())
    epsilon = 1e-3

    n, d = X.shape
    n, c = Y.shape
    for j in range(d):
        x = normalizate(X[:, j])
        if gradient_validation(x, W, X_model, Y, threshold):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            W= np.vstack((W, np.ones(c)))
            W, obj_value = update_weight(W, X_model, Y, threshold)
            W, X_model, X_index_retained = refresh_selected(W, X_model, X_index_retained, epsilon)
            print "***"*30
            print "j = %s obj_value = %s"%(str(j), str(obj_value))
            print "X_index_retained = %s"%str(X_index_retained)
            print "weight matrix: \n%s"%str(W)
            print "***"*30
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
    return X_index_retained, W, X_index, obj_values

def run(fname):
    from util import read_data
    X, Y = read_data(fname, 0)
    print X.shape, Y.shape
    threshold = 0.1
    print "X shape: %s"%str(X.shape)
    X_index_retained, W, X_index, obj_values = sfs_l21_norm(X, Y, threshold)
    
    print "**"*30
    print "selected features index: \n%s\n"%str(X_index_retained)
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

if __name__ == "__main__":
    import sys
    fname = sys.argv[1]
    run(fname)
