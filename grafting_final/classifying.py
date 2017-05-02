import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm
from sklearn import model_selection
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import numpy as np
import scipy as sp

from util import read_data

# whole data set, use cross validation to classify
def run_cross_validation(X, y):
    print "size of data matrix: ", X.shape 
    #clf = svm.SVC()
    clf = svm.SVC(kernel='linear')
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    print "cross validation scores: ", scores, scores.mean()
    clf = svm.LinearSVC()
    X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print "y_test: \n", y_test
    print "y_pred: \n", y_pred
    print confusion_matrix(y_test, y_pred)

    print "accuracy: %f"%accuracy_score(y_test, y_pred)

# already split train and test data set
def run_train_test_split(X_train, X_test, y_train, y_test):
    print "size of train data matrix: ", X_train.shape
    print "size of test data matrix: ", X_test.shape
    #clf = svm.SVC()
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    print "y_test: \n", y_test
    print "y_pred: \n", y_pred
    print confusion_matrix(y_test, y_pred)

    print "accuracy: %f"%accuracy_score(y_test, y_pred)

# run interface
def classifying(X, Y, X_test=None, Y_test=None, args={}):
    if X_test==None and Y_test==None:
        for info, indexes in args.items():
            print info
            run_cross_validation(X[:, indexes], Y)
    else:
        for info, indexes in args.items():
            print info
            run_train_test_split(X[:, indexes], Y, X_test[:, indexes], Y_test)

def run(*args):
    print args
    if len(args) == 1:
        fname = args[0]
        print 'deal with %s'%fname
        print "origin data set"
        X, Y = read_data(fname)
        run_cross_validation(X, Y)
        print "after sf using osfs "
        indexes = [1278, 2416]
        X_model = X[:, indexes]
        run_cross_validation(X_model, Y)
    elif len(args) == 1:
        X_train, Y_train = read_data(args[0])
        X_test, Y_test = read_data(args[1])
        run_train_test_split(X_train, Y_train, X_test, Y_test)
    else:
        print "arguments for classified error"

if __name__ == "__main__":
    import sys
    run(sys.argv[1])
    print 'DONE'
