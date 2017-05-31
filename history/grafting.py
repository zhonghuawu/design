from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
import numpy as np
import math
import functools
import os

from scipy import optimize

'''
grafting algorithm using l1-norm regularied
w is selection vector with d dimension
X is data matrix with n*d dimension
y is labels vector with n dimension
here,
n is number of samples
d is number of features
'''

def normalizate(X):
    X = np.array(X)
    mean = X.mean()
    xigma = X.std()
    return (X-mean)/xigma

def f(w, x):
    return np.dot(np.matrix(w), np.matrix(x).T)[0, 0]

def C(w, X, y, threshold):
    n, d = X.shape
    res1 = 0
    for i in range(n):
        res1 += math.log(1+math.exp(-y[i]*f(w, X[i, :])))
    res1 = res1/n
    res2 = 0
    for i in range(d):
        res2 += abs(w[i])
    res2 = res2*threshold
    return res1+res2

def C_std(w, X, y, threshold):
    n = X.shape[0]
    res = 0
    for i in range(n):
        res += math.log(1+math.exp(-y[i]*f(w, X[i, :])))
    res = res/n + threshold*np.linalg.norm(w, 1)
    return res

def Loss_grad(x, w, X, y):
    X_new = np.hstack((X, x))
    n = X.shape[0]
    res = 0
    for i in range(n):
        res -= y[i]/(1+math.exp(y[i]*f(w, X_new[i, :])))*x[i]
    return res/n

def C_grad_std(x, w, X, y, threshold):
    from numpy.random import random_sample
    sample_point_number = 10
    sample_points = random_sample(sample_point_number)*2-1
    k_count = 0
    for point in sample_points:
        w_new = np.hstack((w, point))
        if abs(Loss_grad(x, w_new, X, y))>threshold:
            return True
    return False

def refresh_selected(w, X_model, RetainCount, X_index):
    from pandas import Series, DataFrame
    X_zero = X_model[:, 0]
    w_zero = w[0]
    X_dataframe = DataFrame(X_model[:, 1:].transpose(), index=X_index)
    w_series = Series(w[1:], index=X_index)
    w_series = w_series.sort_values(ascending=False)[:RetainCount]
    X_index_new = list(w_series.index)
    X_model_new = X_dataframe.ix[X_index_new].get_values().transpose()
    X_model_new = np.hstack((X_zero, X_model_new))
    w_new = w_series.get_values()
    w_new = np.hstack((w_zero, w_new))
    return w_new, X_model_new, X_index_new

def grafting(y, X, threshold, RetainCount):
    X = np.matrix(X)
    [n, d] = X.shape
    X_index = [i for i in range(RetainCount)]
    X_model = np.matrix(np.ones_like(X[:, 0]))
    X_model = np.matrix(np.hstack((X_model, X[:, :RetainCount])))
    w = np.ones(RetainCount+1)
    f = functools.partial(C, X=X_model, y=y, threshold=threshold)
    from scipy import optimize
    w = optimize.fmin_cg(f, w)
    results = []
    for i in range(RetainCount, d):
        x = normalizate(X[:, i])
        if C_grad_std(x, w, X_model, y, threshold):
            print "i = %d"%i
            X_index.append(i)
            X_model = np.hstack((X_model, x))
            w = np.hstack((w, 1))
            f = functools.partial(C, X=X_model, y=y, threshold=threshold)
            w = optimize.fmin_cg(f, w)
            w, X_model, X_index = refresh_selected(w, X_model, RetainCount, X_index)
            result = C_std(w, X_model, y, threshold)
            results.append(result)
    return w, X_index, results

def grafting_ColonTumor_mat(threshold=0.1):
    fr_n = r"/home/huaa/workspace/datas/gene_expr/DLBCL-Stanford/DLBCL-Stanford.mat"
    import scipy.io as sio
    data = sio.loadmat(fr_n)['data']
    X = data[:, :-1]
    y = data[:, -1]
    y[y==0]==-1
    print X.shape, y.shape
    RetainCount = 30
    w, X_index, results = grafting(y, X, threshold, RetainCount)
    print w
    print X_index
    print results
    print "Done!"

    import matplotlib.pyplot as plt
    s = pd.Series(results, index=X_index)
    s.plot()
    plt.show()

if __name__ == "__main__":
    grafting_ColonTumor_mat(0.1)
