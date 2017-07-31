from __future__ import division

from numpy import matrix
from numpy.random import random_sample
import numpy as np

import pandas as pd

from scipy import optimize

from functools import partial

'''
establishing model for problem, 
solve the problem using grafting algorithm 
model:
    C(w;X,Y,threshold)=|X*w-Y|_2+threshold*|w|_1
where:
    w: d*1
    X: n*d
    Y: n*1
    threshold: scalar value
'''

def normalize(x): 
    return (x-np.mean(x))/np.std(x)

def f(w, X):
    return np.dot(X, w)

def Loss(w, X, Y):
    mat = np.dot(X, w) - Y
    return np.linalg.norm(mat, ord=2)

def Loss_grad(w, X, Y):
    mat = np.dot(X, w) - Y
    loss = np.linalg.norm(mat, ord=2)
    mat = np.dot(X.T, mat)
    return mat[-1, 0]/loss

def C(w, X, Y, threshold):
    w = np.matrix(w).reshape((X.shape[1], Y.shape[1]))
    return Loss(w, X, Y) + threshold*np.linalg.norm(w, 1)

def gradient_validation_std(x, w, X, Y, threshold):
    X_new = np.hstack((X, x))
    points_number = 20
    points = random_sample(points_number)*2 - 1
    for point in points:
        w_new = np.vstack((w, point))
        grad = Loss_grad(w_new, X_new, Y)
        if abs(grad)>threshold:
        #if np.sign(point)*grad + threshold < 0:
            print("grad = %s"%str(grad))
            return True
    return False

def gradient_validation(x, w, X, Y, threshold, epsilon):
    X_new = np.hstack((X, x))
    points = np.array((-epsilon, epsilon))
    #eps = np.sqrt(np.finfo(float).eps)
    #eps_array = w*eps
    for point in points:
        w_new = np.vstack((w, point))
        #eps_array_new = np.hstack((eps_array, eps*point))
        #grad = optimize.approx_fprime(w_new, Loss, eps_array_new, X_new, Y)[-1]
        grad = Loss_grad(w_new, X_new, Y)
        #if abs(grad)>threshold:
        if np.sign(point)*grad + threshold < 0:
            # print("grad = %s"%str(grad))
            return True
    return False
 
def update_wegiht(w, X, Y, threshold):
    #wopt, fopt = optimize.fmin_bfgs(C, w, args=(X, Y, threshold), full_output=1)[:2]
    wopt, fopt = optimize.fmin_cg(C, w, args=(X, Y, threshold), full_output=1, disp=0)[:2]
    return np.matrix(wopt).reshape((X.shape[1], Y.shape[1])), fopt

def refresh_selected(W, X, X_index, epsilon=1e-3):
    X_zero, X = X[:, 0], X[:, 1:]
    W_zero, W = W[0, :], W[1:, :]
    df_x = pd.DataFrame(X.transpose(), index=X_index) 
    df_w = pd.DataFrame(W, index=X_index)
    RowScore = pd.Series(np.linalg.norm(W, ord=1, axis=1), index=X_index)
    RowScore = RowScore[RowScore > epsilon]
    X_index = np.array(RowScore.index)
    X = df_x.ix[X_index].get_values().transpose()
    X = np.hstack((X_zero, X))
    W = df_w.ix[X_index].get_values()
    W = np.vstack((W_zero, W))
    return W, X, X_index

