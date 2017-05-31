from __future__ import division

from pandas import DataFrame, Series
import pandas as pd
import numpy as np
import math
import functools

import os

from scipy import optimize

def normalizate(x):
    x = np.array(x)
    ave = x.mean()
    xigma = x.std()
    return (x-ave)/xigma

def f(w, x):
    return np.dot(np.array(w), np.array(x))

def C(W, X_model, y, threshold):
    n, d = X_model.shape
    res1 = 0
    for i in range(n):
        res1+=math.log(1+math.exp(-y[i]*f(W, X_model[i])))
    res1 = res1/n
    res2 = 0
    for i in range(W.size):
        res2+=abs(W[i])
    res2 = res2*threshold
    return res1 + res2

def C_grad(W, X_model, y, x):
    n, d = X_model.shape
    result = 0
    for i in range(n):
        result+=(-y[i])/(1+math.exp(y[i]*f(W, X_model[i])))*x[i]
    return result/n

def grafting(y, X, threshold):
    n, d = X.shape
    X_model = np.ones_like(X[:, 0])
    X_index = []
    results = []
    w = np.zeros(1)

    from numpy.random import random_sample
    for i in range(d):
        x = normalizate(X[:, i])
        sample_points = random_sample(10)
        for point in sample_points:
            w_new = np.hstack((w, point))
            grad = C_grad(w_new, X_model, y, x)
            if abs(grad)>threshold:
                print "i = %d, grad = %f"%(i, grad)
                X_index.append(i)
                X_model = np.hstack((X_model, x))
                w = np.hstack((w, 1))
                F = functools.partial(C, X_model=X_model, y=y, threshold=threshold)
                W=optimize.fmin_cg(F, W)
                result = C(W, X_model, y, threshold)
                results.append(result)
                print "**"*20,
                print result
    return X_index, w, results 

    
def grafting_old(y, X, threshold=0.1):
    n, d = X.shape
    X_model = np.ones_like(X[:, 0])
    x_index = []
    result_C = []
    W=np.zeros(1)

    for i in range(d):
        x = normalizate(X[:, i])
        grad = C_grad(W, X_model, y, x)
        if(abs(grad) > threshold):
            print "i = %d, grad = %f"%(i, grad)
            x_index.append(i)
            #X_model = np.c_[X_model, x]
            #W = np.r_[W, 1]
            X_model = np.hstack((X_model, x))
            W = np.hstack((W, 1))
            F = functools.partial(C, X_model=X_model, y=y, threshold=threshold)
            W=optimize.fmin_cg(F, W)
            result = C(W, X_model, y, threshold)
            result_C.append(result)
            print "**"*20,
            print result
    return x_index, W, result_C

def grafting_ColonTumor():
    import scipy.io as sio
    fr_n = r"/home/huaa/workspace/datas/gene_expr/ColonTumor/colonTumor.mat"
    data = sio.loadmat(fr_n)['data']
    X = data[:, :-1]
    y = data[:, -1]
    y[y==0]=-1

    threshold=0.1

    index, W, results = grafting(y, X, threshold)
    print "index = ",index 
    print "results = ", results
    print "W = ",W
    print "Done!"
    import matplotlib.pyplot as plt
    from pandas import Series
    s = Series(results, index=index)
    s.plot()
    plt.show()

if __name__ == "__main__":
    grafting_ColonTumor()
