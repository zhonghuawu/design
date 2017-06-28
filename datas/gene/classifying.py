import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm
from sklearn import model_selection
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import numpy as np
import scipy as sp
import scipy.io as sio

import os

def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    return X, Y

# whole data set, use cross validation to classify
def run_cross_validation(X, y):
    print "size of data matrix: ", X.shape 
    #clf = svm.SVC(kernel='poly')
    clf = svm.SVC(kernel='linear')
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    #print "cross validation scores: ", scores
    print "cross validation accuracy: ", scores.mean()


def run(fname):
    fn = os.path.splitext(fname)[0]
    fn = os.path.split(fn)[1]
    print "classifying dataset: %s"%fn
    X, Y = read_data("dataset/%s.mat"%fn)
    print "**"*35
    print "origin data: "
    run_cross_validation(X, Y)
    print "**"*35
    with open(fname, 'r') as f:
        for line in f:
            alg, indexes = line.split(":")[:2]
            print "after fs using %s: "%alg
            indexes = eval(indexes)
            #print "selected features index: \n%s"%indexes
            run_cross_validation(X[:, indexes], Y)
            print "**"*35

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
    print 'DONE'
