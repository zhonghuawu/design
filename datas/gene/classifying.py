import os
import sys

import pandas as pd
from pandas import DataFrame, Series
from sklearn import svm, tree, ensemble
from sklearn import model_selection
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score

import numpy as np
import scipy.io as sio


def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    return X, Y


def run_cross_validation(X, y):
    print "size of data matrix: ", X.shape
    clf = svm.SVC(kernel='linear')
    # clf = tree.DecisionTreeClassifier()
    scores = model_selection.cross_val_score(
        clf, X, y, cv=5, scoring="accuracy")
    print "cross validation accuracy: ", scores.mean()
    print "standard deviation: ", scores.std()


def run(fname):
    fn = os.path.splitext(fname)[0]
    fn = os.path.split(fn)[1]
    print "classifying dataset: %s" % fn
    X, Y = read_data("dataset/%s.mat" % fn)
    print "**" * 35
    print "origin data: "
    run_cross_validation(X, Y)
    print "**" * 35
    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(":")[:2]
            print "after fs using %s: " % alg
            indexes = eval(indexes)
            run_cross_validation(X[:, indexes], Y)
            print "**" * 35


def run_one_grafting_or_l21(fname, clf, write_to_folder):
    alg = write_to_folder.split('_')[-1]
    dataset_name = os.path.split(fname)[-1].split('.')[0]
    print "classifying dataset: %s" % dataset_name
    X, Y = read_data("dataset/%s.mat" % dataset_name)
    wfname = write_to_folder + "/%s_cls.output_streaming" % (dataset_name)
    f_streaming = open(wfname, 'w')
    f_streaming.write("classify dataset: %s\n" % dataset_name)

    # classifying origin data
    f_streaming.write("**" * 35 + '\n')
    f_streaming.write("origin data: \n")
    f_streaming.write("size of data matrix: %s\n" % str(X.shape))
    scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
    f_streaming.write("cross validation accuracy: %s\n" % str(scores.mean()))
    f_streaming.write("standard deviation: %s\n" % str(scores.std()))
    f_streaming.write("**" * 35 + '\n')

    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(':')[:2]
            f_streaming.write("after fs using %s: \n" % alg)
            indexes = eval(indexes)
            X_fs = X[:, np.array(indexes)]
            f_streaming.write("size of data matrix: %s\n" % str(X_fs.shape))
            scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
            f_streaming.write("cross validation accuracy: %s\n" % str(scores.mean()))
            f_streaming.write("standard deviation: %s\n" % str(scores.std()))
            f_streaming.write("**" * 35 + '\n')
    f_streaming.write("DONE")
    f_streaming.close()


def get_datasets_name():
    fname=r'dataset/all_attribute.csv'
    datasets_fname=[]
    with open(fname, 'r') as f:
        f.readline()
        for line in f:
            datasets_fname.append(line.split(',')[0])
    return datasets_fname


def run_grafting_or_l21(ind_folder, clf, write_to_folder):
    datasets_name = get_datasets_name()
    for dataset_name in datasets_name:
        fname = ind_folder+"%s.ind_streaming"%dataset_name
        run_one_grafting_or_l21(fname, clf, write_to_folder)


