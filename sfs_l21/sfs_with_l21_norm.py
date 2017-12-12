from __future__ import division

import pandas as pd
import numpy as np
import scipy as sp
import math

from scipy import optimize

"""
streaming features selection using l2,1-norm regularized term
W is selection matrix with d*c dimension
X is data matrix with n*d dimension
Y is labels matrix with n*c dimension, the j-th of i-th Y is 1 if i-th X is belong to j-th class
here, 
n is number of samples
d is number of features of every sample
c is number of labels 
"""

def L2_norm(vec):
    return np.linalg.norm(vec)
    
def normalizate(X):
    X = np.array(X)
    mean = X.mean()
    std = X.std()
    return (X-mean)/std

# loss function, frobenious norm using np.linalg
def Loss_F2_std(W, X, Y):
    res = np.dot(np.matrix(X), np.matrix(W)) - np.matrix(Y)
    return np.linalg.norm(res, ord='fro')

# loss function gradient for W(t, :) of frobenious norm
def Loss_grad(w, x, Y):
    n, c = Y.shape
    res = 0
    for i in range(n):
        for k in range(c):
            res += (x[i]*w[k] - Y[i, k])*x[i]
    return res

# Regulazied term using l21-norm 
def Regularized_term(W):
    '''L21-norm Regularized term'''
    res = 0
    W = np.matrix(W)
    d, c = W.shape
    for j in range(d):
        res += L2_norm(W[j, :])
    return res

# D(t, t) = (1/2)*(1/W(t,:)^2)
def get_D_tt(w):
    D_tt = L2_norm(w)
    return 1/D_tt/2

def Regularized_term_grad(w):
    res = 0
    c = len(w)
    for k in range(c):
        res += w[k]
    D_tt = get_D_tt(w)
    return res*D_tt

def J_one(w, X_model, y, threshold):
    return L2_norm(np.dot(X_model,w)-y)+threshold*L2_norm(w)

def J(W, X, Y, threshold):
    return Loss_F2_std(W, X, Y)+threshold*Regularized_term(W)

def gradient_validation(x, W, X_model, Y, threshold, j):
    #sample_point = [-1, -0.5, -0.1, 0.1, 0.5, 1]
    n, c = Y.shape
    sample_point_number = 30
    sample_points = 2*np.random.random_sample((sample_point_number, c))-1
    
    k_count = 0
    for w in sample_points:
        w = np.matrix(w).T
        grad = Loss_grad(w, x, Y)+threshold*Regularized_term_grad(w)
        if grad < 0:
            k_count+=1
    print 'for %d-th feature, k_count = %d'%(j, k_count)
    if k_count >= sample_point_number/2:
        return True
    return False

def gradient_validation_std(x, W, X_model, Y, threshold, j):
    res = False
    n, d = X_model.shape
    n, c = Y.shape
    eps = 0.1
    sample_point_number = 50
    from numpy.random import random_sample
    sample_points = eps*random_sample((sample_point_number, c))-0.5*eps
    M = np.hstack((X_model, x))
    M = np.dot(M.T, M)
    D_vector = 0.5/np.linalg.norm(W, axis=1)
    
    W_old = np.vstack((W, np.ones(c)))
    D_old = np.diag(np.hstack((D_vector, [0])))
    gradient_old = 2*threshold*np.dot(D_old, W_old)-2*np.dot(M, W_old)

    k_count = 0
    for w in sample_points:
        w = np.matrix(w)
        gradient_incre = np.zeros((d, c))
        gradient_incre = np.vstack((gradient_incre, threshold*w/L2_norm(w)))
        gradient_incre = gradient_incre-2*np.dot(np.matrix(M[:, d]), np.matrix(w))
        subgradient = gradient_old + gradient_incre

        if sum(np.dot(np.matrix(subgradient), np.matrix(w).transpose()))<0:
            k_count += 1
    print 'for %d-th feature, k_count = %d'%(j, k_count)
    if k_count >= sample_point_number/2:
        res = True
    return res

def update_weight(W, X, Y, threshold):
    from functools import partial
    from scipy import optimize
    [n, d] = X.shape
    [n, c] = Y.shape
    W = np.vstack((W, np.ones(c)))
    for k in range(c):
        f=partial(J_one, X_model=X, y=Y[:, k], threshold=threshold)
        W[:, k] = optimize.fmin_cg(f, W[:, k])
    return W

def refresh_selected(W, X_model, Y, RetainCount, X_index):
    from pandas import Series, DataFrame
    X_zero = X_model[:, 0]
    X_dataframe = DataFrame(X_model[:,1:].transpose(), index=X_index)
    W_zero = W[0,:]
    W_dataframe = DataFrame(W[1:,:], index=X_index)
    RowScore = np.linalg.norm(W[1:, :], axis=1)
    RowScore_serires = Series(RowScore, index=X_index)
    RowScore_serires = RowScore_serires.sort_values(ascending=False)[:RetainCount]
    X_index_new = np.array(RowScore_serires.index)
    X_model_new = X_dataframe.ix[X_index_new].get_values().transpose()
    X_model_new = np.matrix(np.hstack((X_zero, X_model_new)))
    W_new = W_dataframe.ix[X_index_new].get_values()
    W_new = np.vstack((W_zero, W_new))
    return W_new, X_model_new, X_index_new 
    
def sfs_l21_norm(X, Y, threshold = 0.1):
    [n, d] = X.shape
    [n, c] = Y.shape
    MinCount = 30
    RetainCount = 25
    X_index = [i for i in range(MinCount)]
    X_model = np.ones_like(X[:,0])
    X_model = np.matrix(np.c_[X_model, X[:, X_index]])
    W = np.ones((MinCount, c))
    W = update_weight(W, X_model, Y, threshold)

    for j in range(MinCount, d):
        x = normalizate(X[:, j])
        #if gradient_validation(x, W, X_model, Y, threshold, j):
        if gradient_validation_std(x, W, X_model, Y, threshold, j):
            X_index = np.hstack((X_index, [j]))
            X_model = np.hstack((X_model, x))
            W = update_weight(W, X_model, Y, threshold)
            W, X_model, X_index = refresh_selected(W, X_model, Y, RetainCount, X_index)
        print "**"*10,
        print "check object value: ", J(W, X_model, Y, threshold)
    return X_index, X_model, W

def run():
    import scipy.io as sio
    #fr_n = r"/home/huaa/workspace/datas/gene_expr/ColonTumor/colonTumor.mat"
    fr_n = r"./datas/DLBCL-Stanford/DLBCL-Stanford.mat"
    data = sio.loadmat(fr_n)['data']
    X = data[:, :-1]
    y = data[:, -1]
    number_of_classes = len(set(y))
    number_of_samples = len(y)
    Y = np.matrix(np.zeros((number_of_samples, number_of_classes)))
    for i in range(number_of_samples):
        Y[i, int(y[i])] = 1

    threshold = 0.1
    X_index, X_model, W = sfs_l21_norm(np.matrix(X), np.matrix(Y), threshold)
    print 
    print "**"*20
    print "selected features:"
    print X_index
    print "selected features data:"
    print X_model
    print "weight matrix:"
    print W

if __name__ == '__main__':
    run()
    print "Done"
