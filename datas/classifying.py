import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm, linear_model, tree
from sklearn import model_selection
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import numpy as np
import scipy as sp
import scipy.io as sio

import os
import sys

def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    return X, Y

# whole data set, use cross validation to classify
def run_cross_validation(X, y):
    print "size of data matrix: ", X.shape 
    clf = svm.SVC(kernel='linear')
    # clf = tree.DecisionTreeClassifier()
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    print "cross validation accuracy: ", scores.mean()

def run_one(fname):
    fn = os.path.splitext(fname)[0]
    fn = os.path.split(fn)[1]
    print "classifying dataset: %s"%fn
    X, Y = read_data("dataset/%s.mat"%fn)
    line = ''
    with open(fname, 'r') as f:
        line = f.readlines()[-2]
    alg, indexes = line.split(':')[:2]
    indexes = eval(indexes)
    run_cross_validation(X[:, indexes], Y)

def run(fname, clf):
    dataset_type, alg_name, dataset_name = fname.split('/')
    dataset_name = dataset_name.split('.')
    print "classifying dataset: %s"%dataset_name
    X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))
    print "**"*35
    print "origin data: "
    print "size of data matrix: ", X.shape 
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    print "cross validation accuracy: ", scores.mean()
    print "**"*35
    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(":")[:2]
            print "after fs using %s: "%alg
            indexes = eval(indexes)
            X_fs = X[: indexes]
            print "size of data matrix: ", X_fs.shape 
            scores = model_selection.cross_val_score(clf, X_fs, y, cv=5, scoring="accuracy")
            print "cross validation accuracy: ", scores.mean()
            print "**"*35

def run_one_grafting_or_l21(fname, clf):
    dataset_type, alg_name, dataset_name = os.path.split(fname.split('.'))
    print "classifying dataset: %d"%dataset_name

    X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))

    wfname = "%s/all_result/%s/%s_cls.output_streaming"%(dataset_type, alg_name, dataset_name)
    f_streaming = open(wfname, 'w')
    f_streaming.write("classify dataset: %s"%dataset_name+'\n')
    f_streaming.write("**"*35+'\n')
    f_streaming.write("origin data: "+'\n')
    f_streaming.write("size of data matrix: "+str(X.shape)+'\n')
    scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
    f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

    f_streaming.write("**"*35+'\n')
    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(':')[:2]
            f_streaming.write("after fs using %s: "%alg)
            indexes = eval(indexes)
            X_fs = X[:, np.array(eval(indexes))-1]
            f_streaming.write("size of data matrix: "+str(X_fs.shape)+'\n')
            scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
            f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

            f_streaming.write("**"*35+'\n')
    f_streaming.write("DONE")
    f_streaming.close()

def run_all_osfs_or_saola(fname, clf):
    dataset_type, alg_name = fname.split('/')
    alg_name = alg_name.split('.')[0][4:] # alg_name = osfs or saola
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            wfname = "%s/all_result/streaming_%s/%s_cls.output_streaming"%(dataset_type, alg_name, dataset_name)
            f_streaming = open(wfname, 'w')
            print "classify dataset: %s"%dataset_name
            f_streaming.write("classify dataset: %s"%dataset_name+'\n')
            X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))
            f_streaming.write("**"*35+'\n')
            f_streaming.write("origin data: "+'\n')

            f_streaming.write("size of data matrix: "+str(X.shape)+'\n')
            scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
            f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

            f_streaming.write("**"*35+'\n')
            indexes_set = indexes_set.split()
            percent = 10
            for indexes in indexes_set:
                if not indexes.startswith('['):
                    continue
                f_streaming.write("after fs using %3d%% %s: "%(percent, alg)+'\n')

                X_fs = X[:, np.array(eval(indexes))-1]
                f_streaming.write("size of data matrix: "+str(X_fs.shape)+'\n')
                scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

                f_streaming.write("**"*35+'\n')
                percent+=10
            f_streaming.write("DONE")
            f_streaming.close()

def run_all_Alpha_investing(fname, clf):
    dataset_type, alg_name = fname.split('/')
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            if line == '':
                continue
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            wfname = "%s/all_result/streaming_Alpha_investing/%s_cls.output_streaming"%(dataset_type, dataset_name)
            f_streaming = open(wfname, 'w')
            print "classify dataset: %s"%dataset_name
            f_streaming.write("classify dataset: %s"%dataset_name+'\n')
            X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))
            f_streaming.write("**"*35+'\n')
            f_streaming.write("origin data: "+'\n')

            f_streaming.write("size of data matrix: "+str(X.shape)+'\n')
            scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
            f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

            f_streaming.write("**"*35+'\n')

            indexes_set = eval(indexes_set)
            n, d = X.shape
            d_part=(d+9)/10
            for i in range(1, 11):
                indexes = indexes_set[indexes_set<d_part*i]
                percent = i*10
                f_streaming.write("after fs using %3d%% %s: "%(percent, alg)+'\n')
                X_fs = X[:, indexes]
                f_streaming.write("size of data matrix: "+str(X_fs.shape)+'\n')
                scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

                f_streaming.write("**"*35+'\n')
            f_streaming.write("DONE")
            f_streaming.close()


if __name__ == "__main__":
    clf = svm.SVC(kernel='linear')
    run(sys.argv[1], clf)
    # for sfs_l21 and grafting alg
    # run(sys.argv[1])

    # for osfs alg
    # run_all_osfs(sys.argv[1])
    
    #for saola alg
    # run_all_saola(sys.argv[1])

    #for Alpha_investing alg
    # run_all_Alpha_investing(sys.argv[1])

    print 'DONE'
