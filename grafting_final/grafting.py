from __future__ import division

from numpy import matrix
import numpy as np

from pandas import Series, DataFrame
import pandas as pd
import matplotlib.pyplot as plt

from model import *

'''
run grafting algorithm on data set from file fname
'''
import logging
import logging.config

logging.config.fileConfig("logging.conf")
logger = logging.getLogger('main')

def grafting(X, Y, threshold):
    #print "threshold = %f"%threshold
    logger.info("threshold = %f"%threshold)
    X_model = np.ones_like(X[:, 0])
    w = np.ones(1)

    X_index = np.array([])
    X_index_retained = np.array([])
    obj_values = np.array([])
    epsilon = 1e-3

    n, d = X.shape
    for j in range(d):
        x = normalize(X[:, j])
        if C_grad_std(x, w, X_model, Y, threshold):
            X_index_retained = np.hstack((X_index_retained, j))
            X_model = np.hstack((X_model, x))
            w = np.hstack((w, 1))
            w, obj_value = update_wegiht(w, X_model, Y, threshold)
            w, X_model, X_index_retained = refresh_selected(w, X_model, X_index_retained, epsilon)
            #print "j = %-6d obj_value = %f"%(j, obj_value)
            #print "X_index_retained = %s"%str(X_index_retained)
            #print "weight_vector = %s"%str(w)
            logger.info("j = %-6d obj_value = %f"%(j, obj_value))
            logger.info("X_index_retained = %s"%str(X_index_retained))
            logger.info("weight_vector = %s"%str(w))
            X_index = np.hstack((X_index, j))
            obj_values = np.hstack((obj_values, obj_value))
    return X_index_retained, w, X_index, obj_values

def run(fname):
    logger.info("deal with %s..."%fname)
    from util import read_data
    X, Y = read_data(fname)
    threshold = 0.2
    logger.info("X shape: %s"%str(X.shape))
    X_index_retained, w, X_index, obj_values = grafting(np.matrix(X), np.matrix(Y).T, threshold)
    
    logger.info(str("**"*30))
    logger.info("selected features index retained: %s"%str(X_index_retained))
    logger.info("selected features weight: %s"%str(w))
    logger.info("selected features index: %s"%str(X_index))
    logger.info("objective function values: %s"%str(obj_values))
    logger.info(str("**"*30))
    logger.info("DONE")

    obj_values_df = DataFrame(obj_values, index=X_index, columns=["obj values"])
    weights_df = DataFrame(w, index=np.hstack((-1, X_index_retained)), columns=["weight"])
    df = pd.concat((obj_values_df, weights_df))
    df.plot(subplots=True)
    plt.show()

if __name__ == '__main__':
    import sys
    fname = sys.argv[1]
    run(fname)
