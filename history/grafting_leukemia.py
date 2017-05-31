from __future__ import division
import pandas as pd
from pandas import DataFrame, Series
import numpy
import math
import functools
import os

from scipy import optimize

def normalizate(X):
    X = numpy.array(X)
    ave = X.mean()
    xigma = X.std()
    return (X-ave)/xigma

def f(w, x):
    res = numpy.dot(numpy.array(w), numpy.array(x))
    return res

def C(W, X_model, y, m, lamda=0.1):
    res1 = 0
    for i in range(m):
        res1+=math.log(1+math.exp(-y[i]*f(W, X_model[i])))
    res1 = res1/m
    res2 = 0
    for i in range(W.size):
        res2+=abs(W[i])
    res2 = res2*lamda
    return res1 + res2

def C_grad(W, X_model, y, m, x):
    result = 0
    for i in range(m):
        result+=(-y[i])/(1+math.exp(y[i]*f(W, X_model[i])))*x[i]
    return result/m

def grafting(y, X, threshold=0.1):
    X_model = numpy.ones_like(X[0])
    m = numpy.array(y).size
    x_index = []
    result_C = []
    W=numpy.zeros(1)
    i = 0
    for x in X:
        x = normalizate(x)
        grad = C_grad(W, X_model, y, m, x)
        if(abs(grad) > threshold):
            print "i = %d, grad = %f"%(i, grad)
            x_index.append(i)
            X_model = numpy.c_[X_model, x]
            W = numpy.r_[W, 1]
            F = functools.partial(C, X_model=X_model, y=y, m=m, lamda=threshold)
            #F_d = functools.partial(C_grad, X_model=X_model, y=y, m=m, x=x)
            W=optimize.fmin_cg(F, W)
            result = C(W, X_model, y, m, threshold)
            result_C.append(result)
            print "**"*20,
            print result
        i+=1
    return x_index, W, result_C

def grafting_DLBCL(threshold=0.1):
    fr_n = r"/home/huaa/workspace/datas/gene_expr/ColonTumor/colonTumor.data"
    datas = pd.read_csv(fr_n, sep=',', header=None)
    n_features = len(datas.columns)
    yy = datas[n_features-1]
    y = [-1 if i==yy[0] else 1 for i in yy]
    X = datas.drop(n_features-1, axis=1).get_values()
    X, y = numpy.array(X).transpose(), numpy.array(y)
    print X.shape, y.shape
    index, W, result_C = grafting(y, X, threshold)
    print "index = ",index 
    print "result_C = ", result_C
    print "W = ",W
    print "Done!"
    import matplotlib.pyplot as plt
    from pandas import Series
    s = Series(result_C, index=index)
    s.plot()
    plt.show()

def grafting_arcene(threshold):
    path = r"~/workspace/datas/ArceneDataset/Arcene"
    datasfilename = os.path.join(path, "arcene_train.data")
    labelsfilename = os.path.join(path, "arcene_train.labels")
    datas = pd.read_csv(datasfilename, sep=' ', header=None)
    X = numpy.array(datas.get_values()).transpose()
    labels = pd.read_csv(labelsfilename, sep=' ', header=None, squeeze=True)
    y = numpy.array(labels.get_values())
    index, W = grafting(y, X, threshold)
    print index 
    print W 
    print 'Done'

def grafting_leukemia(threshold):
    fr_n = r"~/workspace/datas/gene_expr/Leukemia/AMLALL_train.data"
    datas = pd.read_csv(fr_n, sep=',', header=None)
    n_features = len(datas.columns)
    yy = datas[n_features-1]
    X = datas.drop(n_features-1, axis=1).get_values()
    y = [0 if i==yy[0] else 1 for i in yy]
    X, y = numpy.array(X).transpose(), numpy.array(y)
    print X.shape, y.shape
    index, W, result_C = grafting(y, X, threshold)
    print "index = ",index 
    print "result_C = ", result_C
    print "W = ",W
    print "Done!"
    import matplotlib.pyplot as plt
    from pandas import Series
    s = Series(result_C, index=index)
    s.plot()
    plt.show()

if __name__ == "__main__":
    #grafting_arcene(0.2)
    grafting_DLBCL(0.1)
    #grafting_leukemia(0.1)
