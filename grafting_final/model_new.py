from __future__ import division

from numpy import matrix
from numpy.random import random_sample
import numpy as np

import pandas as pd

from scipy import optimize as opt

from functools import partial

'''
establishing model for problem, 
solve the problem using grafting algorithm 
'''

def normalize(x): 
    return (x-np.mean(x))/np.std(x)

def f(w, x):
    return np.dot(w, x.T)[0, 0]

def loss(w, f_val, y):
    return np.log(1+np.exp(-y*f_val))

def Loss(w, X, Y):
    n = X.shape[0]
    result = 0
    for i in range(n):
        f_val = f(w, X[i, :])
        result += loss(w, f_val, Y[i, 0])
    return result/n

def C(w, X, Y, threshold):
    return Loss(w, X, Y) + threshold*np.linalg.norm(w, 1)

def Loss_grad(x, F_VAL, Y):
    n = Y.shape[0]
    result = 0
    for i in range(n):
        result += (-Y[i, 0])/(1+np.exp(Y[i, 0]*F_VAL[i, 0]))*x[i, 0]
    return result/n

def C_grad(x, w, X, Y, threshold, epsilon):
    sub_F_VAL = np.dot(X, w)
    points_number = 20
    points = 2*epsilon*random_sample(points_number) - epsilon
    #print "sub_F_VAL = \n%s"%str(sub_F_VAL)
    for point in points:
        F_VAL = sub_F_VAL +  x*point
        grad = Loss_grad(x, F_VAL, Y)
        if abs(grad)>threshold:
        #if np.sign(point)*grad + threshold < 0:
            print "points = %s"%str(point)
            print "grad = %s\t"%str(grad)
            return True
    return False

def update_wegiht(w, X, Y, threshold):
    #wopt, fopt = opt.fmin_bfgs(C, w, args=(X, Y, threshold), full_output=True)[:2]
    wopt, fopt = opt.fmin_cg(C, w, args=(X, Y, threshold), full_output=True)[:2]
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
