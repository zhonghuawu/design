from __future__ import division

import numpy as np
from scipy import optimize
from functools import partial
import matplotlib.pyplot as plt

# w is vector of features weight
# x is sample vector
# X is sample matrix
# y is label value (-1, 1)
# Y is label matrix

def f(w, x):
    return np.dot(np.matrix(w), np.matrix(x).T)

def loss(w, x, y):
    return np.log(1+np.exp((-y)*f(w, x)))[0, 0]

def Loss(w, X, Y):
    n = X.shape[0]
    res = 0
    for i in range(n):
        res += loss(w, X[i, :], Y[i, :])
    return res/n

def C(w, X, Y, threshold):
    res = Loss(w, X, Y)
    res += threshold*np.linalg.norm(w, 1)
    return res

def normalize(x):
    return (x-np.mean(x))/np.std(x)

#X = np.matrix(np.random.random((3,10)))
X = np.matrix(
        [[0.61856832, 0.22510381, 0.57838847, 0.19514078, 0.12633871, 0.61386397, 0.16392846, 0.26312341, 0.78464014, 0.38205329],
         [0.3771132 , 0.42317827, 0.88295305, 0.44258504, 0.7210982 , 0.71181544, 0.62802295, 0.73161301, 0.64498065, 0.24541482],
         [0.23418782, 0.03861684, 0.4098603 , 0.62496842, 0.66906535, 0.60161075, 0.76008686, 0.24457919, 0.65445907, 0.7220447]])

for j in range(X.shape[1]):
    X[:, j] = normalize(X[:, j])
#Y = np.matrix([1,-1,1]).T
Y = np.matrix([[1,0],[0,1],[1,0]])
threshold = 0.1

n, d = X.shape
n, c = Y.shape
print "n = %d"%n
print "d = %d"%d
print "c = %d"%c
W = np.matrix(np.ones((d, c)))

def Loss(W, X, Y):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    mat = np.dot(X, W) - Y
    return np.linalg.norm(mat)

def Regularized_term(W):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    arr = np.linalg.norm(W, ord=2, axis=1)
    return np.linalg.norm(arr, ord=1, axis=0)

def J(W, X, Y, threshold):
    res = Loss(W, X, Y)
    res += threshold*Regularized_term(W)
    return res

F=partial(J, X=X, Y=Y, threshold=threshold)

results = optimize.fmin_cg(F, W, full_output=1, disp=1)
print results
