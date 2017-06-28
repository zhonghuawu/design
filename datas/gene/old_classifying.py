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

def read_data(fname, pos):
    data = sio.loadmat(fname)
    X, Y = None, None
    if 'data' in data.keys():
        data = data['data']
        Y = data[:, pos]
        X = np.delete(data, pos, axis=1)
    else :
        X = data['X']
        Y = data['Y'][:, 0]
    return X, Y

# whole data set, use cross validation to classify
def run_cross_validation(X, y):
    print "size of data matrix: ", X.shape 
    #print "size of label matrix: ", y.shape 
    #clf = svm.SVC(kernel='poly')
    clf = svm.SVC(kernel='linear')
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    #print "cross validation scores: ", scores
    print "cross validation accuracy: ", scores.mean()
    #clf = svm.LinearSVC()
    #X_train, X_test, y_train, y_test = train_test_split(X, y, random_state=1)
    #clf.fit(X_train, y_train)
    #y_pred = clf.predict(X_test)

    #print "y_test: \n", y_test
    #print "y_pred: \n", y_pred
    #print confusion_matrix(y_test, y_pred)
    #print "accuracy: %f"%accuracy_score(y_test, y_pred)

# already split train and test data set
def run_train_test_split(X_train, y_train, X_test, y_test):
    print "size of train data matrix: ", X_train.shape
    print "size of test data matrix: ", X_test.shape
    #clf = svm.SVC()
    clf = svm.SVC(kernel='linear')
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)

    #print "y_test: \n", y_test
    #print "y_pred: \n", y_pred
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

def run(fname, pos, splited):
    import os
    fn = os.path.splitext(fname)[0]
    if not splited:
        print "classifying dataset: %s"%fn
        X, Y = read_data("%s.mat"%fn, pos)
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
    else:
        print "classifying dataset: %s"%fn
        X_train, Y_train = read_data("%s_train.mat"%fn, pos)
        X_test, Y_test = read_data("%s_test.mat"%fn, pos)
        print "**"*30
        print "origin data: "
        run_train_test_split(X_train, Y_train, X_test, Y_test)
        print "**"*30
        
        with open(fname, 'r') as f:
            for line in f:
                alg, indexes = line.split(":")[:2]
                print "after fs using %s: "%alg
                indexes = eval(indexes)
                print "selected features index: \n%s"%indexes
                run_train_test_split(X_train[:, indexes], Y_train, X_test[:, indexes], Y_test)
                print "**"*30

def get_options(args):
    from optparse import OptionParser
    opt = OptionParser(usage='%prog datafilename [options]')
    opt.add_option('-s', '--splited', action='store_true', dest='splited', help='whether data set is splited to train and test set')
    opt.add_option('-p', '--label_pos', action='store', type='int', dest='label_pos', default=-1, help='label position in data set(0: begin, -1: end)')
    #opt.set_default(label_pos=-1)
    return opt.parse_args(args)[0]

if __name__ == "__main__":
    import sys
    options = get_options(sys.argv[2:])
    run(sys.argv[1], options.label_pos, options.splited)
    print 'DONE'
