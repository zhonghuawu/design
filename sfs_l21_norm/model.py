from __future__ import division

import pandas as pd
import numpy as np
import scipy as sp
import itertools as it
import math

import scipy.optimize as opt

from util import fprime
"""
streaming features selection model Regularized by l21-norm term

W is selection matrix, d*c dimension
X is data matrix, n*d dimension
Y is labels matrix, n*c dimension, the j-th of i-th Y is 1 if i-th X is belong to j-th class
here, 
n is number of samples
d is number of features of every sample
c is number of label catergories
"""

"""
features selection model:
  J(W, X, Y, threshold) = ||X*W-Y||(fro, 2) + threshold*||W||(2,1)
"""

def normalizate(x):
    return (x-x.mean())/x.std()

def L21_norm(W):
    vec = np.linalg.norm(W, ord=2, axis=1)
    return np.linalg.norm(vec, ord=1, axis=0)

def Loss_Fro(W, X, Y):
    mat = np.dot(X, W) - Y
    return np.linalg.norm(mat, ord='fro')
    #return L21_norm(mat)

def J(W, X, Y, threshold):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    return Loss_Fro(W, X, Y)+threshold*L21_norm(W)

def J_grad(W, X, Y, threshold):
    W = np.matrix(W).reshape((X.shape[1], Y.shape[1]))
    mat = np.dot(X, W) - Y
    loss = np.linalg.norm(mat, ord='fro')
    mat = np.dot(X.T, mat)
    grad_loss = mat[-1, :]/loss
    D_vector = 0.5/np.linalg.norm(W, axis=1)
    D = np.diag(D_vector)
    grad_regularized_term = 2*threshold*np.sum(np.dot(D, W)[-1, :])
    return grad_loss + grad_regularized_term


def gradient_validation(x, W, X, Y, threshold, epsilon):
    X_new = np.hstack((X, x))
    points = it.product((-epsilon, epsilon), repeat=Y.shape[1])
    #eps = np.sqrt(np.finfo(float).eps)
    #eps_matrix = np.matrix(W)*eps
    for point in points:
        W_new = np.vstack((W, point))
        #eps_matrix_new = np.vstack((eps_matrix, eps*np.matrix(point)))
        #grad = fprime(W_new, J, eps_matrix_new, X_new, Y, threshold)[-1, :]
        grad = J_grad(W_new, X_new, Y, threshold)
        grad_mat = np.matrix(grad)
        sign_mat = np.matrix(np.sign(point)).T
        grad_sum = np.dot(grad_mat, sign_mat)[0, 0]
        #grad = J_grad(W_new, X_new, Y, threshold)
        if grad_sum < 0:
            print "point = %s"%str(point)
            print "grad_mat = %s"%str(grad_mat)
            print "grad_sum = %s"%str(grad_sum)
            return True
    return False

def update_weight(W, X, Y, threshold):
    #W, obj_value = opt.fmin_bfgs(J, W, args=(X, Y, threshold), full_output=1)[:2]
    W, obj_value = opt.fmin_cg(J, W, args=(X, Y, threshold), full_output=1)[:2]
    return np.matrix(W).reshape((X.shape[1], Y.shape[1])), obj_value

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