def run_all_osfs_and_saola(fname, clf, write_to_folder):
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            f_streaming = open(
                write_to_folder+"/%s_cls.output_streaming" % dataset_name, 'w')
            print "classify dataset: %s" % dataset_name
            f_streaming.write("classify dataset: %s\n" % dataset_name)
            X, Y = read_data("dataset/%s.mat" % dataset_name)

            # classifying origin data
            f_streaming.write("**" * 35 + '\n')
            f_streaming.write("origin data: \n")
            f_streaming.write("size of data matrix: %s\n" % str(X.shape))
            scores = model_selection.cross_val_score(
                clf, X, Y, cv=5, scoring="accuracy")
            f_streaming.write(
                "cross validation accuracy: %s\n" % str(scores.mean()))
            f_streaming.write(
                "stardard deviation: %s\n" % str(scores.std()))

            f_streaming.write("**" * 35 + '\n')

            #classifying streaming data
            indexes_set = indexes_set.split()
            percent = 10
            for indexes in indexes_set:
                f_streaming.write(
                    "after fs using %3d%% %s: \n" % (percent, alg))
                X_fs = X[:, np.array(eval(indexes)) - 1]
                f_streaming.write(
                    "size of data matrix: %s\n" % str(X_fs.shape))
                scores = model_selection.cross_val_score(
                    clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write(
                    "cross validation accuracy: %s\n" % str(scores.mean()))
                f_streaming.write(
                    "stardard deviation: %s\n" % str(scores.std()))

                f_streaming.write("**" * 35 + '\n')
                percent += 10
            f_streaming.write("DONE")
            f_streaming.close()


def run_all_Alpha_investing(fname, clf, write_to_folder):
    with open(fname, 'r') as f:
        alg = f.readline().strip()[:-1]
        for line in f:
            dataset_name, indexes_set = line.split(':')
            dataset_name = dataset_name.strip()
            f_streaming = open(
                write_to_folder+"/%s_cls.output_streaming" % dataset_name, 'w')
            print "classify dataset: %s" % dataset_name
            f_streaming.write(
                "classify dataset: %s\n" % dataset_name)
            X, Y = read_data("dataset/%s.mat" % dataset_name)
            f_streaming.write("**" * 35 + '\n')
            f_streaming.write("origin data: \n")

            f_streaming.write(
                "size of data matrix: %s\n" % str(X.shape))
            scores = model_selection.cross_val_score(
                clf, X, Y, cv=5, scoring="accuracy")
            f_streaming.write(
                "cross validation accuracy: %s\n" % str(scores.mean()))
            f_streaming.write(
                "stardard deviation: %s\n" % str(scores.std()))

            f_streaming.write("**" * 35 + '\n')

            indexes_set = eval(indexes_set)
            if indexes_set.size == 0:
                continue
            n, d = X.shape
            d_part = (d + 9) / 10
            for i in range(1, 11):
                indexes = indexes_set[indexes_set < d_part * i]
                percent = i * 10
                f_streaming.write(
                    "after fs using %3d%% %s: " % (percent, alg) + '\n')
                X_fs = X[:, indexes]
                f_streaming.write(
                    "size of data matrix: " + str(X_fs.shape) + '\n')
                scores = model_selection.cross_val_score(
                    clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write(
                    "cross validation accuracy: " + str(scores.mean()) + '\n')
                f_streaming.write(
                    "stardard deviation: %s\n" % str(scores.std()))

                f_streaming.write("**" * 35 + '\n')
            f_streaming.write("DONE")
            f_streaming.close()


def main(fname):
    path, filename = os.path.split(fname)

    run_osfs = run_all_osfs_and_saola
    run_saola = run_all_osfs_and_saola
    run_Alpha_investing = run_all_Alpha_investing

    run_l21 = run_grafting_or_l21
    run_grafting = run_grafting_or_l21

    if filename.startswith("all_"):
        alg = os.path.splitext(filename)[0][4:]
    else :
        alg = path.split('_')[-1]

    # clf = svm.SVC(kernel="linear")
    # clf = tree.DecisionTreeClassifier()
    # clf = ensemble.RandomForestClassifier(oob_score=True)
    clf = ensemble.AdaBoostClassifier(n_estimators=100)
    write_to_folder = r"all_result_ab/streaming_%s/"%alg
    print "write to %s"%write_to_folder
    cmd = "run_%s(fname, clf, write_to_folder)"%alg
    eval(cmd)
    print "\n"

def aggr():
    fnames = (
        "all_Alpha_investing.ind_streaming",
        "all_osfs.ind_streaming",
        "all_saola.ind_streaming",
        "ind_streaming_grafting/",
        "ind_streaming_l21/"
    )

    for fname in fnames:
        main(fname)



if __name__ == "__main__":
    aggr()
    # main(sys.argv[1])
    print 'DONE'
