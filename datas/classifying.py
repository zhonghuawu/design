import os
import sys

from sklearn import svm, linear_model, tree
from sklearn import model_selection
from sklearn.model_selection import train_test_split

# from sklearn.metrics import confusion_matrix
# from sklearn.metrics import accuracy_score

import numpy as np
import scipy.io as sio

def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    return X, Y

# whole data set, use cross validation to classify
def run_cross_validation(X, y):
    clf = svm.SVC(kernel='linear')
    # clf = tree.DecisionTreeClassifier()
    scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    
    # clf = svm.SVC(kernel='linear')
    # clf = tree.DecisionTreeClassifier()
    # scores = model_selection.cross_val_score(clf, X, y, cv=5, scoring="accuracy")
    return scores

def run(fname, dataset_type, alg_name, dataset_name):
    print "classifying dataset: %s"%dataset_name
    X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))
    print "**"*35
    print "origin data: "
    print "size of data matrix: ", X.shape 
    scores = run_cross_validation(X, Y)
    # scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
    print "cross validation accuracy: ", scores.mean()
    print "**"*35
    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(":")[:2]
            print "after fs using %s: "%alg
            indexes = eval(indexes)
            X_fs = X[:, indexes]
            print "size of data matrix: ", X_fs.shape 
            scores = run_cross_validation(X_fs, Y)
            # scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
            print "cross validation accuracy: ", scores.mean()
            print "**"*35

def run_one_grafting_or_l21(fname, dataset_type, alg_name, dataset_name):
    print "classifying dataset: %s"%dataset_name
    X, Y = read_data("%s/dataset/%s.mat"%(dataset_type, dataset_name))
    wfname = "%s/all_result/streaming_%s/%s_cls.output_streaming"%(dataset_type, alg_name, dataset_name)
    f_streaming = open(wfname, 'w')
    f_streaming.write("classify dataset: %s"%dataset_name+'\n')
    f_streaming.write("**"*35+'\n')
    f_streaming.write("origin data: "+'\n')
    f_streaming.write("size of data matrix: "+str(X.shape)+'\n')
    scores = run_cross_validation(X, Y)
    # scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
    f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

    f_streaming.write("**"*35+'\n')
    with open(fname, 'r') as f:
        for line in f:
            if ':' not in line:
                continue
            alg, indexes = line.split(':')[:2]
            f_streaming.write("after fs using %s: \n"%alg)
            indexes = eval(indexes)
            X_fs = X[:, np.array(indexes)]
            f_streaming.write("size of data matrix: %s\n"%str(X_fs.shape))
            scores = run_cross_validation(X_fs, Y)
            # scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
            f_streaming.write("cross validation accuracy: %s\n"%str(scores.mean()))

            f_streaming.write("**"*35+'\n')
    f_streaming.write("DONE")
    f_streaming.close()

def run_all_osfs_or_saola(fname, dataset_type, alg_name):
    # alg_name = alg_name.split('.')[0][4:] # alg_name = osfs or saola
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
            scores = run_cross_validation(X, Y)
            # scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
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
                scores = run_cross_validation(X_fs, Y)
                # scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

                f_streaming.write("**"*35+'\n')
                percent+=10
            f_streaming.write("DONE")
            f_streaming.close()

def run_all_Alpha_investing(fname, dataset_type, alg_name):
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
            scores = run_cross_validation(X, Y)
            # scores = model_selection.cross_val_score(clf, X, Y, cv=5, scoring="accuracy")
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
                scores = run_cross_validation(X_fs, Y)
                # scores = model_selection.cross_val_score(clf, X_fs, Y, cv=5, scoring="accuracy")
                f_streaming.write("cross validation accuracy: "+str(scores.mean())+'\n')

                f_streaming.write("**"*35+'\n')
            f_streaming.write("DONE")
            f_streaming.close()

def main(fname):
    path, filename = os.path.split(fname)

    # run(fname, dataset_type, alg_name, dataset_name)

    if filename.startswith("all_"):
        dataset_type = path
        alg = os.path.splitext(filename)[0][4:]

        run_osfs = run_all_osfs_or_saola
        run_saola = run_all_osfs_or_saola
        run_Alpha_investing = run_all_Alpha_investing

        cmd = "run_%s(fname, dataset_type, \"%s\")"%(alg, alg)
        eval(cmd)
    else :
        dataset_type, alg_name = os.path.split(path)
        dataset_name = os.path.splitext(filename)[0]
        alg = alg_name.split("_")[-1]

        run_l21 = run_one_grafting_or_l21
        run_grafting = run_one_grafting_or_l21

        cmd = "run_%s(fname, dataset_type, \"%s\", dataset_name)"%(alg, alg)
        eval(cmd)
    print 'DONE'

if __name__ == "__main__":
    main(sys.argv[1])
