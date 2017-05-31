from __future__ import division

from numpy.linalg import norm
from numpy import matrix
import numpy as np

from numpy.random import random_sample

import math

from functools import partial

def normalizate(x):
    x = matrix(x)
    return (x-x.mean())/x.std()

def f(w, x):
    return np.dot(matrix(w), matrix(x).T)[0, 0]

def Loss(w, X, y):
    result = np.dot(matrix(X), matrix(w).T)-matrix(y)
    return norm(result, 2)

def Loss_grad(x, w, X, y):
    X_new = np.hstack((X, x))
    result = np.dot(matrix(X_new), matrix(w).T)-matrix(y)
    result = np.dot(matrix(result).T, matrix(x))
    return result[0, 0]*0.5

def C(w, X, y, threshold):
    return Loss(w, X, y)+threshold*norm(w, 1)

def C_grad(x, w, X, y, threshold):
    sample_point_number=20
    sample_points = random_sample(sample_point_number)*2-1
    k_count = 0
    for point in sample_points:
        w_new = np.hstack((w, point))
        if abs(Loss_grad(x, w_new, X, y))>threshold:
            k_count += 1
    print ", k_count = %d"%k_count
    if k_count >= sample_point_number/2:
        return True
    return False

def C_Logistic(w, X, y, threshold):
    n = X.shape[0]
    res = 0
    for i in range(n):
        res += math.log(1+math.exp(-y[i]*f(w, X[i, :])))
    res = res/n + threshold*np.linalg.norm(w, 1)
    return res
def Loss_Logistic(x, w, X, y):
    X_new = np.hstack((X, x))
    n = X.shape[0]
    res = 0
    for i in range(n):
        res -= y[i]/(1+math.exp(y[i]*f(w, X_new[i, :])))*x[i]
    return res/n
def C_grad_Logistic(x, w, X, y, threshold):
    from numpy.random import random_sample
    sample_point_number = 10
    sample_points = random_sample(sample_point_number)*2-1
    for point in sample_points:
        w_new = np.hstack((w, point))
        if abs(Loss_Logistic(x, w_new, X, y))>threshold:
            return True
    return False


# update weight vector of selected feature using conjugrate gradient algorithm
def update_weight_by_cg(w, X, y, threshold):
    from scipy.optimize import fmin_cg
    f = partial(C_Logistic, X=X, y=y, threshold=threshold)
    w = fmin_cg(f, w)
    return w

def update_weight_by_bfgs(w, X, y, threshold):
    from scipy.optimize import fmin_bfgs
    f = partial(C_Logistic, X=X, y=y, threshold=threshold)
    w = fmin_bfgs(f, w)
    return w
