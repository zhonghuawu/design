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
'''

def normalize(x): 
    return (x-np.mean(x))/np.std(x)

def f(w, x):
    return np.dot(w, x.T)[0, 0]

def loss(w, x, y):
    return np.log(1+np.exp(-y*(np.dot(w, x.T)[0, 0])))  #f(w, x)))

def Loss(w, X, Y):
    n = X.shape[0]
    result = 0
    for i in range(n):
        result += loss(w, X[i, :], Y[i, 0])
    return result/n

def Loss_grad(x, w, X, Y):
    X_new = np.hstack((X, x))
    n = X_new.shape[0]
    result = 0
    for i in range(n):
        result += -Y[i, 0]*x[i, 0]/(1+np.exp(Y[i, 0]*f(w, X_new[i, :])))
    return result/n

def C(w, X, Y, threshold):
    return Loss(w, X, Y) + threshold*np.linalg.norm(w, 1)

def C_grad(x, w, X, Y, threshold):
    points_number = 20
    points = random_sample(points_number)*2 - 1
    for point in points:
        w_new = np.hstack((w, point))
        grad = Loss_grad(x, w_new, X, Y)
        #if abs(grad)>threshold:
        if np.sign(point)*grad + threshold < 0:
            print "grad = %10.7f\t"%grad,
            return True
    return False

def C_grad_std(x, w, X, Y, threshold, epsilon):
    X_new = np.hstack((X, x))
    points = np.array((-epsilon, epsilon))
    eps = np.sqrt(np.finfo(float).eps)
    eps_array = w*eps
    for point in points:
        w_new = np.hstack((w, point))
        eps_array_new = np.hstack((eps_array, eps*point))
        grad = optimize.approx_fprime(w_new, Loss, eps_array_new, X_new, Y)[-1]
        if abs(grad)>threshold:
        #if np.sign(point)*grad + threshold < 0:
            print("grad = %10.7f\t"%grad)
            return True
    return False
 
def update_wegiht(w, X, Y, threshold):
    #wopt, fopt = optimize.fmin_bfgs(C, w, args=(X, Y, threshold), full_output=1)[:2]
    wopt, fopt = optimize.fmin_cg(C, w, args=(X, Y, threshold), full_output=1)[:2]
    return wopt, fopt

def refresh_selected(w, X_model, X_index, epsilon):
    X_model_zero, X_model = X_model[:, 0], X_model[:, 1:]
    w_zero, w = w[0], w[1:]
    df = pd.DataFrame(X_index, index=w)
    df = df[np.abs(df.index)>epsilon]
    X_index_new = df.get_values().transpose()[0]
    df = pd.DataFrame(X_model.transpose(), index=w)
    df = df[np.abs(df.index)>epsilon]
    X_model_new = np.hstack((X_model_zero, df.get_values().transpose()))
    w_new = np.hstack((w_zero, np.array(df.index)))
    return w_new, X_model_new, X_index_new
