from __future__ import division

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import math
import os

'''
grafting algorithm using l1-norm regularied
w is selection vector with d dimension
X is data matrix with n*d dimension
y is labels vector with n dimension
here,
n is number of samples
d is number of features
'''
import model
import refresh

def grafting(y, X, threshold, RetainCount):
    [n, d] = X.shape
    # first step, retain previous RetainCount features
    # and update weight
    X = np.matrix(X)
    y = np.matrix(y)
    X_index = np.arange(RetainCount)
    X_model = np.ones_like(X[:, 0])
    X_model = np.hstack((X_model, X[:, :RetainCount]))
    w = np.ones(RetainCount+1)
    w = model.update_weight_by_bfgs(w, X_model, y, threshold)
    w, X_index, X_model = refresh.refresh_selected(w, X_index, X_model, RetainCount)
    # second step, gradient validation for coming feature one by one 
    # if return one, update weight, and refresh selected feature set
    results = pd.Series(np.zeros(d), np.arange(d))
    for i in range(RetainCount, d):
        x = model.normalizate(X[:, i])
        #print "i = %d, "%i,
        if model.C_grad_Logistic(x, w, X_model, y, threshold):
            print "i = %d"%i
            X_index = np.hstack((X_index, i))
            X_model = np.hstack((X_model, x))
            w = np.hstack((w, 1))
            # update selection vector, features weight vector
            w = model.update_weight_by_bfgs(w, X_model, y, threshold)
            # refresh selected features
            w, X_index, X_model = refresh.refresh_selected(w, X_index, X_model, RetainCount)
            results[i] = model.C(w, X_model, y, threshold)
    return w, X_index, results

def run_grafting(fr_n):
    # fr_n = r"/home/huaa/workspace/datas/gene_expr/DLBCL-Stanford/DLBCL-Stanford.mat"
    print fr_n
    import scipy.io as sio
    data = sio.loadmat(fr_n)['data']
    X = np.matrix(data[:, :-1])
    y = np.matrix(data[:, -1]).T
    y[y==0]==-1
    print X.shape, y.shape

    hreshold=0.1
    RetainCount = 20
    w, X_index, results = grafting(y, X, threshold, RetainCount)

    print w
    print X_index
    print results

    import matplotlib.pyplot as plt
    results.plot()
    plt.show()

if __name__ == "__main__":
    threshold = 0.1
    import sys
    fr_n = sys.argv[1]
    run_grafting(fr_n)
    print "Done!"
