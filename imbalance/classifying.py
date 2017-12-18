
from sklearn import svm
from sklearn import linear_model
from sklearn import metrics
from sklearn import model_selection
from sklearn.model_selection import train_test_split

from sklearn.metrics import confusion_matrix
from sklearn.metrics import accuracy_score
from sklearn.metrics import matthews_corrcoef
from sklearn.metrics import recall_score
from sklearn.metrics import precision_score
from sklearn.metrics import f1_score

from draw import plotRUC
import scipy.io as sio
import numpy as np


def map_y(y):
    y0, y1 = set(y)
    y = list(y)
    if y.count(y0) < y.count(y1):
        y0, y1 = y1, y0
    y = np.array(y)
    y[y == y0] = 0
    y[y == y1] = 1
    return y


def read_data(fname):
    data = sio.loadmat(fname)
    X = data['X']
    Y = data['Y'][:, 0]
    y = map_y(Y)
    return X, y


def run_train_test_split(X_train, X_test, y_train, y_true, clf):
    clf.fit(X_train, y_train)
    y_pred = clf.predict(X_test)
    # y_pred = clf.predict_proba(X_test)[:, 1]
    # scores = model_selection.cross_val_score(clf, X, y, scoring=metrics.make_scorer(metrics.roc_auc_score))
    # scores = model_selection.cross_val_score(clf, X, y, cv=3, scoring=metrics.make_scorer(metrics.matthews_corrcoef))
    # scores = model_selection.cross_val_score(clf, X, y, cv=3, scoring=metrics.make_scorer(metrics.f1_score))
    # print scores

    print "y_true: {}".format(y_true)
    print "y_pred: {}".format(y_pred)
    print "confusion_matrix: \n{}".format(confusion_matrix(y_true, y_pred))
    print "accuray: {}".format(accuracy_score(y_true, y_pred))
    print "recall_score: {}".format(recall_score(y_true, y_pred))
    print "pression_score: {}".format(precision_score(y_true, y_pred))
    print "f1_score: {}".format(f1_score(y_true, y_pred))
    print "mattews_corrceof: {}".format(matthews_corrcoef(y_true, y_pred))

    # plotRUC(y_true, y_pred)


def run(fname, indexes, indexes_imbalance, clf, test_size=0.5):
    fname = "../datas/gene/dataset/%s.mat" % fname
    print "classifying dataset: %s" % fname
    X, y = read_data(fname)
    X_train, X_test, y_train, y_true = train_test_split(
        X, y, test_size=test_size)

    print "origin ({}): ".format(len(indexes))
    X_selected_train = X_train[:, indexes]
    X_selected_test = X_test[:, indexes]
    run_train_test_split(X_selected_train, X_selected_test,
                         y_train, y_true, clf)

    print "\nimbalance ({}): ".format(len(indexes_imbalance))
    X_selected_train = X_train[:, indexes_imbalance]
    X_selected_test = X_test[:, indexes_imbalance]
    run_train_test_split(X_selected_train, X_selected_test,
                         y_train, y_true, clf)


def main():
    # clf = svm.SVC(kernel='linear')
    clf = linear_model.LogisticRegressionCV()
    fname = "ALLAML"
    indexes_imbalance = [3, 48, 87, 148, 156, 167, 172,
                         207, 210, 1290, 1368, 1927, 2362]  # imbalance
    indexes = [3, 21, 35, 64, 87, 128, 141, 460, 1778, 1795, 1881]
    # run(fname, indexes, indexes_imbalance, clf)

    fname = "colon"
    indexes_imbalance = [2, 13, 14, 16, 69, 1259, 1643]  # imbalance
    indexes = [2, 10, 13, 16, 69, 142]
    # run(fname, indexes, indexes_imbalance, clf)

    fname = "DLBCL"
    indexes_imbalance = [2, 13, 14, 16, 69, 1259, 1643]  # imbalance
    indexes_imbalance = [0, 5, 10, 11, 51, 143, 1258]
    indexes_imbalance = [0, 5, 11, 51, 583, 1070]
    indexes_imbalance = [0, 5, 10, 11, 51, 143, 735, 1258, 1375]
    indexes = [5, 11, 12, 51, 305, 452]
    run(fname, indexes, indexes_imbalance, clf)

    fname = "GLI_85"
    # indexes = [1, 2, 5, 15, 19, 21, 26, 32, 34, 49, 60, 63, 79, 96, 104, 186, 271, 359, 519, 1281, 2375, 2945, 6936, 8517] # imbalance
    indexes_imbalance = [1, 2, 13, 15, 26, 28, 53, 96, 111, 175,
                         257, 475, 520, 674, 802, 884, 1599, 10367, 15699, 17233]
    indexes = [1, 2, 5, 12, 15, 19, 21, 23, 27, 28, 49, 50, 79,
               96, 98, 104, 113, 213, 389, 405, 551, 1990, 4132, 6034]
    # run(fname, indexes, indexes_imbalance, clf)


if __name__ == "__main__":
    main()
