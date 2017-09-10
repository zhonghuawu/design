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

def run_all_osfs(fname):
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            f_streaming_osfs = open("all_result/streaming_osfs/%s_cls.output_streaming_osfs"%dataset_name, 'w')
            print "classify dataset: %s"%dataset_name
            f_streaming_osfs.write("classify dataset: %s"%dataset_name+'\n')
            X, Y = read_data("dataset/%s.mat"%dataset_name)
            # print "**"*35
            # print "origin data: "
            f_streaming_osfs.write("**"*35+'\n')
            f_streaming_osfs.write("origin data: "+'\n')
            # run_cross_validation(X, Y)

            f_streaming_osfs.write("size of data matrix: "+str(X.shape)+'\n')
            #clf = svm.SVC(kernel='poly')
            clf = svm.SVC(kernel='linear')
            scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
            #print "cross validation scores: ", scores
            f_streaming_osfs.write("cross validation accuracy: "+str(scores.mean())+'\n')

            # print "**"*35
            f_streaming_osfs.write("**"*35+'\n')
            indexes_set = indexes_set.split()
            percent = 10
            for indexes in indexes_set:
                # print "after fs using %3d%% %s: "%(percent, alg)
                f_streaming_osfs.write("after fs using %3d%% %s: "%(percent, alg)+'\n')
                # run_cross_validation(X[:, eval(indexes)], Y)

                X_fs = X[:, np.array(eval(indexes))-1]
                f_streaming_osfs.write("size of data matrix: "+str(X_fs.shape)+'\n')
                #clf = svm.SVC(kernel='poly')
                clf = svm.SVC(kernel='linear')
                scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                #print "cross validation scores: ", scores
                f_streaming_osfs.write("cross validation accuracy: "+str(scores.mean())+'\n')

                # print "**"*35
                f_streaming_osfs.write("**"*35+'\n')
                percent+=10
            f_streaming_osfs.write("DONE")
            f_streaming_osfs.close()

def run_all_saola(fname):
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            f_streaming_saola = open("all_result/streaming_saola/%s_cls.output_streaming_saola"%dataset_name, 'w')
            print "classify dataset: %s"%dataset_name
            f_streaming_saola.write("classify dataset: %s"%dataset_name+'\n')
            X, Y = read_data("dataset/%s.mat"%dataset_name)
            # print "**"*35
            # print "origin data: "
            f_streaming_saola.write("**"*35+'\n')
            f_streaming_saola.write("origin data: "+'\n')
            # run_cross_validation(X, Y)

            f_streaming_saola.write("size of data matrix: "+str(X.shape)+'\n')
            #clf = svm.SVC(kernel='poly')
            clf = svm.SVC(kernel='linear')
            scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
            #print "cross validation scores: ", scores
            f_streaming_saola.write("cross validation accuracy: "+str(scores.mean())+'\n')

            # print "**"*35
            f_streaming_saola.write("**"*35+'\n')
            indexes_set = indexes_set.split()
            percent = 10
            for indexes in indexes_set:
                # print "after fs using %3d%% %s: "%(percent, alg)
                f_streaming_saola.write("after fs using %3d%% %s: "%(percent, alg)+'\n')
                # run_cross_validation(X[:, eval(indexes)], Y)

                X_fs = X[:, np.array(eval(indexes))-1]
                f_streaming_saola.write("size of data matrix: "+str(X_fs.shape)+'\n')
                #clf = svm.SVC(kernel='poly')
                clf = svm.SVC(kernel='linear')
                scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                #print "cross validation scores: ", scores
                f_streaming_saola.write("cross validation accuracy: "+str(scores.mean())+'\n')

                # print "**"*35
                f_streaming_saola.write("**"*35+'\n')
                percent+=10
            f_streaming_saola.write("DONE")
            f_streaming_saola.close()

def run_all_Alpha_investing(fname):
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            f_streaming_Alpha_investing = open("all_result/streaming_Alpha_investing/%s_cls.output_streaming_Alpha_investing"%dataset_name, 'w')
            print "classify dataset: %s"%dataset_name
            f_streaming_Alpha_investing.write("classify dataset: %s"%dataset_name+'\n')
            X, Y = read_data("dataset/%s.mat"%dataset_name)
            f_streaming_Alpha_investing.write("**"*35+'\n')
            f_streaming_Alpha_investing.write("origin data: "+'\n')
            # run_cross_validation(X, Y)

            f_streaming_Alpha_investing.write("size of data matrix: "+str(X.shape)+'\n')
            #clf = svm.SVC(kernel='poly')
            clf = svm.SVC(kernel='linear')
            scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
            #print "cross validation scores: ", scores
            f_streaming_Alpha_investing.write("cross validation accuracy: "+str(scores.mean())+'\n')

            # print "**"*35
            f_streaming_Alpha_investing.write("**"*35+'\n')

            indexes_set = eval(indexes_set)
            if indexes_set.size==0:
                continue
            n, d = X.shape
            d_part=(d+9)/10
            for i in range(1, 11):
                indexes = indexes_set[indexes_set<d_part*i]
                percent = i*10
                f_streaming_Alpha_investing.write("after fs using %3d%% %s: "%(percent, alg)+'\n')
                X_fs = X[:, indexes]
                f_streaming_Alpha_investing.write("size of data matrix: "+str(X_fs.shape)+'\n')
                #clf = svm.SVC(kernel='poly')
                clf = svm.SVC(kernel='linear')
                scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                #print "cross validation scores: ", scores
                f_streaming_Alpha_investing.write("cross validation accuracy: "+str(scores.mean())+'\n')

                # print "**"*35
                f_streaming_Alpha_investing.write("**"*35+'\n')
            f_streaming_Alpha_investing.write("DONE")
            f_streaming_Alpha_investing.close()


if __name__ == "__main__":
    import sys
    run(sys.argv[1])
    # run_all_osfs(sys.argv[1])
    # run_all_saola(sys.argv[1])
    print 'DONE'
